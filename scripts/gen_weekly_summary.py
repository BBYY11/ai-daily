#!/usr/bin/env python3
"""
gen_weekly_summary.py
每周一 8 点 cron 触发。读取上周一到上周日(Asia/Shanghai)的 7 天归档,
生成 weekly_summary.json(块 1 数据源)。

用法: python3 gen_weekly_summary.py
输出: /workspace/ai-daily/data/weekly_summary.json
"""
import json, os, datetime, sys

DATA_DIR = "/workspace/ai-daily/data"
ARCHIVE_DIR = os.path.join(DATA_DIR, "archive")
WEEKLY_FILE = os.path.join(DATA_DIR, "weekly_summary.json")


def iso_week_label(dt):
    """2026-W21 这样的标签"""
    y, w, _ = dt.isocalendar()
    return f"{y}-W{w:02d}"


def get_last_week_range(today=None):
    """返回上周一到上周日的 (start_date, end_date, week_label)"""
    if today is None:
        today = datetime.date.today()
    # 找到上周一(今天是周几,周一=0...周日=6,但 Python weekday() 周一=0...周日=6)
    days_since_monday = today.weekday()  # 周一是 0
    this_monday = today - datetime.timedelta(days=days_since_monday)
    last_monday = this_monday - datetime.timedelta(days=7)
    last_sunday = this_monday - datetime.timedelta(days=1)
    return last_monday, last_sunday, iso_week_label(last_monday)


def weekday_cn(d):
    return ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][d.weekday()]


def load_archive(date_str):
    fp = os.path.join(ARCHIVE_DIR, f"{date_str}.json")
    if not os.path.exists(fp):
        return None
    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    start, end, label = get_last_week_range()

    days = []
    cur = start
    while cur <= end:
        date_str = cur.isoformat()
        d = load_archive(date_str)
        if d:
            # 找该日最具代表性的新闻(取前 3 条 headline)
            top = [it for it in d.get("items", []) if it.get("category") == "headline"][:3]
            summary = "; ".join([it["title"][:50] for it in top]) if top else \
                      (d.get("summary", "(无摘要)")[:200])
            days.append({
                "date": date_str,
                "weekday": weekday_cn(cur),
                "summary": summary
            })
        else:
            days.append({
                "date": date_str,
                "weekday": weekday_cn(cur),
                "summary": "(无归档)"
            })
        cur += datetime.timedelta(days=1)

    # 汇总趋势
    valid_days = [d for d in days if "无" not in d["summary"]]
    summary = f"第 {label.split('-W')[1]} 周({start.isoformat()} - {end.isoformat()})AI 圈共 {len(valid_days)} 天有归档,共 {sum(len(load_archive(d['date']).get('items', [])) for d in valid_days if load_archive(d['date']))} 条新闻。详细主题待 cron 任务上层 agent 提炼。"

    # 5 个主题(空骨架,让上层 agent 填)
    key_themes = [
        {"title": "(待生成)", "body": "待上层 agent 提炼,基于上周 daily items 的 high-heat 条目聚类"},
        {"title": "(待生成)", "body": ""},
        {"title": "(待生成)", "body": ""},
        {"title": "(待生成)", "body": ""},
        {"title": "(待生成)", "body": ""}
    ]

    out = {
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M (Asia/Shanghai)"),
        "week": label,
        "week_label": f"第 {label.split('-W')[1]} 周",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "weekday_start": weekday_cn(start),
        "weekday_end": weekday_cn(end),
        "summary": summary,
        "key_themes": key_themes,
        "data_highlights": {
            "total_events": sum(len(load_archive(d['date']).get("items", [])) for d in valid_days if load_archive(d['date'])),
            "key_funding_total": "—",
            "biggest_news": "—"
        },
        "day_links": days
    }

    with open(WEEKLY_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"OK weekly_summary.json: {label} ({start} → {end}), {len(valid_days)} valid days")


if __name__ == "__main__":
    main()
