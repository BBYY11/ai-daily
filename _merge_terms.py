#!/usr/bin/env python3
"""合并 2026-06-22 高频词条到 terms.json,保留已有项,新增 10 个。"""
import json

with open("data/terms.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

new_terms = {
    "autoarxiv": {
        "name": "autoarxiv",
        "category": "工具 / 产品",
        "summary": "alphaXiv 2026 年 6 月推出的 arXiv 论文自动复现功能,改 URL 即可让 AI 智能体自主 clone 代码仓库、修复环境、运行最小化复现并估算完整算力。",
        "detail": "演示中智能体把原本需要 4 张 H100、15 分钟完成的实验压缩到单卡 LoRA 40 步即可跑通,标志 AI 读论文从「总结」走向「跑通」的下一阶段。",
        "links": []
    },
    "Slackbot AI Agent": {
        "name": "Slackbot AI Agent",
        "category": "产品 / 发布",
        "summary": "Salesforce 2026 年 6 月 21 日发布的企业级工作流智能体,自动处理消息优先级、安排会议、起草文档,与 Agentforce 生态无缝衔接。",
        "detail": "同日 Salesforce 宣布 2026 年向 Anthropic 采购 3 亿美元 Claude Token,贝尼奥夫称「这些编码代理太棒了」。",
        "links": []
    },
    "Databricks": {
        "name": "Databricks",
        "category": "公司 / 资本",
        "summary": "2026 年 6 月 21 日铅笔道披露,Databricks 启动新一轮融资,目标估值最高 1750 亿美元,有望成为一级市场最后一家活跃的巨型 AI 独角兽。",
        "detail": "公司核心业务是企业级数据湖与 AI 模型训练基础设施,被视为企业 AI 数据层隐形冠军。",
        "links": []
    },
    "AI+消费": {
        "name": "AI+消费 实施意见",
        "category": "政策 / 监管",
        "summary": "商务部联合发改委、工信部等八部门 2026 年 6 月联合印发的《关于加快「人工智能+消费」发展的实施意见》,推动 AI 手机、AI PC、智能眼镜、智能汽车等终端加快迭代。",
        "detail": "国金证券看好 AI+消费级 3D 打印、AI+眼镜两个细分方向,认为「AI+消费」是当下赔率较好的应用赛道。",
        "links": []
    },
    "OpenClaw": {
        "name": "OpenClaw",
        "category": "开源项目",
        "summary": "GitHub 6 月霸榜月榜项目,Star 数 376,307,定位「Any OS. Any Platform.」个人 AI 助理,支持 Discord、Telegram、WhatsApp、Slack 多平台接入。",
        "detail": "可在聊天软件中执行代码、管理文件、控制设备,代表 Agent 生态从「写代码」进化到「自主完成任务」的标志。",
        "links": []
    },
    "Superpowers": {
        "name": "Superpowers",
        "category": "开源项目",
        "summary": "obra/superpowers,GitHub Star 数 215,946,定位 Agent Skill 即插即用框架,提供 50+ 预置技能。",
        "detail": "原生支持 Claude Code、Codex 等主流 Agent,提供 Skill 标准格式与社区贡献机制。",
        "links": []
    },
    "Hermes Agent": {
        "name": "Hermes Agent",
        "category": "开源项目",
        "summary": "NousResearch 出品的多模态 AI Agent 框架,GitHub Trending 6 月榜第三名。",
        "detail": "依托 NousResearch 在 Hermes 系列模型上的积累,定位多模态 Agent 框架,与 OpenClaw、Superpowers 共同构成 Agent 生态三大基础设施。",
        "links": []
    },
    "mem0": {
        "name": "mem0 (Memory Layer)",
        "category": "开源项目",
        "summary": "mem0ai/mem0,定位 AI Agent 的通用记忆层,2026 年 4 月新算法 BEAM 1M 64.1、LongMemEval 94.8,GitHub 当日登顶。",
        "detail": "核心升级:单次 ADD-only 提取 + 实体链接 + 多信号(语义/BM25/实体)检索融合 + 时序推理。同步上线 agent 自主注册 API Key、Sign up as an agent 工作流与 skills 标准集成。",
        "links": []
    },
    "DAAAM": {
        "name": "DAAAM 时空记忆框架",
        "category": "训练方法 / 学术",
        "summary": "MIT 团队 2026 年 6 月发布于 arXiv:2512.00565 的机器人长期记忆框架,层次化 4D 场景图 + 双步优化提速 10 倍。",
        "detail": "在 OC-NaVQA 基准测试中,DAAAM 比 SOTA 在问题回答准确率上提升 53.6%,位置误差降低 21.9%,时间误差降低 21.6%。",
        "links": []
    },
    "神经形态软体机器人基准": {
        "name": "软体身体 + 神经形态大脑",
        "category": "训练方法 / 学术",
        "summary": "苏黎世联邦理工 Elisa Donati 团队 2026 年 6 月在 Nature Machine Intelligence 发表的具身智能新范式,软体身体+神经形态计算结合。",
        "detail": "同步开源模块化物理机器人基准测试框架,评估指标聚焦适应能力、稳健性、能源效率与人机协作安全性。",
        "links": []
    },
    "HBM ASP": {
        "name": "HBM (High Bandwidth Memory) ASP",
        "category": "硬件 / 芯片",
        "summary": "高带宽内存平均售价,摩根士丹利预测 2027 财年同比有望 +50%,2026/2027/2028 财年 HBM 市场总规模将分别达 560 亿/1160 亿/1680 亿美元。",
        "detail": "TrendForce 预计 26Q2 通用 DRAM 合约价上涨 58-63%,NAND 合约价上涨 70-75%,英伟达 Vera CPU 内存减配印证 AI 生态关键瓶颈。",
        "links": []
    }
}

existing.update(new_terms)

with open("data/terms.json", "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"✅ terms.json 已合并:新增 {len(new_terms)} 个,合计 {len(existing)} 个")
