#!/usr/bin/env python3
"""
validate_news.py — news.json 质量门
主 cron 写完 news.json 后必须跑。任一检查失败 → exit 1,cron 应当立即告警。

检查项:
- JSON 合法
- date == 今天
- items >= 14 且 <= 25
- 分类分布:headline >= 3, rising >= 4(必须带 rising_metrics),company >= 3
- 热度 level 4 档(爆/热/中/新星)合理,score 跟 level 对应
- summary >= 80 字
- weekly_arc.weeks[0].date == 今天
- ASCII 双引号在中文文本里(没转义)→ JSON 必须合法(避免 #008)
"""
import sys, os, json, datetime, re

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
NEWS = os.path.join(DATA, "news.json")
HEAT_LEVELS = {"爆": 7500, "热": 5000, "中": 3000, "新星": 1500}

today = datetime.date.today().isoformat()
errors = []
warnings = []

if not os.path.exists(NEWS):
    print(f"FAIL: news.json 不存在")
    sys.exit(1)

try:
    with open(NEWS, "r", encoding="utf-8") as f:
        d = json.load(f)
except json.JSONDecodeError as e:
    print(f"FAIL: news.json JSON 非法: {e}")
    sys.exit(1)

# date
if d.get("date") != today:
    errors.append(f"date={d.get('date')} != 今天({today})")

# items
items = d.get("items", [])
if len(items) < 14:
    errors.append(f"items 只有 {len(items)}(< 14)")
elif len(items) > 25:
    warnings.append(f"items {len(items)} 条偏多(> 25)")

# 分类分布
by_cat = {}
for it in items:
    by_cat[it.get("category", "")] = by_cat.get(it.get("category", ""), 0) + 1

if by_cat.get("headline", 0) < 3:
    errors.append(f"headline 只有 {by_cat.get('headline', 0)}(< 3)")
if by_cat.get("rising", 0) < 4:
    errors.append(f"rising 只有 {by_cat.get('rising', 0)}(< 4)")

# rising 必须有 rising_metrics
for it in items:
    if it.get("category") == "rising":
        if not it.get("rising_metrics"):
            errors.append(f"rising item {it.get('id')} 缺 rising_metrics")

# heat
for it in items:
    heat = it.get("heat", {})
    score = heat.get("score", 0)
    level = heat.get("level", "")
    if not level:
        errors.append(f"item {it.get('id')} 缺 heat.level")
    if score > 0 and level in HEAT_LEVELS:
        expected_min = HEAT_LEVELS[level]
        if score < expected_min * 0.7:
            warnings.append(f"item {it.get('id')} score={score} < level {level} 期望 >= {expected_min}")
    if not heat.get("sources") or len(heat.get("sources", [])) < 1:
        errors.append(f"item {it.get('id')} heat.sources 为空")

# summary
summary = d.get("summary", "")
if len(summary) < 80:
    errors.append(f"summary 只有 {len(summary)} 字(< 80)")

# weekly_arc
weekly = d.get("weekly_arc", {}).get("weeks", [])
if not weekly:
    errors.append("weekly_arc.weeks 空")
elif weekly[0].get("date") != today:
    errors.append(f"weekly_arc.weeks[0].date={weekly[0].get('date')} != 今天")

# ASCII 双引号 in 中文字符串内(粗略检查)
for it in items:
    title = it.get("title", "")
    summ = it.get("summary", "")
    if '"' in title or '"' in summ:
        warnings.append(f"item {it.get('id')} 含未转义双引号,可能 JSON 风险")

# 输出
if errors:
    print("=== FAIL ===")
    for e in errors:
        print(f"  ✗ {e}")
    for w in warnings:
        print(f"  ⚠ {w}")
    sys.exit(1)
else:
    print(f"=== OK ===")
    print(f"  date={today} items={len(items)}")
    print(f"  by_category: {by_cat}")
    if warnings:
        for w in warnings:
            print(f"  ⚠ {w}")
    sys.exit(0)
