#!/usr/bin/env python3
"""
gen_feed.py — 读取 data/news.json 生成 RSS 2.0 XML
供 RSS 阅读器和 AI Agent 订阅。

用法: python3 gen_feed.py
输出: /workspace/ai-daily/feed.xml

RSS 2.0 schema,中文标题,UTF-8,每条新闻 1 个 <item>。
额外字段(给 Agent 用):用 <category> 标分类,<heat:score> 标热度(命名空间),
<source:url> 标原文链接,<guid isPermaLink="false"> 标唯一 ID。
"""
import json, os, datetime, html, re

ROOT = "/workspace/ai-daily"
NEWS_FILE = os.path.join(ROOT, "data", "news.json")
FEED_FILE = os.path.join(ROOT, "feed.xml")

PUBLIC_URL = "https://bbyy11.github.io/ai-daily"
ARCHIVE_BASE = f"{PUBLIC_URL}/archive-view.html"


def xml_escape(s):
    return html.escape(str(s or ""), quote=True)


def strip_html(s):
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", "", str(s))
    s = re.sub(r"\s+", " ", s).strip()
    return s


def build_item(item):
    """构造一个 <item> 元素"""
    title = xml_escape(item.get("title", ""))
    desc = xml_escape(strip_html(item.get("summary", "")))
    source = xml_escape(item.get("source", ""))
    cat = item.get("category", "")
    time = item.get("time", "")
    heat = item.get("heat", {})
    heat_score = heat.get("score", 0)
    heat_level = heat.get("level", "")
    heat_sources = ",".join(heat.get("sources", []))
    comments = item.get("comments", 0)
    item_id = item.get("id", "")
    tags = item.get("tags", [])
    terms = item.get("terms", [])

    # pubDate 用 ISO 8601 格式
    pub_date = time
    if time:
        try:
            d = datetime.datetime.strptime(time.split()[0], "%Y-%m-%d")
            pub_date = d.strftime("%a, %d %b %Y 00:00:00 +0800")
        except Exception:
            pass

    # archive 链接(回到单日快照)
    link = f"{ARCHIVE_BASE}?date={time}"

    # category 作为 XML category
    cat_cn = {"headline":"头条","company":"公司","paper":"学术","industry":"行业","social":"声音","rising":"新兴"}.get(cat, cat)
    categories = f"<category>{xml_escape(cat_cn)}</category>"

    # 来源作为 source 标签
    source_tag = f'<source url="{link}">{source}</source>' if source else ""

    # 命名空间扩展:热度信息
    heat_ext = (
        f'<heat:item xmlns:heat="https://bbyy11.github.io/ai-daily/ns/heat">'
        f'<heat:score>{heat_score}</heat:score>'
        f'<heat:level>{xml_escape(heat_level)}</heat:level>'
        f'<heat:sources>{xml_escape(heat_sources)}</heat:sources>'
        f'<heat:comments>{comments}</heat:comments>'
        f'</heat:item>'
    )

    # 标签
    tag_ext = "".join(f'<category>{xml_escape(t)}</category>' for t in tags[:6])

    return f"""    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid isPermaLink="false">ai-daily-{item_id}</guid>
      <pubDate>{pub_date}</pubDate>
      <description><![CDATA[{desc}]]></description>
      {categories}
      {tag_ext}
      {source_tag}
      {heat_ext}
    </item>"""


def build_feed(news):
    date = news.get("date", "")
    weekday = news.get("weekday", "")
    summary = strip_html(news.get("summary", ""))
    items = news.get("items", [])

    last_build = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0800")
    title = f"AI Daily · {date} {weekday} · 全球 AI 早报"
    desc = f"{summary} · 共 {len(items)} 条新闻"

    items_xml = "\n".join(build_item(it) for it in items)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:atom="http://www.w3.org/2005/Atom"
     xmlns:heat="https://bbyy11.github.io/ai-daily/ns/heat">
  <channel>
    <title>{xml_escape(title)}</title>
    <link>{PUBLIC_URL}/</link>
    <atom:link href="{PUBLIC_URL}/feed.xml" rel="self" type="application/rss+xml" />
    <description><![CDATA[{desc}]]></description>
    <language>zh-cn</language>
    <lastBuildDate>{last_build}</lastBuildDate>
    <generator>AI Daily (Mavis)</generator>
    <managingEditor>bbyy11 (via Mavis)</managingEditor>
    <ttl>60</ttl>
{items_xml}
  </channel>
</rss>
"""


def main():
    if not os.path.exists(NEWS_FILE):
        print(f"[gen_feed] {NEWS_FILE} 不存在,跳过")
        return
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        news = json.load(f)
    items = news.get("items", [])
    if not items:
        print(f"[gen_feed] news.json 无 items,跳过")
        return
    xml = build_feed(news)
    with open(FEED_FILE, "w", encoding="utf-8") as f:
        f.write(xml)
    print(f"[gen_feed] {FEED_FILE} 写入成功 ({len(items)} items, {len(xml)} bytes)")


if __name__ == "__main__":
    main()
