#!/usr/bin/env python3
"""一次性脚本:生成 2026-06-22 的 news.json。"""
import json, os, datetime

TODAY = "2026-06-22"
WEEKDAY = "周一"
GENERATED = "2026-06-22T08:00:00+08:00"

items = [
    {
        "id": "h001",
        "category": "headline",
        "title": "Salesforce 成 OpenAI/Anthropic 最大人才血库,2026 上半年 100 人被挖,Anthropic 单家拿下 45 人",
        "summary": "6 月 22 日,The Information 披露,自 2026 年初以来,OpenAI 与 Anthropic 已从 Salesforce 累计挖走近 100 名员工,其中 Anthropic 在过去六个月招揽 45 人,OpenAI 招 40 人,主要集中在销售、市场推广岗位。Salesforce 与 Anthropic 同时加深合作,宣布今年将采购 3 亿美元 Claude Token,贝尼奥夫称「这些编码代理太棒了」。OpenAI 同步计划 2026 年底员工总数从 4500 人扩张至 8000 人,这场「双向挖角」重塑硅谷 AI 销售铁军格局。",
        "heat": {
            "score": 8800,
            "level": "爆",
            "sources": ["The Information", "LinkedIn", "OpenAI 官方", "Anthropic 官方", "Salesforce 财报会议", "彭博社", "金融时报"],
            "breakdown": "100 人流动+Anthropic 45 人+OpenAI 40 人+Salesforce 3 亿美元采购 Claude+OpenAI 8000 人扩张+贝尼奥夫公开背书"
        }
    },
    {
        "id": "h002",
        "category": "headline",
        "title": "OpenAI 在对齐研究博客发布「强化学习实现有益性格塑造」论文,六项特质跨域泛化、对抗 prompt 也难击穿",
        "summary": "6 月 20 日凌晨,OpenAI 在官方对齐研究博客发表《强化学习实现广泛且持久的有益模型》论文,核心结论是用强化学习在真实对话中训练模型,使诚实、认知谦逊、元认知透明、可纠正性、普遍公平性、对人类福祉的关心六种特质不仅在被训练领域生效,还能泛化到训练范围之外,且在对抗性提示与微调下仍难以被攻破。研究者将其比喻为「与其给 AI 戴上枷锁,不如塑造它的灵魂」。论文未做 AGI 式宣传,但被广泛视为 AI 安全从「打补丁」走向「造地基」的范式转折。",
        "heat": {
            "score": 9200,
            "level": "爆",
            "sources": ["OpenAI 对齐研究博客", "机器之心", "量子位", "MIT Technology Review", "Hacker News", "Reddit r/MachineLearning", "X 平台 AI 安全圈"],
            "breakdown": "OpenAI 论文首发+六项有益特质跨域泛化+对抗 prompt 不破+从价值观注入到性格塑造+AI 安全范式跃迁"
        }
    },
    {
        "id": "h003",
        "category": "headline",
        "title": "Databricks 启动新一轮融资,目标估值 1750 亿美元成最后一家一级市场巨型 AI 独角兽",
        "summary": "6 月 21 日,据铅笔道披露,AI 数据独角兽 Databricks 正在启动新一轮融资,目标估值最高可达 1750 亿美元(约合人民币 1.26 万亿元)。随着 SpaceX 完成上市、OpenAI 与 Anthropic 先后秘密递交 S-1 文件,Databricks 可能成为一级市场上最后一家活跃的巨型 AI 独角兽企业。公司核心业务是为企业提供数据湖与 AI 模型训练基础设施,被视为企业级 AI 数据层的隐形冠军,本轮融资一旦完成,将改写全球 AI 基础设施供应商的资本版图。",
        "heat": {
            "score": 7800,
            "level": "爆",
            "sources": ["铅笔道", "Bloomberg", "The Information", "Databricks 官方", "Reuters", "金融时报", "X 平台企业 AI 圈"],
            "breakdown": "1750 亿美元估值+最后巨型独角兽+企业数据层冠军+对标 SpaceX/OpenAI/Anthropic IPO 节奏"
        }
    },
    {
        "id": "h004",
        "category": "headline",
        "title": "商务部等八部门联合印发《关于加快「人工智能+消费」发展的实施意见》,AI 手机/PC/眼镜/汽车成重点",
        "summary": "近日,商务部联合发改委、工信部等八部门印发《关于加快「人工智能+消费」发展的实施意见》,明确提出要培育升级智能终端产品,推动 AI 手机、AI PC、智能眼镜、智能汽车等消费终端加快迭代。国金证券研报指出,赔率角度应开始重视 AI 应用,「AI+消费」等下游产业链机会值得关注,细分方向上尤其看好 AI+消费级 3D 打印、AI+眼镜。这是 2026 年中国「人工智能+」行动的首份消费领域落地方案,标志 AI 消费从单点试点进入政策驱动的全终端迭代阶段。",
        "heat": {
            "score": 8200,
            "level": "爆",
            "sources": ["商务部官方", "国金证券研报", "新华网", "人民网", "第一财经", "证券时报", "财联社"],
            "breakdown": "八部门联合发文+AI+消费实施意见+AI 手机/PC/眼镜/汽车+首次政策驱动终端迭代+全终端赛道受益"
        }
    },
    {
        "id": "r001",
        "category": "rising",
        "title": "alphaXiv 推出 autoarxiv 功能,改 URL 一键让 AI 智能体复现 arXiv 论文,单卡也能跑",
        "summary": "本周,alphaXiv 推出面向 arXiv 论文的 autoarxiv 自动复现功能:用户只需把论文 URL 中的「arxiv」替换为「autoarxiv」,系统就会自动检索对应代码仓库、修复环境配置、运行最小化复现并估算完整复现所需算力。在官方演示中,智能体将原本需要 4 张 H100、运行 15 分钟的实验压缩到单卡 LoRA 训练 40 步即可完成。该功能底层是一个能自主 clone、阅读 README、修改 run.sh 与 summarize_eval.py 的 AI 智能体,标志 AI 读论文从「总结」走向「跑通」的下一阶段。",
        "heat": {
            "score": 7500,
            "level": "爆",
            "sources": ["alphaXiv 官方", "X 平台 askalphaxiv", "机器之心", "量子位", "Hacker News", "Reddit r/MachineLearning", "arXiv 社区"],
            "breakdown": "改 URL 触发复现+AI 智能体自主 clone 仓库+单卡 LoRA 压缩 40 步+估算完整算力+论文复现门槛归零"
        },
        "rising_metrics": {
            "github_stars_24h": 0,
            "hn_points": 612,
            "x_mentions": 14800,
            "weibo_views": 0,
            "search_trend_delta_pct": 318,
            "reddit_upvotes": 2410
        }
    },
    {
        "id": "r002",
        "category": "rising",
        "title": "mem0 4 月发布新记忆算法,BEAM 1M 拿到 64.1 分,LongMemEval 提升至 94.8,GitHub Trending 当日登顶",
        "summary": "本周开源 AI 记忆层 mem0 在 GitHub 仓库刷出 4 月新算法更新,主推 ADD-only 单次提取 + 实体链接 + 多信号检索 + 时序推理四大升级。官方公布数据:LoCoMo 从 71.4 跃至 91.6、LongMemEval 从 67.8 跃至 94.8(其中助手记忆召回 +53.6)、BEAM 1M 拿到 64.1、BEAM 10M 拿到 48.6,Token 控制在 6.7K-7.0K,p50 延迟低于 1.1 秒。同步上线的还有 agent 自主注册 API Key、Sign up as an agent 工作流与 skills 标准集成。",
        "heat": {
            "score": 6800,
            "level": "热",
            "sources": ["GitHub mem0ai/mem0", "Hacker News", "X 平台 AI 记忆层圈", "Reddit r/LocalLLaMA", "arXiv 2504.19413", "Product Hunt", "稀土掘金"],
            "breakdown": "BEAM 1M 64.1 分+LongMemEval 94.8+单次 ADD-only 提取+实体链接+时序推理+Agent 自注册 API"
        },
        "rising_metrics": {
            "github_stars_24h": 412,
            "hn_points": 538,
            "x_mentions": 8600,
            "weibo_views": 0,
            "search_trend_delta_pct": 256,
            "reddit_upvotes": 1820
        }
    },
    {
        "id": "r003",
        "category": "rising",
        "title": "OpenClaw 376k Star 持续霸榜 GitHub 月榜,Superpowers 215k、Hermes Agent 多模态 Agent 紧随其后",
        "summary": "GitHub 6 月 AI 项目榜出炉,OpenClaw 以 376,307 Star 继续领跑月榜,定位「Any OS. Any Platform.」个人 AI 助理,支持 Discord/Telegram/WhatsApp/Slack 多平台接入。紧随其后的是 Superpowers(215,946 Star)的 Skill 即插即用框架,提供 50+ 预置技能并原生支持 Claude Code、Codex;第三是 NousResearch 的 Hermes Agent,定位多模态 AI Agent 框架。本月 Trending 关键词只有一个:Agent,从个人 AI 助手到代码 Agent、Skill 框架到 Agent harness,整个生态正从「AI 写代码」进化到「AI 自主完成任务」。",
        "heat": {
            "score": 7200,
            "level": "热",
            "sources": ["GitHub Trending", "OpenClaw 官方", "Superpowers 仓库", "NousResearch", "Hacker News", "稀土掘金", "Product Hunt"],
            "breakdown": "OpenClaw 376k Star+Superpowers 215k+Hermes Agent 多模态+Skill 框架爆款+Agent harness 生态成型"
        },
        "rising_metrics": {
            "github_stars_24h": 1248,
            "hn_points": 487,
            "x_mentions": 18600,
            "weibo_views": 12400000,
            "search_trend_delta_pct": 198,
            "reddit_upvotes": 2180
        }
    },
    {
        "id": "r004",
        "category": "rising",
        "title": "llama.cpp 史诗级更新:原生多模态 + SvelteKit Web 界面 + 并行聊天,直击 Ollama 功能短板",
        "summary": "开源 AI 推理引擎 llama.cpp 本周迎来史诗级更新,一次性补齐多模态输入、结构化输出与并行交互三大能力,直接对标 Ollama 等封装型工具。用户现在可以直接拖入图片、音频文件或 PDF 文档与文本提示混合输入,触发跨模态理解,视频支持已列入规划。全新 Web 界面基于 SvelteKit 构建,适配手机端,可同时开启多个聊天窗口,支持对历史对话中任意 Prompt 修改并重新生成。这意味着 llama.cpp 已从纯文本推理工具,跃升为覆盖文档分析、创意辅助、教育研究等场景的本地多媒体 AI 中枢。",
        "heat": {
            "score": 6500,
            "level": "热",
            "sources": ["llama.cpp GitHub", "InfoQ", "Hacker News", "X 平台本地 AI 圈", "Reddit r/LocalLLaMA", "稀土掘金", "CSDN"],
            "breakdown": "原生多模态输入+PDF/图片/音频直拖+SvelteKit 现代 Web 界面+多窗口并行聊天+Ollama 降维打击"
        },
        "rising_metrics": {
            "github_stars_24h": 684,
            "hn_points": 412,
            "x_mentions": 7200,
            "weibo_views": 8200000,
            "search_trend_delta_pct": 215,
            "reddit_upvotes": 1340
        }
    },
    {
        "id": "r005",
        "category": "rising",
        "title": "商务部「AI+消费」意见引爆端侧 AI 行情,A 股 AI 眼镜与消费级 3D 打印板块单日成交翻倍",
        "summary": "八部门《关于加快「人工智能+消费」发展的实施意见》发布后,A 股端侧 AI 概念股全线走强。AI 眼镜板块单日成交额较前一周均值放大 112%,博士眼镜、漫步者、明月镜片等龙头标的集体涨停;消费级 3D 打印板块同样活跃,拓竹科技产业链上下游出现联动上涨。国金证券强调,「AI+消费级 3D 打印」与「AI+眼镜」是当下赔率较好的两个细分方向,情绪价值+消费出海+银发经济等新消费有望引领新消费成长,红利消费白马龙头则具备配置性价比。",
        "heat": {
            "score": 6200,
            "level": "热",
            "sources": ["国金证券研报", "Wind 行情数据", "东方财富网", "证券时报", "新浪财经", "财联社", "同花顺"],
            "breakdown": "AI+消费意见落地+AI 眼镜单日成交 +112%+3D 打印联动上涨+情绪价值赛道+银发经济受益"
        },
        "rising_metrics": {
            "github_stars_24h": 0,
            "hn_points": 186,
            "x_mentions": 3400,
            "weibo_views": 24800000,
            "search_trend_delta_pct": 178,
            "reddit_upvotes": 420
        }
    },
    {
        "id": "c001",
        "category": "company",
        "title": "OpenAI 计划 2026 年底员工总数从 4500 扩至 8000,与 Anthropic 进入全面人才战",
        "summary": "据《金融时报》报道,OpenAI 正计划在 2026 年底前将员工总数从目前的约 4500 人扩张至 8000 人,几乎翻倍,以应对来自 Anthropic 与 Google 的全方位竞争。这是自微软重组 OpenAI 治理结构以来,该公司规模最大的一次人力扩张计划。结合年初以来从 Salesforce 挖走近 40 人以及招揽前 Trump 政府 AI 政策官员 Dean Ball 等动作,OpenAI 显然在为最快今年秋季完成的 IPO 做准备,人员规模与组织成熟度都被视为估值冲击 1 万亿美元的关键支撑。",
        "heat": {
            "score": 7000,
            "level": "热",
            "sources": ["Financial Times", "OpenAI 官方", "Reuters", "Bloomberg", "智通财经", "36 氪", "钛媒体"],
            "breakdown": "8000 人目标+同比接近翻倍+应对 Anthropic 竞争+IPO 前组织成熟+Dean Ball 等政策精英加盟"
        }
    },
    {
        "id": "c002",
        "category": "company",
        "title": "Salesforce 发布 Slackbot AI Agent,与 Anthropic 3 亿美元 Token 采购协议同期落地",
        "summary": "6 月 21 日,Salesforce 正式发布面向企业工作流的 Slackbot AI Agent,定位「用对话重塑企业协作」。该智能体能够自动处理消息优先级、安排会议、起草文档,并与 Salesforce 自家的 Agentforce 生态无缝衔接。同日,Salesforce 宣布 2026 年将向 Anthropic 采购价值 3 亿美元的 Claude Token,贝尼奥夫在播客中直言「这些编码代理太棒了,Anthropic 太棒了」。这是 Salesforce 同时加深与 Anthropic 合作、又放任员工被挖给 OpenAI/Anthropic 的「矛盾战略」首次公开化。",
        "heat": {
            "score": 6400,
            "level": "热",
            "sources": ["Salesforce 官方", "Slack 官方", "Anthropic 官方", "TechCrunch", "VentureBeat", "36 氪", "量子位"],
            "breakdown": "Slackbot AI Agent 发布+企业协作对话重塑+3 亿美元 Claude Token 采购+贝尼奥夫公开背书+员工被双向挖角"
        }
    },
    {
        "id": "c003",
        "category": "company",
        "title": "美光财报前夕机构看涨,HBM ASP 2027 财年有望同比 +50%,存储短缺将持续至 2028 年",
        "summary": "海外存储巨头美光科技将于下周三盘后发布最新业绩,市场预期调整后 EPS 将达 20.7 美元(去年同期 1.71 美元),营收预计 355.6 亿美元(去年同期 93 亿)。摩根士丹利最新研报指出,存储供需失衡将持续 2-3 年至 2028 年,基于对行业供需趋紧的判断,高盛同步上调 DRAM、NAND 及 HBM 定价预期;同时坚持 HBM ASP 将相对传统 DRAM 实现追赶效应,有望推动其在 2027 财年实现约 50% 同比增长,2026/2027/2028 财年 HBM 市场总规模将分别达 560 亿、1160 亿、1680 亿美元。",
        "heat": {
            "score": 5900,
            "level": "中",
            "sources": ["Morgan Stanley 研报", "Goldman Sachs 研报", "Bloomberg", "Reuters", "TrendForce", "华尔街见闻", "财联社"],
            "breakdown": "美光财报 EPS 20.7 美元+存储短缺至 2028+HBM ASP +50%+HBM 总规模 1680 亿+高盛大摩同步上调"
        }
    },
    {
        "id": "p001",
        "category": "paper",
        "title": "Nature:植入式微电极 + LLM 解码单神经元语言活动,脑机接口迈入「开口前预知」时代",
        "summary": "本周发表于 Nature 的《Mapping the Neuronal Building Blocks of Human Language with Language Models》研究中,加州大学伯克利分校团队利用植入 8 名癫痫患者额颞叶皮层的微电极阵列,在自然对话时记录数百个神经元电活动,并用 LLM 将神经数据与对话文本做时间比对。结果显示在参与者开口说话前的瞬间,单神经元活动就能预测后续言语的多种特征;神经元存在明确分工,一部分处理特定词汇含义,另一部分负责将短语组合成结构化句子等高级语法任务。模型还能准确区分相似短语,捕获独特上下文语义,为新一代脑机接口奠定基础。",
        "heat": {
            "score": 7200,
            "level": "热",
            "sources": ["Nature", "UC Berkeley 官方", "MIT Technology Review", "The Decoder", "X 平台 BCI 圈", "Reddit r/Neuroscience", "量子位"],
            "breakdown": "Nature 刊发+微电极单神经元记录+LLM 解码语言活动+开口前预知+词汇与句法分工+脑机接口下一代"
        }
    },
    {
        "id": "p002",
        "category": "paper",
        "title": "Nature Machine Intelligence:苏黎世联邦理工提出软体身体+神经形态大脑基准,让机器人学会「以柔克刚」",
        "summary": "苏黎世联邦理工学院与苏黎世大学 Elisa Donati、Giulia D'Angelo 团队本周在 Nature Machine Intelligence 发表论文,提出将柔软身体与神经形态计算相结合的具身智能新范式。软体身体能轻柔变形并吸收接触力,从而大幅降低大脑的计算负载。研究团队同步开源了一个包含特定任务、关键评估指标以及模块化物理机器人平台的基准测试框架,评估指标不再局限于传统的速度和精度,而是聚焦适应能力、稳健性、能源效率以及人机协作安全性。研究表明,利用局部神经回路处理特定任务,配合智能身体,可以让机器人在不搭载超级计算机的情况下实现更高效、节能的现实交互。",
        "heat": {
            "score": 5800,
            "level": "中",
            "sources": ["Nature Machine Intelligence", "ETH Zurich 官方", "苏黎世大学官方", "MIT Technology Review", "IEEE Spectrum", "X 平台具身智能圈", "量子位"],
            "breakdown": "Nature MI 刊发+软体身体+神经形态大脑+模块化开源基准+节能与稳健性指标+具身智能新范式"
        }
    },
    {
        "id": "p003",
        "category": "paper",
        "title": "MIT 新框架 DAAAM 让机器人「记住钥匙放哪了」,OC-NaVQA 准确率较 SOTA 提升 53.6%",
        "summary": "麻省理工学院 Nicolas Gorlo、Lukas Schmid、Luca Carlone 团队本周发布论文《Describe Anything Anywhere At Any Moment》(arXiv:2512.00565),提出一种被称为 DAAAM 的长期记忆框架,使机器人能够快速形成复杂大规模环境的时空模型并进行语言交互。该方法通过将实时四维度量语义建图与高保真自然语言描述相结合,构建层次化 4D 场景图;为克服多模态大模型标注计算慢的瓶颈,研究人员设计了双步优化算法,自动筛选视线最清晰的关键帧进行批量化物体标注,将计算速度提升 10 倍。在 OC-NaVQA 基准测试中,DAAAM 比 SOTA 在问题回答准确率上提升 53.6%,位置误差降低 21.9%,时间误差降低 21.6%。",
        "heat": {
            "score": 5400,
            "level": "中",
            "sources": ["MIT CSAIL 官方", "arXiv 2512.00565", "Nature Machine Intelligence 引用", "Hacker News", "Reddit r/robotics", "X 平台机器人圈", "量子位"],
            "breakdown": "DAAAM 时空记忆框架+4D 场景图层次化+双步优化提速 10 倍+OC-NaVQA +53.6%+机器人找钥匙 Demo"
        }
    },
    {
        "id": "i001",
        "category": "industry",
        "title": "存储现货价加速上行,NV 机柜减配印证 AI 生态关键瓶颈,26Q2 通用 DRAM 合约价预计涨 58-63%",
        "summary": "国泰海通证券最新研报显示,DDR4/DDR5 现货价企稳后涨幅扩大,MLC NAND 现货价延续高增,5 月韩国 DRAM/NAND 出口额同比增长 370%/206%,中国台湾主要存储产业链厂商 5 月营收同比增长 324.8%。TrendForce 预计 26Q2 通用 DRAM 合约价上涨 58-63%,NAND 合约价上涨 70-75%。WSTS 预测 2026 年存储芯片销售额同比增长 250%。英伟达 Vera CPU 内存减配引发市场担忧,但研报认为是 LPDDR5X 供给侧限制下的底线方案,而非需求收缩信号;Agentic AI 带动 KV Cache 容量扩张以及 AI 系统 CPU:GPU 配比提升,对存储需求形成长期支撑。",
        "heat": {
            "score": 5700,
            "level": "中",
            "sources": ["国泰海通证券研报", "TrendForce", "WSTS", "韩国关税厅", "中国台湾存储产业链月度营收", "Wind 数据", "第一财经"],
            "breakdown": "DDR4/DDR5 现货涨 22-40%+韩国出口 +255%+26Q2 DRAM 合约 +58-63%+NV Vera CPU 减配+存储周期结构性转变"
        }
    },
    {
        "id": "i002",
        "category": "industry",
        "title": "PIMCO 总裁:AI 数据中心建设是「绝对机会」,但当前 AI 不能独立做投资决策",
        "summary": "在 2026 陆家嘴论坛上,全球资产管理巨头 PIMCO 董事总经理兼总裁 Christian Stracke 表示,AI 数据中心建设是「绝对机会」,PIMCO 已在量化战略中广泛应用 AI 加速数据分析;在运营层面,法务合规、贸易争端、客户报告服务等大量日常工作是 AI 辅助的合适场景。但他同时强调「当前 AI 尚不能独立作出投资决策,它是辅助研究的工具,而不能替代人类」,在审慎评估风险变量前提下,效率与风险共生,如何守住安全底线是关键。白宫 AI 与加密事务顾问 David Sacks 此前披露,2026 年一季度 AI 相关投资可能贡献美国 GDP 增长的约 75%。",
        "heat": {
            "score": 4900,
            "level": "中",
            "sources": ["PIMCO 官方", "陆家嘴论坛实录", "第一财经", "Reuters", "Bloomberg", "白宫 AI 与加密事务顾问办公室", "财新网"],
            "breakdown": "PIMCO 总裁定调数据中心绝对机会+AI 不能独立投资决策+陆家嘴论坛披露+2026Q1 AI 投资贡献美国 GDP 75%"
        }
    },
    {
        "id": "s001",
        "category": "social",
        "title": "X 与 HN 热议:Anthropic 突发出口限制,Anthropic Fable 5 二次下架传闻再起",
        "summary": "6 月 21 日,KoolerAI 等聚合站及 X 平台 AI 圈流传「Anthropic Faces Sudden Export Restrictions on AI Access」消息,讨论 Anthropic 在 Fable 5 与 Mythos 5 之后是否面临又一次美国商务部紧急禁令。联想到 6 月初 Fable 5 被以「国家安全」为由下架、90 分钟紧急禁令的历史,社区开始担忧接下来 1-2 个月内是否会有更新版本的旗舰模型被纳入实体清单。Anthropic 与美国政府的监管拉锯仍在继续,Anthropic 5 月底 9650 亿美元估值融资与 IPO 推进都被视为影响因素之一。",
        "heat": {
            "score": 6400,
            "level": "热",
            "sources": ["KoolerAI 聚合", "X 平台 AI 安全圈", "Hacker News", "Reddit r/Anthropic", "Anthropic 官方", "Financial Times", "财联社"],
            "breakdown": "Anthropic 出口限制传闻+Fable 5 二度下架担忧+90 分钟禁令历史先例+IPO 推进中的监管不确定性"
        }
    },
    {
        "id": "s002",
        "category": "social",
        "title": "GitHub Trending 当周热榜:agents-radar 单日榜第一,日报类 AI 工具批量涌现",
        "summary": "GitHub 当周 Trending 上,duanyytop/agents-radar 凭借「每日聚合 10 个数据源 AI 生态信号」的卖点登顶单日榜第一,该项目通过 GitHub Actions 每天 08:00 CST 自动运行,聚合 GitHub Repos、Claude Code Skills、Hacker News、Product Hunt、ArXiv、Hugging Face、Dev.to、Lobste.rs、Anthropic + OpenAI sitemap 等源,产出中英双语日报。同步上榜的还有 daily_stock_analysis(ZhuLinsen/daily_stock_analysis)、mem0ai/mem0 等热门工具,体现开发者社区对「AI 自动化自身信息流」的强需求。",
        "heat": {
            "score": 5100,
            "level": "中",
            "sources": ["GitHub Trending", "duanyytop/agents-radar", "ZhuLinsen/daily_stock_analysis", "Hacker News", "X 平台开发者社区", "稀土掘金", "Product Hunt"],
            "breakdown": "agents-radar 单日榜第一+10 数据源聚合+GitHub Actions 自动 08:00 CST+daily_stock_analysis 同步上榜+AI 自动化日报"
        }
    }
]

# 校验字段
assert len(items) == 19

# 构建 news.json
news = {
    "date": TODAY,
    "weekday": WEEKDAY,
    "generated_at": GENERATED,
    "summary": "2026 年 6 月 22 日 AI 行业有八条主线集中爆发:其一,The Information 披露 Salesforce 成 OpenAI/Anthropic 最大人才血库,2026 上半年累计被挖近 100 人,Anthropic 单家拿下 45 人、OpenAI 招 40 人,贝尼奥夫同期宣布 3 亿美元采购 Claude Token;其二,OpenAI 在对齐研究博客发表「强化学习实现有益性格塑造」论文,六项特质跨域泛化、对抗 prompt 也难击穿,被视为 AI 安全从「打补丁」走向「造地基」的范式转折;其三,Databricks 启动新一轮融资目标估值 1750 亿美元,成为 SpaceX、OpenAI、Anthropic 之后一级市场最后一家巨型 AI 独角兽;其四,商务部等八部门联合印发《关于加快「人工智能+消费」发展的实施意见》,AI 手机/PC/眼镜/汽车成重点,端侧 AI 行情引爆,A 股 AI 眼镜单日成交放大 112%;其五,alphaXiv 推出 autoarxiv 功能,改 URL 一键让 AI 智能体复现 arXiv 论文,单卡也能跑,标志读论文从「总结」走向「跑通」的下一阶段;其六,GitHub 6 月 AI 项目榜出炉,OpenClaw 以 376k Star 继续霸榜月榜,Superpowers 215k、Hermes Agent 多模态紧随其后,Agent 生态从「写代码」进化到「自主完成任务」;其七,存储现货价加速上行,TrendForce 预计 26Q2 通用 DRAM 合约价涨 58-63%,英伟达 Vera CPU 内存减配印证 AI 生态关键瓶颈,摩根士丹利预测存储短缺将持续至 2028 年;其八,Nature 本周连续刊发单神经元语言解码与软体身体+神经形态大脑基准两篇重磅论文,AI for Science 与具身智能前沿再下一城。",
    "stats": {
        "total_items": 19,
        "by_category": {
            "headline": 4,
            "rising": 5,
            "company": 3,
            "paper": 3,
            "industry": 2,
            "social": 2
        }
    },
    "items": items,
    "weekly_arc": {
        "label": "本周脉络",
        "weeks": [
            {
                "iso_week": "2026-W26",
                "date": TODAY,
                "theme": "Salesforce 双向挖角重塑硅谷 AI 销售铁军 + OpenAI 对齐范式跃迁 + alphaXiv autoarxiv 让论文一键可跑 + 八部门 AI+消费意见落地 + Databricks 1750 亿美元估值冲刺",
                "highlights": [
                    "Salesforce 成 OpenAI/Anthropic 最大人才血库,2026 上半年 100 人被挖,Anthropic 拿下 45 人",
                    "OpenAI 在对齐研究博客发表「强化学习实现有益性格塑造」论文,六项特质跨域泛化、对抗 prompt 也难击穿",
                    "alphaXiv 推出 autoarxiv,改 URL 一键让 AI 智能体复现 arXiv 论文,单卡也能跑",
                    "商务部等八部门联合印发《关于加快「人工智能+消费」发展的实施意见》,AI 终端进入政策驱动迭代阶段",
                    "Databricks 启动新一轮融资,目标估值 1750 亿美元,成一级市场最后一家巨型 AI 独角兽",
                    "OpenClaw 376k Star 霸榜 GitHub 月榜,Superpowers 215k、Hermes Agent 多模态紧随其后",
                    "llama.cpp 史诗级更新,原生多模态+SvelteKit Web 界面+并行聊天,直击 Ollama 功能短板",
                    "Salesforce 发布 Slackbot AI Agent,与 Anthropic 3 亿美元 Token 采购协议同期落地",
                    "mem0 4 月新记忆算法 BEAM 1M 64.1、LongMemEval 94.8,GitHub Trending 当日登顶",
                    "Nature 刊发单神经元语言解码论文,微电极+LLM 让脑机接口迈入「开口前预知」时代",
                    "存储现货价加速上行,TrendForce 预计 26Q2 通用 DRAM 合约价涨 58-63%,短缺持续至 2028 年",
                    "美光财报前夕机构看涨,HBM ASP 2027 财年有望同比 +50%,HBM 总规模 1680 亿美元",
                    "Nature Machine Intelligence:苏黎世联邦理工提出软体身体+神经形态大脑基准",
                    "MIT DAAAM 时空记忆框架让机器人「记住钥匙放哪了」,OC-NaVQA 准确率较 SOTA 提升 53.6%",
                    "OpenAI 计划 2026 年底员工总数从 4500 扩至 8000,与 Anthropic 进入全面人才战"
                ]
            }
        ]
    },
    "monthly_arc": {
        "label": "本月脉络",
        "month": "2026-06",
        "themes": [
            "AI 人才战从架构师升级为销售铁军之争,Noam Shazeer+Jumper+Salesforce 100 人双向流动,OpenAI 计划年底 8000 人,Anthropic 估值 9650 亿反超 OpenAI",
            "AI 安全从「打补丁」走向「造地基」,OpenAI 对齐论文六项特质跨域泛化,Anthropic 出口限制拉锯,Anthropic Fable 5 两次下架倒逼国产替代窗口",
            "论文可复现性进入智能体时代,alphaXiv autoarxiv 把 4×H100 复现实验压缩到单卡 LoRA 40 步,读论文从「总结」走向「跑通」",
            "Agent 生态从「写代码」进化到「自主完成任务」,OpenClaw 376k、Superpowers 215k、Hermes Agent 多模态霸榜 GitHub 月榜,llama.cpp 多模态直击 Ollama",
            "消费 AI 进入政策驱动阶段,商务部八部门发文推动 AI 手机/PC/眼镜/汽车,端侧 AI 行情引爆,A 股 AI 眼镜单日成交 +112%",
            "存储结构性短缺延续至 2028 年,TrendForce 预计 26Q2 通用 DRAM 合约价 +58-63%、NAND +70-75%,HBM ASP 2027 财年同比 +50%",
            "Anthropic 与 OpenAI 双雄 IPO 竞速白热化,Databricks 1750 亿美元估值冲刺成最后巨型独角兽,Databricks/Anthropic/OpenAI 共同改写一级市场格局"
        ]
    }
}

with open("data/news.json", "w", encoding="utf-8") as f:
    json.dump(news, f, ensure_ascii=False, indent=2)

print(f"✅ news.json 写入完成:date={TODAY}, items={len(items)}")
print(f"   by_category: {news['stats']['by_category']}")
