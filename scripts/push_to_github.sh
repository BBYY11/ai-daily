#!/bin/bash
# push_to_github.sh — 用 GitHub Contents API 推送 ai-daily 到 bbyy11/ai-daily
# 不用 git,直接调 REST API。绕开 git 协议层网络慢的问题。
#
# 依赖环境变量:
#   GITHUB_TOKEN_BBYY11   GitHub PAT(repo 权限)

set +e
cd "$(dirname "$0")/.."

LOG="/tmp/ai-daily-push.log"
echo "[$(date -Iseconds)] push start (api mode)" > "$LOG"

if [ -z "$GITHUB_TOKEN_BBYY11" ]; then
  echo "[push] ERROR: GITHUB_TOKEN_BBYY11 未设置" >> "$LOG"
  exit 1
fi

REPO="bbyy11/ai-daily"
BRANCH="main"
API="https://api.github.com"
AUTH="Authorization: token ${GITHUB_TOKEN_BBYY11}"
ACCEPT="Accept: application/vnd.github+json"

# 1. 拿到远端 main 的最新 commit SHA
echo "[push] 1. 取远端 main SHA" >> "$LOG"
HEAD_SHA=$(curl -fsS -H "$AUTH" -H "$ACCEPT" "$API/repos/$REPO/branches/$BRANCH" 2>>"$LOG" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['commit']['sha'])" 2>>"$LOG")
if [ -z "$HEAD_SHA" ]; then
  echo "[push] WARN: 远端 main 不存在,可能是空仓库,直接用空树 SHA" >> "$LOG"
  HEAD_SHA=""
fi
echo "[push] HEAD_SHA=$HEAD_SHA" >> "$LOG"

# 2. 拿到当前 commit 的 tree(为了基于它创建新 tree)
if [ -n "$HEAD_SHA" ]; then
  echo "[push] 2. 取 base_tree_sha" >> "$LOG"
  BASE_TREE=$(curl -fsS -H "$AUTH" -H "$ACCEPT" "$API/repos/$REPO/git/commits/$HEAD_SHA" 2>>"$LOG" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['tree']['sha'])" 2>>"$LOG")
  echo "[push] BASE_TREE=$BASE_TREE" >> "$LOG"
else
  BASE_TREE=""
fi

# 3. 收集要推送的文件列表(以 .gitignore 排除 assets/ snap.js)
echo "[push] 3. 收集文件" >> "$LOG"
FILES=()
while IFS= read -r -d '' file; do
  rel="${file#./}"
  # 排除 .git 目录
  case "$rel" in
    .git/*) continue ;;
  esac
  # 排除 assets/ 和 snap.js(以 .gitignore 为准,这里手动起一份防快选)
  case "$rel" in
    assets/*) continue ;;
    snap.js) continue ;;
  esac
  FILES+=("$rel")
done < <(find . -type f -not -path './.git/*' -print0 | sort -z)

echo "[push] 共 ${#FILES[@]} 个文件" >> "$LOG"

# 4. 用 Git Data API 创建 blob(每个文件一个)
echo "[push] 4. 创建 blobs" >> "$LOG"
BLOB_JSON="["
FIRST=1
for f in "${FILES[@]}"; do
  # base64 编码内容
  CONTENT_B64=$(base64 -w0 "$f" 2>/dev/null)
  if [ -z "$CONTENT_B64" ]; then
    echo "[push] WARN: 跳过空文件 $f" >> "$LOG"
    continue
  fi
  # 把 payload 写到临时文件,避免命令行超长
  python3 -c "import json,sys; print(json.dumps({'content': open(sys.argv[1],'rb').read().decode('utf-8','replace'), 'encoding': 'utf-8'}))" "$f" > /tmp/blob-payload.json
  BLOB_RESP=$(curl -fsS -X POST \
    -H "$AUTH" -H "$ACCEPT" -H "Content-Type: application/json" \
    -d @/tmp/blob-payload.json \
    "$API/repos/$REPO/git/blobs" 2>>"$LOG")
  if [ -z "$BLOB_RESP" ]; then
    echo "[push] ERROR: blob 创建失败 $f" >> "$LOG"
    continue
  fi
  BLOB_SHA=$(echo "$BLOB_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])" 2>/dev/null)
  if [ -z "$BLOB_SHA" ]; then
    echo "[push] ERROR: 无法解析 blob sha for $f" >> "$LOG"
    continue
  fi
  if [ $FIRST -eq 0 ]; then
    BLOB_JSON+=","
  fi
  BLOB_JSON+="$(python3 -c "import json,sys; print(json.dumps({'path': sys.argv[1], 'mode': '100644', 'type': 'blob', 'sha': sys.argv[2]}))" "$f" "$BLOB_SHA")"
  FIRST=0
done
BLOB_JSON+="]"

# 5. 创建 tree
echo "[push] 5. 创建 tree" >> "$LOG"
TREE_PAYLOAD=$(python3 -c "
import json, sys
tree = json.loads('''$BLOB_JSON''')
payload = {'tree': tree}
if '''$BASE_TREE''':
    payload['base_tree'] = '''$BASE_TREE'''
print(json.dumps(payload))
")
TREE_RESP=$(curl -fsS -X POST \
  -H "$AUTH" -H "$ACCEPT" -H "Content-Type: application/json" \
  -d "$TREE_PAYLOAD" \
  "$API/repos/$REPO/git/trees" 2>>"$LOG")
TREE_SHA=$(echo "$TREE_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])" 2>/dev/null)
if [ -z "$TREE_SHA" ]; then
  echo "[push] ERROR: tree 创建失败" >> "$LOG"
  echo "$TREE_RESP" >> "$LOG"
  exit 1
fi
echo "[push] TREE_SHA=$TREE_SHA" >> "$LOG"

# 6. 创建 commit
echo "[push] 6. 创建 commit" >> "$LOG"
COMMIT_PAYLOAD=$(python3 -c "
import json
print(json.dumps({
  'message': 'ai-daily auto-update $COMMIT_DATE',
  'tree': '''$TREE_SHA''',
  'parents': ['$HEAD_SHA'] if '''$HEAD_SHA''' else []
}))
")
COMMIT_RESP=$(curl -fsS -X POST \
  -H "$AUTH" -H "$ACCEPT" -H "Content-Type: application/json" \
  -d "$COMMIT_PAYLOAD" \
  "$API/repos/$REPO/git/commits" 2>>"$LOG")
COMMIT_SHA=$(echo "$COMMIT_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['sha'])" 2>/dev/null)
if [ -z "$COMMIT_SHA" ]; then
  echo "[push] ERROR: commit 创建失败" >> "$LOG"
  exit 1
fi
echo "[push] COMMIT_SHA=$COMMIT_SHA" >> "$LOG"

# 7. 推送 commit(更新 main 引用)
echo "[push] 7. 更新 main 引用" >> "$LOG"
REF_PAYLOAD=$(python3 -c "
import json
print(json.dumps({'sha': '''$COMMIT_SHA''', 'force': True}))
")
REF_RESP=$(curl -fsS -X PATCH \
  -H "$AUTH" -H "$ACCEPT" -H "Content-Type: application/json" \
  -d "$REF_PAYLOAD" \
  "$API/repos/$REPO/git/refs/heads/$BRANCH" 2>>"$LOG")
REF_SHA=$(echo "$REF_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('object',{}).get('sha',''))" 2>/dev/null)
if [ -n "$REF_SHA" ]; then
  echo "[push] OK: 推送完成" >> "$LOG"
  echo "[push] 公网链接: https://bbyy11.github.io/ai-daily/" >> "$LOG"
  echo "[push] 1-2 分钟后 GitHub Pages 会自动刷新" >> "$LOG"
else
  echo "[push] ERROR: ref 更新失败" >> "$LOG"
  echo "$REF_RESP" >> "$LOG"
  exit 1
fi

echo "[$(date -Iseconds)] push done" >> "$LOG"
cat "$LOG"
