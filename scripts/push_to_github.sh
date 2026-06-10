#!/bin/bash
# push_to_github.sh — 用 GitHub Contents API 推送 ai-daily 到 bbyy11/ai-daily
# 不用 git,直接调 REST API。绕开 git 协议层网络慢的问题。
#
# 依赖环境变量:
#   GITHUB_TOKEN_BBYY11_V2   GitHub PAT(repo 权限)

set +e
cd "$(dirname "$0")/.."

LOG="/tmp/ai-daily-push.log"
echo "[$(date -Iseconds)] push start (api mode)" > "$LOG"

if [ -z "$GITHUB_TOKEN_BBYY11_V2" ]; then
  echo "[push] ERROR: GITHUB_TOKEN_BBYY11_V2 未设置" >> "$LOG"
  exit 1
fi

REPO="bbyy11/ai-daily"
BRANCH="main"
API="https://api.github.com"
AUTH="Authorization: token ${GITHUB_TOKEN_BBYY11_V2}"
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

# 2.5 去重检查:对比本地 news.json 内容跟远端最新 news.json 是否完全相同
# 避免 LLM session 重复触发造成同一份内容推两次(事故 #012)
# 注:只在 news.json 跟远端完全一致时跳过该项(不全局退出)
SKIP_NEWS=""
if [ -f "data/news.json" ] && [ -n "$HEAD_SHA" ]; then
  echo "[push] 2.5 去重检查" >> "$LOG"
  REMOTE_NEWS=$(curl -fsS -H "$AUTH" -H "$ACCEPT" "$API/repos/$REPO/contents/data/news.json?ref=$BRANCH" 2>>"$LOG" | python3 -c "import sys,json,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode('utf-8'))" 2>>"$LOG")
  if [ -n "$REMOTE_NEWS" ]; then
    LOCAL_HASH=$(python3 -c "import hashlib,json; d=json.load(open('data/news.json')); s=json.dumps(d,sort_keys=True,ensure_ascii=False); print(hashlib.sha256(s.encode()).hexdigest())" 2>>"$LOG")
    REMOTE_HASH=$(python3 -c "import hashlib,json; d=json.loads('''$REMOTE_NEWS'''); s=json.dumps(d,sort_keys=True,ensure_ascii=False); print(hashlib.sha256(s.encode()).hexdigest())" 2>>"$LOG")
    if [ "$LOCAL_HASH" = "$REMOTE_HASH" ]; then
      SKIP_NEWS="data/news.json"
      echo "[push] ⊘ news.json 与远端一致(同内容 sha=${LOCAL_HASH[:12]}),该文件跳过" >> "$LOG"
    fi
  fi
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
  # 跳过跟远端一致的 news.json
  if [ "$rel" = "$SKIP_NEWS" ]; then
    continue
  fi
  # 排除(以 .gitignore 为准,这里手动起一份防快选)
  case "$rel" in
    assets/preview-*.png) continue ;;
    snap.js) continue ;;
    scripts/__pycache__/*) continue ;;
    *.pyc) continue ;;
    *.pyo) continue ;;
    *.log) continue ;;
    .DS_Store) continue ;;
    # .github/ 目录不能通过 Contents API 推送(GitHub 安全机制)
    # 要推 .github/workflows/*.yml 需要带 'workflow' scope 的 token
    # 详见 scripts/README.md
    .github/*) continue ;;
  esac
  FILES+=("$rel")
done < <(find . -type f -not -path './.git/*' -print0 | sort -z)

# 4.0.5 【幽灵文件检查】对比本地文件列表与仓库远端,提醒需删除的远端文件
# (API 拉取所有文件可能超大,这里只提醒 4 个已知的)
REMOTE_TO_DELETE=(
  "weekly.html"            # 6-04 改名后未删除
  "snap.js"                # .gitignore 之前的 commit 遗留下
  "scripts/__pycache__"    # pycache 误推
)
for f in "${REMOTE_TO_DELETE[@]}"; do
  REMOTE_CHECK=$(curl -fsS -H "$AUTH" -H "$ACCEPT" "$API/repos/$REPO/contents/$f" 2>>"$LOG" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('name',''))" 2>/dev/null)
  if [ -n "$REMOTE_CHECK" ]; then
    echo "[push] ⚠ 远端有幽灵文件 $f,本次推送不会删除它。请手动 git rm 或在 GitHub 网页删除" >> "$LOG"
  fi
done

# 4.0 【数据保护】检查 news.json 是否是今天的——不是今天则警告、提示用户
if [ -f "data/news.json" ]; then
  NEWS_DATE=$(python3 -c "import json; d=json.load(open('data/news.json')); print(d.get('date',''))" 2>/dev/null)
  TODAY=$(TZ=Asia/Shanghai date +%Y-%m-%d)
  if [ -z "$NEWS_DATE" ]; then
    echo "[push] ⚠ news.json 读不出 date,可能 JSON 损坏"
  elif [ "$NEWS_DATE" != "$TODAY" ]; then
    # 允许两个例外:1) summary 含 PLACEHOLDER 2) 手动带上 --force-data
    IS_PLACEHOLDER=$(python3 -c "import json; d=json.load(open('data/news.json')); s=d.get('summary',''); print('yes' if ('PLACEHOLDER' in s or '🚧' in s) else 'no')" 2>/dev/null)
    if [ "$IS_PLACEHOLDER" = "yes" ] || [ "$1" = "--force-data" ]; then
      echo "[push] ⚠ news.json date=$NEWS_DATE != 今天($TODAY),但属于 PLACEHOLDER 或 --force-data,放行" >> "$LOG"
    else
      echo "[push] ❌ REFUSE: news.json date=$NEWS_DATE 不是今天($TODAY),拒绝推送!"
      echo "[push] 如果确认要推(比如手写补当天的),加 --force-data 参数"
      echo "[push] 建议:先 cp data/news.json data/archive/${NEWS_DATE}.json 备份"
      exit 2
    fi
  else
    echo "[push] ✓ news.json date=$NEWS_DATE == 今天,放行" >> "$LOG"
  fi
fi

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
  'message': 'ai-daily auto-update $COMMIT_DATE MavisBot',
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
