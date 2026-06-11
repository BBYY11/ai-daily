#!/usr/bin/env python3
"""AI Daily Fallback — OpenAI gpt-4o-mini 兜底生成早报

设计: 这个脚本只跑在 GitHub Actions runner 上,由 ai-daily-fallback.yml 调用。
逻辑:
  1. 拉 7 天 archive 上下文
  2. 调 OpenAI API 生成 18 条早报
  3. 校验 JSON
  4. 写 data/news.json
  5. 跑 validate_news.py / gen_feed / gen_json_feed / gen_digest
  6. (workflow 自己) commit + push

环境变量:
  OPENAI_API_KEY  OpenAI API key(必填)
"""
import os
import sys
import json
import datetime
import urllib.request


def fetch_archive_context(data_dir: str = "data", days: int = 7) -> str:
    """读最近 7 天 archive 的 5 条 title,作为 prompt 上下文"""
    archive_dir = os.path.join(data_dir, "archive")
    if not os.path.isdir(archive_dir):
        return ""

    dates = []
    for f in sorted(os.listdir(archive_dir)):
        if f.endswith(".json") and f != "index.json":
            dates.append(f[:-5])
    dates = dates[-days:]

    lines = []
    for d in dates:
        path = os.path.join(archive_dir, f"{d}.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                a = json.load(f)
                titles = [it.get("title", "")[:50] for it in a.get("items", [])[:5]]
                lines.append(f"[{d}] " + " | ".join(titles))
        except Exception as e:
            print(f"[fallback] warn: read {d} failed: {e}", file=sys.stderr)
    return "\n".join(lines)


def build_prompt(today: str, weekday_cn: str, iso_year: int, iso_week: int, archive_context: str) -> str:
    return f"""你是 AI 早报编辑, 今天是 {today} {weekday_cn}, ISO 周 {iso_year}-W{iso_week:02d}

上一周上下文 {archive_context}

任务: 生成今天全球 AI 行业 15 到 20 条早报, 严格按下面的 JSON schema 输出, 只输出 JSON 本身, 不要任何解释

{{
  "date": "{today}",
  "weekday": "{weekday_cn}",
  "generated_at": "{today} 08:15 (Asia/Shanghai) - GitHub Actions OpenAI Fallback",
  "summary": "200 到 300 字的总览, 覆盖头条 新兴 趋势",
  "stats": {{"total_items": 18, "by_category": {{"headline": 4, "rising": 5, "company": 4, "paper": 2, "industry": 2, "social": 1}}}},
  "items": [
    {{
      "id": "h001",
      "category": "headline",
      "title": "标题 30 到 50 字",
      "summary": "150 到 250 字事实摘要, 5W1H",
      "heat": {{
        "score": 7500,
        "level": "爆",
        "sources": ["Reuters", "第一财经"],
        "breakdown": "原因 1 加 原因 2 加 原因 3"
      }},
      "rising_metrics": {{"hn_show_points": 1500, "github_stars_24h": "+1.8k"}}
    }}
  ],
  "weekly_arc": {{
    "label": "本周脉络",
    "weeks": [
      {{"week": "{iso_year}-W{iso_week:02d}", "date": "{today}", "week_label": "第 {iso_week} 周", "summary": "本周前 7 天加今早的关键事件串联"}}
    ]
  }},
  "monthly_arc": {{
    "label": "本月脉络",
    "months": [
      {{"month": "{today[:7]}", "month_label": "{iso_year} 年 {today[5:7]} 月", "summary": "本月 1 到 7 日主叙事线"}}
    ]
  }}
}}

硬规则
- 18 条 items, 分布 4 5 4 2 2 1
- 5 条 rising 必带 rising_metrics 字段
- 中文文本里禁止 ASCII 双引号嵌入 (用单引号或中文引号)
- heat.level 必须是 爆 热 中 新星 之一
- 标题不能重复, source 不能重复超过 3 次
- JSON 严格合法
"""


def call_openai(prompt: str, api_key: str) -> str:
    """调 OpenAI gpt-4o-mini, 返回 content 字符串"""
    req_body = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "你是 AI 早报编辑, 严格按用户要求的 JSON schema 输出, 只输出 JSON 本身, 不要任何解释"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 8000,
        "response_format": {"type": "json_object"}
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(req_body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read())
    return resp["choices"][0]["message"]["content"]


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[fallback] ERROR: OPENAI_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    today = datetime.date.today().isoformat()
    dt = datetime.datetime.strptime(today, "%Y-%m-%d")
    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][dt.weekday()]
    iso_year, iso_week, _ = dt.isocalendar()

    archive_context = fetch_archive_context()
    print(f"[fallback] archive context: {len(archive_context)} chars", file=sys.stderr)

    prompt = build_prompt(today, weekday_cn, iso_year, iso_week, archive_context)
    print(f"[fallback] prompt: {len(prompt)} chars", file=sys.stderr)

    content = call_openai(prompt, api_key)
    print(f"[fallback] OpenAI returned: {len(content)} chars", file=sys.stderr)

    news = json.loads(content)
    assert news.get("date") == today, f"date mismatch: {news.get('date')} != {today}"
    n_items = len(news.get("items", []))
    assert 14 <= n_items <= 25, f"items count bad: {n_items}"

    # weekly_arc.weeks[0].date 修正为今天
    weeks = news.get("weekly_arc", {}).get("weeks", [])
    if weeks:
        weeks[0]["date"] = today

    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)
    print(f"[fallback] news.json written, items={n_items}", file=sys.stderr)


if __name__ == "__main__":
    main()
