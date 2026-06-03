#!/bin/bash
# daily.sh — AI 早报全流程触发脚本
# 由 cron 每天 08:00 (Asia/Shanghai) 调用
# 流程: 拉信源 → 重生成 → 部署 → 推送

set -e
cd "$(dirname "$0")/.."

echo "[daily] $(date -Iseconds) start"

# 1. 抓信源
python3 scripts/fetch_news.py

# 2. 抓信源+生成 new.json + terms.json 由上层 agent 完成(读取 search_queries.txt 后用 web_search)
#    生成后写到 data/news.json + data/terms.json

# 3. 推送
python3 scripts/push.py

echo "[daily] $(date -Iseconds) done"
