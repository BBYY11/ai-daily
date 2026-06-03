#!/usr/bin/env python3
"""
gen_monthly_summary.py
每月最后一天 8 点 cron 触发(由 cron 表达式 + 上层判断是否最后一天)。
读取当月所有日归档,生成当月 summary 追加到 monthly_archive.json。

用法: python3 gen_monthly_summary.py [YYYY-MM]
不传参:自动判断"今天是不是该月最后一天,是的话生成当月 summary"
传参: 强制生成指定月份(用于补跑)
"""
import json, os, datetime, sys
from calendar import monthrange

DATA_DIR = "/workspace/ai-daily/data"
ARCHIVE_DIR = os.path.join(DATA_DIR, "archive")
MONTHLY_FILE = os.path.join(DATA_DIR, "monthly_archive.json")


def load_archive(date_str):
    fp = os.path.join(ARCHIVE_DIR, f"{date_str}.json")
    if not os.path.exists(fp):
        return None
    with open(fp, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # 解析参数
    if len(sys.argv) > 1:
        target_month = sys.argv[1]  # 2026-06
    else:
        today = datetime.date.today()
        # 今天是该月最后一天?
        last_day = monthrange(today.year, today.month)[1]
        if today.day != last_day:
            print(f"[gen_monthly] 今天 {today} 不是该月最后一天({last_day}),退出")
            return
        target_month = f"{today.year}-{today.month:02d}"

    # 检查月度是否已存在
    if os.path.exists(MONTHLY_FILE):
        with open(MONTHLY_FILE, "r", encoding="utf-8") as f:
            monthly = json.load(f)
    else:
        monthly = {"generated_at": "", "period_label": "", "period_summary": "", "months": []}

    # 已存在该月则跳过
    if any(m["date"] == target_month for m in monthly["months"]):
        print(f"[gen_monthly] {target_month} 已存在,跳过")
        return

    # 读该月所有日
    year, month = map(int, target_month.split("-"))
    last_day = monthrange(year, month)[1]
    days_data = []
    for d in range(1, last_day + 1):
        ds = f"{target_month}-{d:02d}"
        data = load_archive(ds)
        if data:
            days_data.append(data)

    if not days_data:
        print(f"[gen_monthly] {target_month} 没有归档数据,跳过")
        return

    # 汇总
    all_items = []
    for d in days_data:
        all_items.extend(d.get("items", []))

    headlines = [it for it in all_items if it.get("category") == "headline"]
    rising = [it for it in all_items if it.get("category") == "rising"]
    total_items = len(all_items)

    # 输出骨架(上层 cron agent 会改写 trend_summary / look_ahead / data_points)
    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    first_dt = datetime.date(year, month, 1)
    last_dt = datetime.date(year, month, last_day)
    first_weekday = weekday_cn[first_dt.weekday()]
    last_weekday = weekday_cn[last_dt.weekday()]

    new_month = {
        "date": target_month,
        "title": f"{target_month} 月度总结(待生成标题)",
        "trend_summary": f"{target_month} 月({first_dt.isoformat()} {first_weekday} 至 {last_dt.isoformat()} {last_weekday})AI 圈共 {len(days_data)} 天归档,总计 {total_items} 条新闻,其中头条 {len(headlines)} 条 / 新兴项目 {len(rising)} 条。详细趋势分析待上层 cron agent 提炼。",
        "key_events": [f"{it['title']} ({it['time']})" for it in headlines[:10]],
        "data_points": [
            f"总新闻数:{total_items}",
            f"头条:{len(headlines)} / 新兴:{len(rising)} / 公司:0 / 论文:0 / 行业:0 / 声音:0(待补)",
            f"天数:{len(days_data)}",
        ],
        "look_ahead": f"待下月 1 号 cron 跑完后,在 monthly_archive.json 添加 {target_month} 月总结"
    }

    monthly["months"].append(new_month)
    # 保持月份按时间升序
    monthly["months"].sort(key=lambda m: m["date"])

    with open(MONTHLY_FILE, "w", encoding="utf-8") as f:
        json.dump(monthly, f, ensure_ascii=False, indent=2)
    print(f"OK monthly_archive.json: append {target_month} ({len(days_data)} days, {total_items} items, {len(headlines)} headlines)")


if __name__ == "__main__":
    main()
