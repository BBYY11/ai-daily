#!/usr/bin/env python3
"""
sync_check.py — 远端 vs 本地文件 SHA 一致性检查
用 Contents API 拉每个文件的实际内容,sha1 后跟本地比。
"""
import sys, os, json, urllib.request, hashlib

REPO = "bbyy11/ai-daily"
TOKEN = os.environ.get("GITHUB_TOKEN_BBYY11_V2", "")
BRANCH = "main"
LOCAL_ROOT = "/workspace/ai-daily"

def gh_get(path):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={BRANCH}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json",
    })
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return None

def gh_get_tree():
    url = f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1"
    req = urllib.request.Request(url, headers={"Authorization": f"token {TOKEN}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def main():
    tree = gh_get_tree()
    remote_blobs = sorted([it['path'] for it in tree.get('tree', []) if it['type'] == 'blob'])
    local_files = []
    for root, dirs, files in os.walk(LOCAL_ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
        for f in files:
            if f.endswith(('.pyc', '.pyo', '.log', '.DS_Store', 'snap.js')):
                continue
            if f.startswith('preview-') and f.endswith('.png'):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, LOCAL_ROOT).replace(os.sep, '/')
            local_files.append(rel)
    local_files = sorted(local_files)

    remote_set = set(remote_blobs)
    local_set = set(local_files)

    only_remote = remote_set - local_set
    only_local = local_set - remote_set
    common = remote_set & local_set

    print(f"=== 远端 {len(remote_blobs)} 个文件,本地 {len(local_files)} 个 ===")
    print()
    if only_remote:
        print(f"⚠ 远端有,本地没有(幽灵文件): {len(only_remote)} 个")
        for f in sorted(only_remote):
            print(f"  - {f}")
    if only_local:
        print(f"⚠ 本地有,远端没有(未推送): {len(only_local)} 个")
        for f in sorted(only_local):
            print(f"  - {f}")

    if not only_remote and not only_local:
        print("✓ 文件清单完全一致")

    # SHA 比对(common 文件,抽查)
    print()
    print("=== SHA 比对(抽查 15 个)===")
    for f in sorted(common)[:15]:
        d = gh_get(f)
        if not d or 'content' not in d:
            print(f"  ⚠ 拉不到 {f}")
            continue
        import base64
        remote_bytes = base64.b64decode(d['content'])
        remote_sha = hashlib.sha1(remote_bytes).hexdigest()[:8]
        local_path = os.path.join(LOCAL_ROOT, f)
        if os.path.exists(local_path):
            with open(local_path, 'rb') as fp:
                content = fp.read()
            local_sha = hashlib.sha1(content).hexdigest()[:8]
            match = "✓" if remote_sha == local_sha else "✗"
            print(f"  {match}  远端 {remote_sha}  本地 {local_sha}  {f}")

if __name__ == "__main__":
    main()
