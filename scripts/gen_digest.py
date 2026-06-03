#!/usr/bin/env python3
"""
gen_digest.py — 生成 digest.md(LLM 友好的 Markdown 摘要)
直接可读,适合粘到 ChatGPT / Claude 聊天框当上下文。

用法: python3 gen_digest.py
输出: /workspace/ai-daily/digest.md
"""
import json, os

ROOT = "/workspace/ai-daily"
NEWS_FILE = os.path.join(ROOT, "data", "news.json")
DIGEST_FILE = os.path.join(ROOT, "digest.md")

PUBLIC_URL = "https://bbyy11.github.io/ai-daily"


def cat_label(c):
    return {"headline":"头条","rising":"新兴","company":"公司","paper":"学术","industry":"行业","social":"声音"}.get(c, c)


def heat_str(heat):
    if not heat: return ""
    score = heat.get("score", 0)
    level = heat.get("level", "")
    sources = ",".join(heat.get("sources", []))
    breakdown = heat.get("breakdown", "")
    return f"**热度:** {score} ({level}) · 来源:{sources}\n   · {breakdown}"


def render_item(it, idx):
    out = f"### {idx}. {it.get('title', '')}\n\n"
    out += f"**分类:** {cat_label(it.get('category', ''))} · **来源:** {it.get('source', '')} · **时间:** {it.get('time', '')}\n\n"
    out += f"{it.get('summary', '')}\n\n"
    h = heat_str(it.get("heat", {}))
    if h:
        out += f"{h}\n\n"
    if it.get("tags"):
        out += f"**标签:** {', '.join(it['tags'])}\n\n"
    if it.get("terms"):
        out += f"**词条:** {', '.join(it['terms'])}\n\n"
    return out


def main():
    if not os.path.exists(NEWS_FILE):
        return
    with open(NEWS_FILE, "r", encoding="utf-8") as f:
        news = json.load(f)

    items = news.get("items", [])

    md = f"""# AI Daily · {news.get('date', '')} {news.get('weekday', '')} · 全球 AI 早报

> {news.get('summary', '')}
>
> 共 {len(items)} 条新闻 · 订阅:{PUBLIC_URL}/feed.json (LLM 友好 JSON) 或 {PUBLIC_URL}/feed.xml (RSS) 或 {PUBLIC_URL}/digest.md (本文件)

---

"""
    # 头条
    headlines = [it for it in items if it.get("category") == "headline"]
    if headlines:
        md += f"## 🔥 头条 ({len(headlines)})\n\n"
        for i, it in enumerate(headlines, 1):
            md += render_item(it, i)
        md += "\n---\n\n"

    # 新兴
    rising = [it for it in items if it.get("category") == "rising"]
    if rising:
        md += f"## ⚡ 新兴 ({len(rising)})\n\n"
        for i, it in enumerate(rising, len(headlines) + 1):
            md += render_item(it, i)
        md += "\n---\n\n"

    # 其他
    others = [it for it in items if it.get("category") not in ("headline", "rising")]
    if others:
        md += f"## 📰 公司 / 行业 / 学术 / 声音 ({len(others)})\n\n"
        for i, it in enumerate(others, len(headlines) + len(rising) + 1):
            md += render_item(it, i)

    md += f"""
---

*本文件由 cron 自动生成于 {news.get('generated_at', '')}*
*完整版本:{PUBLIC_URL}/ · 归档:{PUBLIC_URL}/archive.html?date={news.get('date', '')}*
"""

    with open(DIGEST_FILE, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"[gen_digest] {DIGEST_FILE} 写入成功 ({len(items)} items)")


if __name__ == "__main__":
    main()
