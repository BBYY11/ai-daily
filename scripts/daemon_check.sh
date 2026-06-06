#!/bin/bash
# daemon_check.sh — 真硬检查循环,直接 exit 0/1,不靠 LLM
# 适合放在任何能跑 cron 的机器上(用户电脑、服务器)
# 推荐每 30 分钟跑一次

set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LOG="/tmp/ai-daily-daemon.log"
ISSUES=()

echo "[$(date -Iseconds)] daemon check start" >> "$LOG"

# 1. check_health.py — 看今天 news.json
if ! python3 scripts/check_health.py >> "$LOG" 2>&1; then
    ISSUES+=("news.json not today's")
fi

# 2. validate_news.py — 质量门
if ! python3 scripts/validate_news.py >> "$LOG" 2>&1; then
    ISSUES+=("news.json quality gate fail")
fi

# 3. sync_check.py — 远端一致性(只在 GITHUB_TOKEN_BBYY11_V2 存在时跑)
if [ -n "$GITHUB_TOKEN_BBYY11_V2" ]; then
    if ! python3 scripts/sync_check.py >> "$LOG" 2>&1; then
        ISSUES+=("sync check fail")
    fi
fi

# 4. 主页可访问性(可选,需要公网)
if [ -n "$CHECK_PUBLIC_URL" ]; then
    if ! curl -fsS -m 10 "$CHECK_PUBLIC_URL" >> "$LOG" 2>&1; then
        ISSUES+=("public url unreachable")
    fi
fi

echo "[$(date -Iseconds)] daemon check done, issues=${#ISSUES[@]}" >> "$LOG"

# 输出 JSON,方便上层(比如 systemd)读取
if [ ${#ISSUES[@]} -gt 0 ]; then
    echo "{\"status\":\"fail\",\"issues\":[$(printf '"%s",' "${ISSUES[@]}" | sed 's/,$//')]}"
    exit 1
else
    echo '{"status":"ok"}'
    exit 0
fi
