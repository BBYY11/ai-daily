#!/usr/bin/env python3
"""
archive_weekly.py
每周一 cron 在 gen_weekly_summary.py 之后跑。
把 data/weekly_summary.json 复制到 data/archive/weekly/{week}.json(永久保存)，
并重建 data/archive/weekly/index.json 清单。

用法: python3 archive_weekly.py
"""
import json, os, datetime, sys

DATA_DIR = "/workspace/ai-daily/data"
WEEKLY_FILE = os.path.join(DATA_DIR, "weekly_summary.json")
ARCHIVE_DIR = os.path.join(DATA_DIR, "archive", "weekly")
INDEX_FILE = os.path.join(ARCHIVE_DIR, "index.json")


def main():
    if not os.path.exists(WEEKLY_FILE):
        print(f"[archive_weekly] {WEEKLY_FILE} 不存在,跳过")
        return
    with open(WEEKLY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    week = data.get("week", "")
    if not week:
        print(f"[archive_weekly] weekly_summary.json 缺少 week 字段,跳过")
        return

    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    dest = os.path.join(ARCHIVE_DIR, f"{week}.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[archive_weekly] 已归档 {dest}")

    # 重建 index.json
    weeks = []
    for fn in sorted(os.listdir(ARCHIVE_DIR), reverse=True):
        if not fn.endswith(".json") or fn == "index.json":
            continue
        fp = os.path.join(ARCHIVE_DIR, fn)
        try:
            with open(fp, "r", encoding="utf-8") as f:
                d = json.load(f)
            weeks.append({
                "week": d.get("week", fn[:-5]),
                "week_label": d.get("week_label", ""),
                "start_date": d.get("start_date", ""),
                "end_date": d.get("end_date", ""),
                "summary": d.get("summary", "")[:120] + ("..." if len(d.get("summary", "")) > 120 else ""),
                "key_themes_count": len(d.get("key_themes", [])),
            })
        except Exception as e:
            print(f"[archive_weekly] 跳过 {fn}: {e}")
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump({"weeks": weeks, "total": len(weeks)}, f, ensure_ascii=False, indent=2)
    print(f"[archive_weekly] {INDEX_FILE} 已更新 ({len(weeks)} weeks)")


if __name__ == "__main__":
    main()
