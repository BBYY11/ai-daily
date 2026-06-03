#!/usr/bin/env python3
"""
gen_json_feed.py — 生成 JSON Feed v1.1 (https://www.jsonfeed.org/)
对 LLM(ChatGPT / Claude / Gemini)最友好的格式,因为它们解析 JSON 很稳。

用法: python3 gen_json_feed.py
输出: /workspace/ai-daily/feed.json
"""
import json, os, datetime

ROOT = "/workspace/ai-daily"
NEWS_FILE = os.path.join(ROOT, "data", "news.json")
FEED_JSON = os.path.join(ROOT, "feed.json")

PUBLIC_URL = "https://bbyy11.github.io/ai-daily"
ARCHIVE_BASE = f"{PUBLIC_URL}/archive-view.html"


def main():
    if not os.path.exists(NEWS_FILE):
        print(f"[gen_json_feed] news.json 缺失,跳过")
        return
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        news = json.load(f)

    items = []
    for it in news.get("items", []):
        heat = it.get("heat", {})
        items.append({
            "id": it.get("id", ""),
            "title": it.get("title", ""),
            "summary": it.get("summary", ""),
            "category": it.get("category", ""),
            "category_label": {
                "headline": "头条", "company": "公司", "paper": "学术",
                "industry": "行业", "social": "声音", "rising": "新兴"
            }.get(it.get("category", ""), it.get("category", "")),
            "source": it.get("source", ""),
            "time": it.get("time", ""),
            "tags": it.get("tags", []),
            "terms": it.get("terms", []),
            "heat": {
                "score": heat.get("score", 0),
                "level": heat.get("level", ""),
                "sources": heat.get("sources", []),
                "breakdown": heat.get("breakdown", "")
            },
            "comments": it.get("comments", 0),
            "url": f"{ARCHIVE_BASE}?date={it.get('time', '')}"
        })

    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": f"AI Daily · {news.get('date', '')} {news.get('weekday', '')} · 全球 AI 早报",
        "home_page_url": f"{PUBLIC_URL}/",
        "feed_url": f"{PUBLIC_URL}/feed.json",
        "description": news.get("summary", ""),
        "language": "zh-cn",
        "authors": [{"name": "AI Daily", "url": PUBLIC_URL}],
        "items": items,
        "_meta": {
            "format": "jsonfeed-1.1",
            "total_items": len(items),
            "generated_at": news.get("generated_at", ""),
            "tip_for_llm": "This is a daily AI news digest. Each item has a 'heat' object with score/level/sources for popularity signal, and 'category' for type. Useful for trend analysis, summarization, and monitoring."
        }
    }

    with open(FEED_JSON, "w", encoding="utf-8") as f:
        json.dump(feed, f, ensure_ascii=False, indent=2)
    print(f"[gen_json_feed] {FEED_JSON} 写入成功 ({len(items)} items)")


if __name__ == "__main__":
    main()
