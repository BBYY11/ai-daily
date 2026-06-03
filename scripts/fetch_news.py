#!/usr/bin/env python3
"""
fetch_news.py — AI 早报信源抓取与归一化
输入: 无(或 CLI 参数 --date YYYY-MM-DD)
输出: /workspace/ai-daily/data/news.json + terms.json

设计原则:
- 单文件,无外部依赖(只用 stdlib),不依赖任何付费 API
- 信源用 web_search 风格的关键字查询(脚本本身只生成查询清单,实际搜索由上层 agent 调度)
- 词条从出现的高频专有名词自动生成,带默认值,后续人工/agent 增补
"""
import json, re, datetime, os, sys
from collections import Counter

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# === 信源池 ===
# 三类:头部(established)/ 新兴(rising) / 学术(paper) / 行业(industry) / 声音(social)
SOURCE_POOL = {
    "headline": [
        # 英文头部官方
        "OpenAI blog", "Anthropic news", "Google DeepMind blog", "NVIDIA newsroom",
        "Meta AI blog", "Mistral AI blog", "xAI blog",
        # 英文头部媒体
        "TechCrunch AI", "The Verge AI", "Wired AI", "MIT Technology Review AI",
        "VentureBeat AI", "IEEE Spectrum AI", "The Decoder", "Ars Technica AI",
        # 中文头部
        "机器之心", "量子位", "新智元", "智东西", "PaperWeekly", "36氪 AI",
        "澎湃科技", "虎嗅 AI", "IT之家 AI", "钛媒体 AI",
    ],
    # === 新增:新兴应用 / 新模型 / 开源新星 ===
    "rising": [
        # Hacker News
        "Hacker News top AI this week",
        "HN Show HN AI tool new",
        # Reddit
        "Reddit r/MachineLearning top week",
        "Reddit r/LocalLLaMA top",
        "Reddit r/singularity top",
        # GitHub Trending
        "GitHub trending AI this week",
        "GitHub trending LLM repo new",
        "GitHub trending agent framework",
        "GitHub stars new AI project",
        # Product Hunt
        "Product Hunt AI top today",
        "Product Hunt AI launches this week",
        # X/Twitter
        "X trending AI demo new",
        "X AI model release new",
        "X open source LLM announcement",
        # 开源模型发布
        "Hugging Face new model trending",
        "Hugging Face spaces trending AI",
        "new open source LLM release this week",
        "new SOTA benchmark AI",
        # 视频/演示
        "AI demo viral this week",
        "AI agent launch new",
    ],
    "paper": [
        "arXiv cs.AI today", "arXiv cs.CL today",
        "Hugging Face daily papers", "papers with code trending",
        "DeepMind publications", "OpenAI publications",
    ],
    "social": [
        "Hacker News top AI", "Reddit r/MachineLearning top",
        "Polymarket AI prediction", "X AI trending",
    ],
}

# === 热度信号来源映射 ===
# 每条新闻可以标注它主要在哪些平台被讨论
# cron agent 会根据实际抓取情况填入 heat_sources 字段
HEAT_SOURCES = {
    "hn":     {"label": "HN",     "color": "#ff6a1a", "weight": 1.0},
    "x":      {"label": "X",      "color": "#4adfd1", "weight": 1.2},
    "github": {"label": "GitHub", "color": "#d65cd1", "weight": 1.1},
    "reddit": {"label": "Reddit", "color": "#ffb800", "weight": 0.9},
    "ph":     {"label": "PH",     "color": "#da552f", "weight": 1.0},
    "media":  {"label": "媒体",   "color": "#9a9890", "weight": 0.7},
    "paper":  {"label": "论文",   "color": "#4adfd1", "weight": 0.8},
}

SEARCH_QUERIES = []
for cat, sources in SOURCE_POOL.items():
    for s in sources:
        SEARCH_QUERIES.append(f"{s} {datetime.date.today().isoformat()}")

# === 词条分类与默认值 ===
TERM_CATEGORIES = {
    # 基础模型
    "GPT": "基础模型", "Claude": "基础模型", "Gemini": "基础模型",
    "Llama": "基础模型", "Mistral": "基础模型", "DeepSeek": "基础模型",
    "Nemotron": "基础模型", "Qwen": "基础模型", "Grok": "基础模型",
    "V4-Pro": "基础模型", "V4": "基础模型",
    # 硬件
    "H100": "硬件", "H200": "硬件", "B200": "硬件",
    "Blackwell": "硬件", "Vera Rubin": "硬件", "Vera": "硬件",
    "Rubin": "硬件", "MI350x": "硬件", "HBM": "硬件",
    "RTX Spark": "硬件", "N1X": "硬件", "GPU": "硬件", "TPU": "硬件",
    "FPGA": "硬件", "ASIC": "硬件",
    # 机器人
    "Figure": "机器人", "GR00T": "机器人", "Isaac": "机器人",
    "宇树": "机器人", "自由度": "机器人", "DoF": "机器人",
    "具身智能": "机器人", "人形机器人": "机器人",
    # Agent
    "Agent": "Agent", "MCP": "Agent", "Context-ReAct": "Agent",
    "RAG": "Agent", "BrowseComp": "评测",
    # 治理 / 监管
    "BIS": "监管", "实体清单": "监管",
    "受信任访问": "AI 治理", "红队": "AI 安全", "Biodefense": "AI 治理",
    # 评测 / 指标
    "AUROC": "评测指标", "MMLU": "评测基准", "BrowseComp": "评测基准",
    # 商业模式
    "ARR": "商业指标", "Series H": "投融资", "估值": "投融资",
    "GW": "能源", "数据中心": "基础设施", "AI 工厂": "基础设施",
    "Token": "商业模式", "token 经济": "商业模式",
    # 算力分类
    "通算": "算力分类", "智算": "算力分类", "超算": "算力分类",
    # 数学 / 学术名词
    "Erdős": "数学", "单位距离问题": "数学", "反直觉": "方法论",
    "RTL": "硬件", "FP16": "数值精度", "FP32": "数值精度",
    "归一化熵": "概率", "语义自洽": "AI 评估",
    # 预测市场
    "Polymarket": "预测市场", "流动性池": "金融",
    # 耐力测试
    "Figure 03": "机器人", "耐力测试": "机器人",
}

TERM_DEFAULT_TPL = {
    "name": "",
    "category": "通用",
    "summary": "(待补充)",
    "detail": "(待补充,可在 terms.json 中增补)",
    "links": []
}


def slug(s):
    return s.strip()


def merge_terms(existing, new_keys):
    """合并已有词条与新出现的高频词"""
    out = dict(existing)
    for k in new_keys:
        if k not in out:
            tpl = dict(TERM_DEFAULT_TPL)
            tpl["name"] = k
            tpl["category"] = TERM_CATEGORIES.get(k, "通用")
            out[k] = tpl
    return out


def build_seed_news(date_str, weekday):
    """生成空骨架,实际数据由上层 agent 填入后写回"""
    return {
        "date": date_str,
        "weekday": weekday,
        "generated_at": f"{date_str} 08:00 (Asia/Shanghai)",
        "summary": "(待生成)",
        "stats": {"total_items": 0, "by_category": {}},
        "items": [],
        "weekly_arc": {"label": "本周脉络", "weeks": []},
        "monthly_arc": {"label": "本月脉络", "months": []}
    }


def archive_today(date_str):
    """把 news.json 归档到 archive/YYYY-MM-DD.json + 重建 archive/index.json 清单"""
    news_path = os.path.join(DATA_DIR, "news.json")
    archive_dir = os.path.join(DATA_DIR, "archive")
    os.makedirs(archive_dir, exist_ok=True)

    # 1. 如果有今天的 news.json,写入当天快照
    if os.path.exists(news_path):
        day_path = os.path.join(archive_dir, f"{date_str}.json")
        with open(news_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        with open(day_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[archive] {day_path} saved")
    else:
        print(f"[archive] news.json not found, skip today snapshot")

    # 2. 扫描整个 archive 目录,重建 index.json(保证任何手写入的快照也能被索引)
    days = []
    for fn in sorted(os.listdir(archive_dir), reverse=True):
        if not fn.endswith(".json") or fn == "index.json":
            continue
        fp = os.path.join(archive_dir, fn)
        try:
            with open(fp, "r", encoding="utf-8") as f:
                d = json.load(f)
            items = d.get("items", [])
            days.append({
                "date": d.get("date", fn[:-5]),
                "weekday": d.get("weekday", ""),
                "summary": d.get("summary", ""),
                "total": len(items),
                "rising": sum(1 for i in items if i.get("category") == "rising"),
                "headline": sum(1 for i in items if i.get("category") == "headline"),
            })
        except Exception as e:
            print(f"[archive] skip {fn}: {e}")
    days.sort(key=lambda x: x["date"], reverse=True)
    index_path = os.path.join(archive_dir, "index.json")
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({"days": days}, f, ensure_ascii=False, indent=2)
    print(f"[archive] {index_path} rebuilt, {len(days)} days total")


def main():
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.date.today().isoformat()
    dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    weekday_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][dt.weekday()]

    news_path = os.path.join(DATA_DIR, "news.json")
    terms_path = os.path.join(DATA_DIR, "terms.json")

    # 读取已有词条
    if os.path.exists(terms_path):
        with open(terms_path, "r", encoding="utf-8") as f:
            existing_terms = json.load(f)
    else:
        existing_terms = {}

    # 生成 search queries 文件,供上层 agent 参考
    with open(os.path.join(DATA_DIR, "search_queries.txt"), "w", encoding="utf-8") as f:
        for q in SEARCH_QUERIES:
            f.write(q + "\n")

    print(f"[fetch_news] date={date_str} ({weekday_cn})")
    print(f"[fetch_news] search_queries.txt 已生成 ({len(SEARCH_QUERIES)} 条)")
    print(f"[fetch_news] existing terms: {len(existing_terms)}")

    # 归档当天的 news.json(如果存在)
    archive_today(date_str)


if __name__ == "__main__":
    main()
