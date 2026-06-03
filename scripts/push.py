#!/usr/bin/env python3
"""
push.py — 微信推送模块(双通道)
支持:
  - Server 酱 (推荐个人微信): 通过 SCT_SENDKEY 环境变量启用
  - 企业微信群机器人: 通过 WECOM_WEBHOOK 环境变量启用

环境变量(都不设 = 跳过推送,只打日志):
  SCT_SENDKEY     Server 酱 SendKey
  WECOM_WEBHOOK   企业微信群机器人 Webhook URL
  PUSH_TOP_N      推送消息里包含的头条条数(默认 5)
  PUBLIC_URL      早报公网链接(显示在推送里)
"""
import os, sys, json, urllib.request, urllib.parse, urllib.error

PUBLIC_URL = os.environ.get("PUBLIC_URL", "https://fb023nb9lcbx.space.minimaxi.com")
TOP_N = int(os.environ.get("PUSH_TOP_N", "5"))


def build_digest(news):
    """把 news.json 压成推送友好的纯文本"""
    date = news.get("date", "")
    weekday = news.get("weekday", "")
    summary = news.get("summary", "")
    items = news.get("items", [])[:TOP_N]
    lines = []
    lines.append(f"🌐 AI 早报 · {date} {weekday}")
    lines.append("")
    lines.append(summary)
    lines.append("")
    for i, it in enumerate(items, 1):
        cat = it.get("category", "")
        cat_emoji = {"headline":"🔥","company":"🏢","paper":"📄","industry":"🏛","social":"💬"}.get(cat, "•")
        title = it.get("title", "")
        hot = it.get("hot", 0)
        lines.append(f"{i}. {cat_emoji} {title}")
    lines.append("")
    lines.append(f"👉 看完整版(含词条百科 + 周月脉络):{PUBLIC_URL}")
    return "\n".join(lines)


def push_server_chan(sendkey, digest, news):
    """Server 酱推送,带图文 + 跳转按钮"""
    if not sendkey:
        return False, "sendkey empty"
    title = f"AI 早报 · {news.get('date','')}"
    desp = digest.replace("\n", "\n\n")
    data = urllib.parse.urlencode({"title": title, "desp": desp}).encode("utf-8")
    url = f"https://sctapi.ftqq.com/{sendkey}.send"
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return True, body[:200]
    except urllib.error.URLError as e:
        return False, str(e)


def push_wecom(webhook, digest, news):
    """企业微信群机器人推送(markdown)"""
    if not webhook:
        return False, "webhook empty"
    md = f"""# 🌐 AI 早报 · {news.get('date','')} {news.get('weekday','')}

> {news.get('summary','')}

{digest}

[👉 查看完整版(支持词条百科 + 周月脉络)]({PUBLIC_URL})
"""
    payload = json.dumps({"msgtype": "markdown", "markdown": {"content": md}}).encode("utf-8")
    try:
        req = urllib.request.Request(webhook, data=payload, method="POST",
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return True, body[:200]
    except urllib.error.URLError as e:
        return False, str(e)


def main():
    news_path = os.path.join(os.path.dirname(__file__), "..", "data", "news.json")
    if not os.path.exists(news_path):
        print("[push] news.json not found, skip")
        return
    with open(news_path, "r", encoding="utf-8") as f:
        news = json.load(f)
    digest = build_digest(news)

    print(f"[push] digest ready, {len(digest)} chars")
    print("--- digest preview ---")
    print(digest)
    print("--- end digest ---")

    sct = os.environ.get("SCT_SENDKEY", "").strip()
    if sct:
        ok, msg = push_server_chan(sct, digest, news)
        print(f"[push] server-chan: ok={ok}, msg={msg}")
    else:
        print("[push] SCT_SENDKEY 未设置,跳过 Server 酱")

    wecom = os.environ.get("WECOM_WEBHOOK", "").strip()
    if wecom:
        ok, msg = push_wecom(wecom, digest, news)
        print(f"[push] wecom: ok={ok}, msg={msg}")
    else:
        print("[push] WECOM_WEBHOOK 未设置,跳过企业微信")


if __name__ == "__main__":
    main()
