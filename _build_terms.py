#!/usr/bin/env python3
"""2026-06-20 提取当天高频词条并合并到 terms.json"""
import json

with open("/workspace/ai-daily/data/terms.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

new_terms = {
    "John Jumper": {
        "name": "John Jumper",
        "category": "人物",
        "summary": "2024 年诺贝尔化学奖得主,AlphaFold 核心开发者,DeepMind 蛋白质结构预测团队负责人,2026 年 6 月 20 日宣布离开 DeepMind 加入 Anthropic。",
        "detail": "Jumper 加入 Anthropic 被视作该公司发力蛋白质设计与科学推理方向、对标 AlphaFold 的关键落子,也是 48 小时内第二位从 DeepMind 流向 AI 新贵的顶级科学家。",
        "links": []
    },
    "Noam Shazeer": {
        "name": "Noam Shazeer",
        "category": "人物",
        "summary": "2017 年 Transformer 论文《Attention Is All You Need》核心作者,2024 年谷歌以 27 亿美元回购其创立的 Character.AI,2026 年 6 月 18 日加盟 OpenAI 担任架构研究负责人。",
        "detail": "在 OpenAI 的角色定位是探索 Transformer 之后的下一代架构,标志 AI 人才战从工程师挖角升级为架构师战争。",
        "links": []
    },
    "ARD 协议": {
        "name": "ARD 协议 (Agentic Resource Discovery)",
        "category": "协议 / 标准",
        "summary": "代理资源发现协议,2026 年 6 月 18 日由谷歌、微软、Salesforce、Snowflake、ServiceNow 五家联合推出,旨在让企业员工通过单一应用访问所有 AI 工具与服务。",
        "detail": "与 Anthropic 去年发布的 MCP 存在承继关系,但 OpenAI 与 Anthropic 均未加入初始支持方,标志传统软件巨头与 AI 新贵在企业入口主导权上的正式决裂。",
        "links": []
    },
    "GLM-5.2": {
        "name": "GLM-5.2",
        "category": "基础模型",
        "summary": "智谱 2026 年 6 月 17 日凌晨开源的旗舰大模型,1M 上下文,MIT 协议,在 Code Arena 全球盲测中拿下全球可用模型第一。",
        "detail": "已 Day 0 完成与华为昇腾、平头哥、摩尔线程、寒武纪、昆仑芯、沐曦、海光、壁仞等 9 家国产算力平台的推理适配,1M 上下文下 FLOPs 降至 2.9 倍,定位 Anthropic Fable 5 被下架后的国产替代窗口。",
        "links": [{"label": "GitHub", "url": "https://github.com/zai-org/GLM-5"}]
    },
    "MLPerf Training 6.0": {
        "name": "MLPerf Training 6.0",
        "category": "基准 / 评测",
        "summary": "MLCommons 2026 年 6 月发布的最新 AI 训练基准,英伟达 Blackwell 在全部 7 项测试中拿下第一,新增 DeepSeek-V3 671B 和 GPT-OSS-20B 两个 MoE 负载。",
        "detail": "CoreWeave 用 8192 块 GB300 GPU 将 DeepSeek-V3 671B 训练到目标质量耗时 2.02 分钟,微软 Azure 用 GB200 NVL72 在 8192 卡上将 Llama 3.1 405B 训练完成耗时 7.07 分钟,MoE 路线正式进入主流训练基准。",
        "links": []
    },
    "ZPPO 框架": {
        "name": "ZPPO (Zone of Proximal Policy Optimization)",
        "category": "训练方法 / 学术",
        "summary": "英伟达 2026 年 6 月发布于 arXiv 2606.18216 的小模型训练框架,核心理念是让大模型的智慧以题目背景而非正确答案的形式存在,搭配 BCQ/NCQ 双候选改造与提示词回放缓冲区。",
        "detail": "在 Qwen3.5 0.8B 到 9B 学生模型上、27B 教师配置下,0.8B 模型视觉语言能力提升 9.3 个百分点,且对未训练过的纯语言任务也能正向迁移,越小的模型提升越大。",
        "links": [{"label": "arXiv", "url": "https://arxiv.org/abs/2606.18216"}]
    },
    "RTX PRO 6000 Blackwell": {
        "name": "RTX PRO 6000 Blackwell",
        "category": "硬件",
        "summary": "英伟达 2026 年 6 月官方商城上架的旗舰级工作站专业显卡,搭载 GB202 GPU 核心、24064 个 CUDA 核心、96GB GDDR7 ECC 显存、双插槽设计、600W 功耗,官方定价 13250 美元。",
        "detail": "较 2025 年初 8565 美元的常规零售标价上涨 55%,较历史最低 7673 美元上涨约 73%,是 Blackwell 产品线唯一配备 96GB 显存的型号,主要面向大模型本地训练与高精度渲染。",
        "links": []
    },
    "宇树人形机器人": {
        "name": "宇树 (Unitree) 人形机器人",
        "category": "机器人 / 硬件",
        "summary": "中国人形机器人头部厂商,德银 2026 年 6 月研报中将其列为行业领跑者,中国 2026 年人形机器人出货量预计翻倍至 4 万台。",
        "detail": "德银将宇树领跑归因于价格可及性提升、激进销售策略与 IPO 扩张三重驱动;全球 2026 出货量约 5 万台,德银预测 2050 年达 700 万台。",
        "links": []
    },
    "欧盟 AI 法案 Article 50": {
        "name": "欧盟 AI 法案 Article 50",
        "category": "政策 / 监管",
        "summary": "欧盟 AI 法案的透明度义务条款,2026 年 8 月 2 日全面生效,要求所有 AI 生成的图像、文本、音频、视频必须携带机器可读标记。",
        "detail": "义务落在输出 AI 内容的「产品方」而非底层模型厂商,即使仅调用 OpenAI API 也算 provider;违规最高罚款 1500 万欧元或全球营收 3%,中小企业的简化机制下罚款仍具致命性,合规咨询市场价 3000-8000 欧元。",
        "links": []
    },
    "OpenClaw": {
        "name": "OpenClaw",
        "category": "Agent / 开源项目",
        "summary": "GitHub 2026 年 6 月爆款个人 AI 助理项目,376,307 Star 登顶月榜,定位「Any OS. Any Platform.」,支持 Discord、Telegram、WhatsApp、Slack 等多平台接入。",
        "detail": "用户可在聊天软件里直接下达指令如「整理桌面截图按日期分类」,OpenClaw 自动扫描识别、创建文件夹、移动文件;同期 Superpowers(21.6 万 Star)、Hermes Agent 等 Agent 框架项目持续爆发,标志本地部署、隐私安全、团队协同成新趋势。",
        "links": [{"label": "GitHub", "url": "https://github.com/openclaw/openclaw"}]
    }
}

merged = {**new_terms, **existing}

with open("/workspace/ai-daily/data/terms.json", "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"merged: {len(new_terms)} new + {len(existing)} existing = {len(merged)} total")
