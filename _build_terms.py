#!/usr/bin/env python3
"""2026-06-25 提取当天高频词条并合并到 terms.json"""
import json

with open("/workspace/ai-daily/data/terms.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

new_terms = {
    "Claude Tag": {
        "name": "Claude Tag",
        "category": "产品",
        "summary": "Anthropic 2026 年 6 月 23 日在 Slack 上线的群聊 AI 协作助理,底层跑 Opus 4.8,Anthropic 内部 65% 代码已由 Claude Tag 内部版本生成。",
        "detail": "Karpathy 评价为「LLM 交互的第三次重大重新设计」——第一次是访问网站,第二次是本地应用,第三次是「独立、持久、异步运行,拥有组织级工具和上下文的实体」;30 天内将逐步替换 Claude in Slack。",
        "links": [{"label": "Claude.com", "url": "https://claude.com/product/tag"}]
    },
    "Jalapeño 芯片": {
        "name": "Jalapeño",
        "category": "硬件",
        "summary": "OpenAI 与博通 2026 年 6 月 24 日联合发布的首款定制 AI 推理 ASIC 芯片,从架构设计到流片仅用 9 个月,采用 OpenAI 自研架构+博通 Tomahawk 网络。",
        "detail": "工程样片已在实验室以量产目标频率和功耗运行 GPT-5.3、Codex、Spark 等工作负载,每瓦性能将优于当前最先进水平;标志 OpenAI 正式从纯软件层迈入软硬一体,直接对标谷歌 TPU 路径。",
        "links": []
    },
    "灵晟超算": {
        "name": "灵晟 (LineShine) 超算",
        "category": "硬件",
        "summary": "国家超算深圳中心研制的 E 级超算系统,2026 年 6 月 23 日在德国汉堡 ISC 2026 大会以 2.19 EFLOPS 登顶全球 TOP500 榜首,自 2017 年神威·太湖之光后中国超算时隔九年重回榜首。",
        "detail": "全球首台持续性能突破 2 EFLOPS 的超算系统,大幅领先美国 El Capitan(1.809 EFLOPS);采用全 CPU 架构(摒弃 GPU 异构),搭载自研 LX2 处理器(国产 HBM 内存带宽提升 10 倍)、自研灵启高速互联(支持 10 万节点 200 万端口组网),能效比 51 GFLOPS/W。",
        "links": []
    },
    "Vera Rubin 平台": {
        "name": "Vera Rubin 平台",
        "category": "硬件",
        "summary": "英伟达 2026 年年度股东大会上黄仁勋定位为「英伟达历史上最重要的产品之一」,由 Rubin GPU + Vera CPU + NVLink + Spectrum-X + InfiniBand + BlueField 组成完整 AI 工厂平台。",
        "detail": "Vera CPU 是专为智能体打造的新品类,智能体生活在纳秒级计算世界,Vera CPU 通过避免 GPU 闲置来提升 AI 工厂收入;Vera Rubin 已全面量产,主要模型构建商、公有云、AI 云、超大规模客户均已着手部署。",
        "links": []
    },
    "Jonas Adler": {
        "name": "Jonas Adler",
        "category": "人物",
        "summary": "谷歌 Gemini 大模型核心研究员,2026 年 6 月 25 日与 Alexander Pritzel 共同宣布转投 Anthropic。",
        "detail": "与 Pritzel 是 Gemini 强化学习与训练系统的关键负责人,二人转会是 Shazeer 加盟 OpenAI、Jumper 转投 Anthropic 后 48 小时第三位 DeepMind 顶级人才外流,标志 AI 人才战从工程师挖角升级为架构师与团队负责人争夺。",
        "links": []
    },
    "Alexander Pritzel": {
        "name": "Alexander Pritzel",
        "category": "人物",
        "summary": "谷歌 Gemini 大模型强化学习与训练系统关键负责人,2026 年 6 月 25 日与 Jonas Adler 共同宣布转投 Anthropic。",
        "detail": "Gemini 训练基础设施的奠基人之一,加入 Anthropic 后将参与 Claude 下一代训练系统设计,直接强化 Anthropic 在长程 RL 与 Agent 训练上的能力。",
        "links": []
    },
    "反射性遮蔽 (RM)": {
        "name": "反射性遮蔽 (Reflective Masking)",
        "category": "训练方法 / 学术",
        "summary": "马里兰大学等 6 机构 2026 年 6 月在 arXiv(2606.16700)发布的论文,让遮蔽扩散模型(MDM)能主动判断已填入的词是否正确并重新打 MASK 预测,实现「边写边改」。",
        "detail": "配套的「历史参考」(HR)机制维护每个位置压缩历史状态摘要,完整方法包含「历史嵌入旋转」(HER)给不同时间步的历史信息添加时间标记;在 LLaDA 上 MBPP 代码生成提升 11.4%(相对基线 +8.8 个百分点),3 个任务 5 小时 H100 训练完成,代码已开源。",
        "links": [{"label": "arXiv", "url": "https://arxiv.org/abs/2606.16700"}]
    },
    "CoD 训练框架": {
        "name": "CoD (Connect the Dots)",
        "category": "训练方法 / 学术",
        "summary": "阿里巴巴 2026 年 6 月在 arXiv(2606.20002)发布的训练框架,目标让 AI 学会在长周期任务中积累经验并迁移到下一个任务。",
        "detail": "在 Qwen3-8B-Instruct 上,FrozenLake-Obscure 第一题成功率从 18% 提升至 45%,第四题从 28% 跃升至 76%,且能力可泛化到完全没见过的环境;训练时引入位置分组的细粒度信用分配,解决「当前任务得分高但对未来任务无用」的长期 RL 难题。",
        "links": [{"label": "arXiv", "url": "https://arxiv.org/abs/2606.20002"}]
    },
    "Qwen-AgentWorld": {
        "name": "Qwen-AgentWorld",
        "category": "基础模型",
        "summary": "阿里千问 2026 年 6 月 24 日发布的首个原生语言世界模型(LWM),将环境建模作为从 CPT 阶段起的核心训练目标,覆盖文本类与 GUI 类共 7 大 Agent 交互领域。",
        "detail": "单一模型同时覆盖文本类环境(MCP、Search、Terminal、SWE)与 GUI 类环境(Web、OS、Android),同步发布 AgentWorldBench 评测基准,每条测试样本均配备真实环境执行所得观测数据;为 Agent RL 训练提供统一可扩展的世界模型。",
        "links": []
    },
    "MXFP 路由": {
        "name": "模型路由 (Model Router)",
        "category": "Agent / 工具",
        "summary": "2026 年上半年爆发的新工具赛道,让企业根据任务灵活切换 AI 模型以压缩算力开支,Not Diamond 等代表性公司过去半年市场需求爆发式增长。",
        "detail": "使用 Anthropic 老旧低价模型可较顶配模型节省 20%-40% 成本;同类玩家还包括 Martian AI、Factory、Portkey、OpenRouter、CodeStrap 与 Vercel AI Gateway;Vercel AI Gateway 数据显示 DeepSeek 在 5 月份的 Token 调用量占比从不足 1% 飙升至 17%,但收入占比仅约 1%。",
        "links": []
    },
    "Meta MCI 事件": {
        "name": "Meta MCI 数据治理事件",
        "category": "政策 / 监管",
        "summary": "Meta 2026 年 6 月 23 日被曝光的内部 AI 训练项目 Model Capability Initiative 数据权限错配事件,约 4.5 万张数据表一度对内部人员开放,涉及员工键盘、鼠标、屏幕内容记录。",
        "detail": "Meta 首席信息官 Candace Kao 内部备忘录承认「严重违反公司数据治理原则」,承诺 90 天独立第三方审计;这是 Meta 在 AI 训练数据合规上的第二次翻车(4 月曾因公共 GitHub 仓库误传 50000 条用户对话数据集被曝光),硅谷已开始广泛讨论「内部数据是否可用于训练」。",
        "links": []
    }
}

merged = {**new_terms, **existing}

with open("/workspace/ai-daily/data/terms.json", "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"merged: {len(new_terms)} new + {len(existing)} existing = {len(merged)} total")
