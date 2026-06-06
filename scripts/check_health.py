#!/usr/bin/env python3
"""
check_health.py — AI Daily watchdog 健康检查
由 ai-daily-watchdog cron 调,不用内嵌 Python -c,避免引号转义陷阱。
返回 0=正常 / 1=异常(stdout 有 ALERT 前缀)

检查项:
1. news.json.date == 今天
2. news.json.items >= 14
3. news.json.summary >= 80 字
4. news.json 没有 PLACEHOLDER 标记
5. weekly_arc.weeks[0].date == 今天
"""
import sys, os, json, datetime

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
NEWS = os.path.join(DATA, "news.json")

today = datetime.date.today().isoformat()
issues = []

# 1. news.json 存在
if not os.path.exists(NEWS):
    print(f"ALERT: news.json 不存在")
    sys.exit(1)

# 2. JSON 合法 + 字段
try:
    with open(NEWS, "r", encoding="utf-8") as f:
        d = json.load(f)
except json.JSONDecodeError as e:
    print(f"ALERT: news.json JSON 不合法: {e}")
    sys.exit(1)

date = d.get("date", "")
items = d.get("items", [])
summary = d.get("summary", "")
weekly = d.get("weekly_arc", {}).get("weeks", [])

if date != today:
    issues.append(f"news.json.date={date} != 今天({today})")
if len(items) < 14:
    issues.append(f"items 只有 {len(items)} 条(< 14)")
if len(summary) < 80:
    issues.append(f"summary 只有 {len(summary)} 字(< 80)")
if "PLACEHOLDER" in summary or "🚧" in summary:
    issues.append("news.json 还是占位骨架(包含 PLACEHOLDER 标记)")
if not weekly:
    issues.append("weekly_arc.weeks 是空")
elif weekly[0].get("date") != today:
    issues.append(f"weekly_arc.weeks[0].date={weekly[0].get('date')} != 今天")

# 汇总
if issues:
    print("ALERT: " + " | ".join(issues))
    sys.exit(1)
else:
    print(f"OK date={date} items={len(items)} summary={len(summary)}字")
    sys.exit(0)
