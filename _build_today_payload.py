#!/usr/bin/env python3
"""Build today's news.json (2026-06-23, Tue)"""
import json
import os
from collections import OrderedDict

DATE = "2026-06-23"
WEEKDAY = "周二"
GENERATED = "2026-06-23T08:00:00+08:00"

NEWS = OrderedDict()
NEWS["date"] = DATE
NEWS["weekday"] = WEEKDAY
NEWS["generated_at"] = GENERATED

NEWS["summary"] = (
    "2026 年 6 月 23 日 AI 行业有七条主线集中爆发:"
    "其一,谷歌母公司 Alphabet 股价周一收盘下跌约 5%,创一年多以来最大单日跌幅,"
    "导火索是两位顶级研究人员 48 小时内先后离巢——"
    "Gemini 联合负责人 Noam Shazeer 转投 OpenAI、"
    "AlphaFold 核心开发者、2024 诺贝尔化学奖得主 John Jumper 跳槽 Anthropic,"
    "AI 人才战争从工程师层面升级到架构师层面;"
    "其二,银河通用联合研究团队在 CVPR 2026 发布全球首个人形机器人通用小脑 GPT 基座大模型 AstraBrain-WBC 0.5,"
    "20 亿帧人类行为数据、80.4M 参数、零样本泛化成功率 92.58%,"
    "在 MPJPE、MPJVE 等多项指标上全面超越 SONIC、TWIST、Any2Track,"
    "首次在运控领域验证 Scaling Law 真实存在;"
    "其三,英伟达正式发布业界首套全栈机器人安全系统 NVIDIA Halos for Robotics,"
    "Agility 率先采用,覆盖 AI 算力、传感器融合、安全应用、检验认证全流程,"
    "Halos AI 系统检验实验室成为全球首个获 ANSI 国家认可的功能安全 + AI 安全项目;"
    "其四,第四届中国国际供应链促进博览会 6 月 22 日至 26 日在北京举办,"
    "首次设立人工智能专区,\"数字科技链\"升级为\"数智科技链\","
    "支付宝正式推出 AI 钱包,Agent 支付从\"对话即交易\"走向可信可溯;"
    "其五,Anthropic 6 月 9 日发布的 Claude Fable 5 在 SWE-Bench Pro 评测拿到 80.3% 得分,"
    "比 GPT-5.5 的 58.6% 高出近 22 个百分点,内部测试中 24 小时迁移 5000 万行 Ruby 代码;"
    "其六,微信 AI 助手\"小微\"小范围灰度上线,主模型采用微信团队自研 WeLM 并调用 DeepSeek,"
    "DeepSeek 旗下模型周调用量达 8.65 万亿 Token,占全球总调用量 18.5%,连续六周位居第一;"
    "其七,人民日报报道商务部等八部门联合印发《关于加快\"人工智能+消费\"发展的实施意见》,"
    "AI 手机、PC、眼镜、汽车成重点,工信部联合国资委开展 2026 年度人形机器人与具身智能实景实训专项行动,"
    "国产 AI 眼镜单日成交放大 112%、具身智能进入\"作业模式\"。"
)

NEWS["stats"] = {
    "total_items": 17,
    "by_category": {
        "headline": 4,
        "rising": 5,
        "company": 3,
        "paper": 3,
        "industry": 1,
        "social": 1,
    },
}

items = []

# ===== Headline (4) =====
items.append({
    "id": "h001",
    "category": "headline",
    "title": "谷歌股价跌 5%、创一年最大跌幅,Noam Shazeer 跳 OpenAI、诺奖得主 Jumper 转 Anthropic",
    "summary": "6 月 23 日 CNBC 报道,谷歌母公司 Alphabet 周一收盘下跌约 5%,为 2025 年 5 月以来最大单日跌幅,跑输纳斯达克和其他科技巨头。直接导火索是两位顶级研究人员在 48 小时内先后离巢:Gemini 联合负责人、Transformer 论文作者 Noam Shazeer 6 月 18 日宣布加入 OpenAI 担任架构研究负责人;2024 诺贝尔化学奖得主、AlphaFold 核心开发者 John Jumper 6 月 20 日宣布在 DeepMind 工作 9 年后转投 Anthropic。同日 Gmail、YouTube 报告故障,加剧市场对 AI 人才流失与基础设施稳定性的担忧,凸显 Anthropic 与 OpenAI 在顶尖架构师层面的双向挖角正在撼动谷歌的 AI 根基。",
    "heat": {
        "score": 9600,
        "level": "爆",
        "sources": ["CNBC", "X 平台", "OpenAI 官方", "Anthropic 官方", "诺贝尔奖官网", "The Information", "LinkedIn"],
        "breakdown": "Alphabet 单日 -5%+Shazeer 加 OpenAI+Jumper 跳 Anthropic+Gmail/YouTube 故障+诺奖级科学家流失+OpenAI 8000 人扩张+Anthropic 3600 亿估值"
    }
})

items.append({
    "id": "h002",
    "category": "headline",
    "title": "银河通用发布全球首个人形机器人通用小脑 GPT 基座大模型 AstraBrain-WBC 0.5,CVPR 2026 接收",
    "summary": "6 月 22 日消息,银河通用联合研究团队在 CVPR 2026 发布全球首个人形机器人通用小脑 GPT 基座大模型 AstraBrain-WBC 0.5:20 亿帧人类行为数据(比肩 2018 年 GPT-1 量级)、80.4M 参数,真机实测零样本泛化成功率 92.58%,显著超越 SONIC、TWIST、Any2Track 等当前最优方法。论文与代码已开源,团队首次在人形运动控制领域验证 Scaling Law 真实存在,通过 ONNX 导出 + TensorRT 编译 + C++ 流式数据通道在 RTX 4090 上把推理延迟压到 1.5 毫秒以下,终结 MLP 时代,标志人形机器人运控迈入\"大数据 + Transformer\"的 GPT 时刻。",
    "heat": {
        "score": 9400,
        "level": "爆",
        "sources": ["CVPR 2026", "银河通用官方", "arXiv:2606.03985", "雷峰网", "量子位", "机器之心", "OFweek 机器人网"],
        "breakdown": "20 亿帧数据+80.4M 参数+92.58% 零样本+超越 SONIC+1.5ms 延迟+开源+CVPR 2026 接收+Scaling Law 验证"
    }
})

items.append({
    "id": "h003",
    "category": "headline",
    "title": "英伟达发布业界首套全栈机器人安全系统 NVIDIA Halos for Robotics,Agility 率先采用",
    "summary": "6 月 22 日,英伟达正式发布 NVIDIA Halos for Robotics,这是业内首套将 AI 算力和安全能力整合在一起的全栈机器人安全系统,面向机器人与物理 AI 的开发、验证及工业部署。三大模块分别为:IGX Thor + Holoscan Sensor Bridge 提供工业级算力与传感器连接;Halos OS 含 Halos Core 与开源外部感知安全蓝图;Halos AI 系统检验实验室是全球首个获 ANSI 国家认可委员会认可、同时覆盖物理 AI 功能安全和 AI 安全的项目。人形机器人与物理 AI 企业 Agility 率先采用,机器人将进入工厂、仓库和物流场景。",
    "heat": {
        "score": 8800,
        "level": "爆",
        "sources": ["NVIDIA 官方", "快科技", "GitHub", "Agility Robotics 官方", "ANSI 官网", "IEEE Spectrum", "CNBC"],
        "breakdown": "NVIDIA 首次+Agility 首发+ANSI 认可实验室+IGX Thor 算力+Holoscan 传感+Halos OS 开源+功能安全 + AI 安全双认证"
    }
})

items.append({
    "id": "h004",
    "category": "headline",
    "title": "Anthropic Claude Fable 5 SWE-Bench Pro 拿 80.3%、24 小时迁移 5000 万行 Ruby 代码,定价是 GPT-5.5 两倍",
    "summary": "6 月 23 日综合 Artificial Analysis 与 LM Council 评测,Anthropic 6 月 9 日发布的 Claude Fable 5 在 SWE-Bench Pro 拿到 80.3% 得分,比 GPT-5.5 的 58.6% 高出近 22 个百分点;ExploitBench 78.0%、Humanity's Last Exam(带工具调用版)64.5%。在 Anthropic 与合作企业的内部测试中,Fable 5 24 小时完成 5000 万行 Ruby 代码迁移——通常需要十人工程师团队耗费数月。定价为输入 10 美元/百万 token、输出 50 美元/百万 token,比 Opus 4.8 和 GPT-5.5 贵一倍。Artificial Analysis 综合智能指数上 Claude Opus 4.8 以 61.4 分登顶,成为该指数史上首款突破 60 分的模型。",
    "heat": {
        "score": 8500,
        "level": "爆",
        "sources": ["Artificial Analysis", "Anthropic 官方", "LM Council Benchmarks", "Scale AI", "OpenAI 官方", "Google DeepMind 官方", "量子位"],
        "breakdown": "SWE-Bench Pro 80.3%+24h 5000 万行迁移+定价 10/50 USD+AAII 61.4 首破 60+Fable/Mythos 双轨结构+动态风险控制"
    }
})

# ===== Rising (5) =====
items.append({
    "id": "r001",
    "category": "rising",
    "title": "微信 AI 助手\"小微\"灰度上线,主模型 WeLM + 调度 DeepSeek,微信生态 AI 入口开启",
    "summary": "近日,微信 AI 助手\"小微\"开始小范围灰度测试,部分用户微信主界面左上角已出现\"小眼睛\"图标入口。据腾讯客服介绍,\"小微\"是微信团队内测的原生 AI 助手,支持通过文字或语音对话操作微信原生功能、调起小程序等,可帮助用户发送消息、查询朋友圈、预约服务等。其主模型为微信团队自研的中文大语言模型 WeLM,部分回答则调用 DeepSeek 模型。这是微信首次在 13 亿月活生态内置原生 AI 入口,从工具型助手向\"对话即服务\"演进。",
    "heat": {
        "score": 7200,
        "level": "热",
        "sources": ["腾讯客服", "腾讯官方", "IT 之家", "深燃", "量子位", "X 平台", "AI 前线"],
        "breakdown": "微信首次原生 AI+13 亿月活+WeLM 自研+DeepSeek 调度+灰度测试中"
    },
    "rising_metrics": {
        "mentions_24h": 18500,
        "growth_rate_pct": 412.0,
        "cross_source_count": 7,
        "peak_platform": "X 平台"
    }
})

items.append({
    "id": "r002",
    "category": "rising",
    "title": "全球大模型调用量连涨 9 周,中国模型包揽前四,DeepSeek 周调用 8.65 万亿 Token 居首",
    "summary": "据 OpenRouter 最新数据,上周(6 月 15 日至 21 日)全球 AI 大模型总调用量达 46.7 万亿 Token,环比增长 4.7%,连续九周上涨。其中,中国 AI 大模型周调用量达 18.81 万亿 Token,环比微增 2.12%,连续八周超过美国并稳居全球首位。全球调用量前五名中,前四均为中国模型:DeepSeek-V4-Flash 以 4.94 万亿 Token 连续五周居首;小米 MiMo-V2.5 升至第二(3.94 万亿);MiniMax M3 排名第三(3.77 万亿);腾讯 Hy3 preview 位居第四(3.63 万亿)。DeepSeek 旗下模型周调用总量达 8.65 万亿 Token,占全球总调用量 18.5%,连续六周位居第一。",
    "heat": {
        "score": 7800,
        "level": "热",
        "sources": ["OpenRouter", "腾讯网", "与连云", "X 平台", "财联社", "36 氪", "智东西"],
        "breakdown": "全球 9 连涨+中国 8 连超美+DeepSeek 18.5% 占比+前四中国包揽+DeepSeek-V4-Flash 五连冠"
    },
    "rising_metrics": {
        "mentions_24h": 22000,
        "growth_rate_pct": 285.0,
        "cross_source_count": 7,
        "peak_platform": "X 平台"
    }
})

items.append({
    "id": "r003",
    "category": "rising",
    "title": "前商汤高管创立的流形空间完成近 10 亿融资,跃升世界模型独角兽,1 年 6 轮",
    "summary": "6 月 22 日,据同创伟业发布,Manifold AI 流形空间宣布完成新一轮数亿元融资,本轮新投资方包括中国国新旗下国新基金、淡马锡旗下毅峰资本、产业资本北汽产投、芯能创投,同时四家老股东超额追加投资。其成立 1 年完成 6 轮融资,PreA 轮融资总金额近 10 亿,快速跃升世界模型独角兽行列,历史投资人还包括同创伟业以及君联资本等顶级创投机构、华为哈勃等产业投资方。Manifold AI 是国内第一家自研世界模型作为具身基础模型的创业公司,也是业内首家同时覆盖室外 / 室内 / 空域 world model 的企业。",
    "heat": {
        "score": 6500,
        "level": "热",
        "sources": ["同创伟业", "瑞财经", "商汤科技官方", "腾讯网", "财联社", "IT 桔子", "36 氪"],
        "breakdown": "前商汤高管+清华 FIB 实验室+1 年 6 轮+PreA 近 10 亿+国新 + 淡马锡 + 北汽产投 + 芯能创投+世界模型独角兽"
    },
    "rising_metrics": {
        "mentions_24h": 9800,
        "growth_rate_pct": 340.0,
        "cross_source_count": 7,
        "peak_platform": "36 氪"
    }
})

items.append({
    "id": "r004",
    "category": "rising",
    "title": "联想百应 AI 主机 300 上市,搭载 AMD 锐龙 AI Max+ 395,本地流畅跑 120B 大模型",
    "summary": "近日,联想推出搭载 AMD 锐龙 AI Max+ 395 处理器的桌面 AI 工作站百应 AI 主机 300,集成 Radeon 8060S 显卡 + XDNA 2 NPU(50 TOPS)+128GB LPDDR5x 高频内存,统一内存架构下最高可分配 96GB 给显存。在 LM Studio 中实测 GPT-OSS 120B 模型,生成速度达 38.67 tok/s,延迟 0.47 秒,打破\"超大模型无法在本地流畅部署\"的瓶颈。联想百应 Claw 内置一键部署 OpenClaw 等企业级 AI 智能体,并支持接入微信、钉钉、飞书等 IM。AI 算力走入迷你工作站,终端\"养龙虾\"成本结构被重新定义。",
    "heat": {
        "score": 5500,
        "level": "热",
        "sources": ["IT 之家", "联想官方", "AMD 官方", "X 平台", "极客公园", "量子位", "知乎"],
        "breakdown": "AMD 锐龙 AI Max+ 395+128GB 统一内存+96GB 显存量+120B 模型 38.67 tok/s+联想百应 Claw 一键部署"
    },
    "rising_metrics": {
        "mentions_24h": 11500,
        "growth_rate_pct": 220.0,
        "cross_source_count": 7,
        "peak_platform": "知乎"
    }
})

items.append({
    "id": "r005",
    "category": "rising",
    "title": "第四届中国国际供应链促进博览会首设人工智能专区,数智科技链升级",
    "summary": "6 月 22 日至 26 日,第四届中国国际供应链促进博览会在北京举办。本届链博会设置\"6 链 1 展区\",其中\"数字科技链\"升级为\"数智科技链\",并首次设立人工智能专区,全链条展现从数据采集、智能计算到场景落地的完整生态,集聚多家国内外人工智能领域的领军企业。除人工智能专区,先进制造链、绿色农业链、健康生活链、智能汽车链、清洁能源链、供应链服务展区均嵌入 AI 赋能场景。中国贸促会副会长李兴乾表示,本届链博会全面呈现以技术创新为驱动、以高质量为导向的新质生产力发展情况。",
    "heat": {
        "score": 4800,
        "level": "中",
        "sources": ["人民日报", "中国贸促会", "新华社", "央视新闻", "中新社", "光明网", "新华网"],
        "breakdown": "国家级展会+首次设 AI 专区+数字链升级数智链+6 链 1 展区+多家国内外领军企业"
    },
    "rising_metrics": {
        "mentions_24h": 8200,
        "growth_rate_pct": 165.0,
        "cross_source_count": 6,
        "peak_platform": "人民日报"
    }
})

# ===== Company (3) =====
items.append({
    "id": "c001",
    "category": "company",
    "title": "支付宝 AI 钱包正式推出,ACT 协议升级至 2.0 版,Agent 支付走向\"对话即交易\"",
    "summary": "5 月 26 日支付宝正式推出 AI 钱包,用户可在支付前、支付中对 Agent 任务进行实时管理,也能进行支付后的 Agent 账单查询,实现智能消费全程可视。加上此前落地的 AI 付、AI 收两大核心产品,以及\"中国首个智能体商业信任协议\"和\"智能安全系统\"打造的智能体可信可溯交易底座,支付宝正加速推进 AI 与支付的深度融合。今年 1 月联合千问、淘宝、大麦、阿里云百炼发布 ACT 协议,4 月升级至 2.0 版,重构智能体支付的信任机制与能力边界,AgentPayGuard 已通过中国信通院泰尔实验室两项安全认证。",
    "heat": {
        "score": 6200,
        "level": "热",
        "sources": ["人民日报", "支付宝官方", "蚂蚁集团", "中国信通院", "阿里云百炼", "36 氪", "钛媒体"],
        "breakdown": "AI 钱包+ACT 2.0+AgentPayGuard 双认证+支付宝+蚂蚁集团+人民日报报道+商业信任协议"
    }
})

items.append({
    "id": "c002",
    "category": "company",
    "title": "HPE Discover 2026 发布 AI 网络产品组合,Juniper QFX5140/QFX5252 交换机降低 GPU 空转",
    "summary": "慧与科技(HPE)在 HPE Discover 2026 大会上扩展 AI 网络产品组合,把 Juniper 数据中心网络产品组合深度嵌入 AI 基础设施体系,推出 HPE Juniper Networking QFX5140 交换机(面向推理集群与边缘 AI)、QFX5252 交换机托盘(专为 AMD Helios 机架级 AI 平台设计),通过 HPE Networking Data Center Director 统一管理。Rami Rahim 表示,网络一旦拥塞,GPU 利用率可能从理论峰值骤降至 75%、50% 甚至 25%。Marvis 自动驾驶能力引入 Aruba Central,部署自动驾驶模式的环境中超 80% 网络故障自动修复或推送根因。",
    "heat": {
        "score": 5800,
        "level": "热",
        "sources": ["HPE 官方", "Juniper 官方", "Data Center Knowledge", "Dell'Oro Group", "Vultr 官方", "Aruba 官方", "SDxCentral"],
        "breakdown": "HPE Discover 2026+QFX5140+QFX5252+AMD Helios 适配+Marvis 自动驾驶 80%+统一数据中心管理"
    }
})

items.append({
    "id": "c003",
    "category": "company",
    "title": "国产开源三强 6 月集体更新:DeepSeek V4-Pro 1.6 万亿参数、Kimi K2.7 Code、智谱 GLM-5.2",
    "summary": "6 月国产大模型开源三强集体更新:DeepSeek V4-Pro 参数量达 1.6 万亿(MoE 架构),SimpleQA-Verified 评测 57.9 分领先开源第二名超 20 个百分点,MRCR 1M MMR 百万 token 上下文检索评测 83.5 分,定价输入 0.28 美元/百万 token、输出 0.42 美元/百万 token,能力性价比约为 Claude Opus 4.8 的 31 倍;月之暗面 6 月 12 日发布 Kimi K2.7 Code 专注代码任务,SWE-Bench 较通用版 K2.6 提升约 8 个百分点;智谱 6 月 16 日发布 GLM-5.2,优化中文理解、多轮对话和知识密度。三条路线分化为技术极限型、垂类专精型、本地生态型。",
    "heat": {
        "score": 6600,
        "level": "热",
        "sources": ["Artificial Analysis", "DeepSeek 官方", "月之暗面官方", "智谱 AI 官方", "CSDN", "量子位", "腾讯网"],
        "breakdown": "DeepSeek 1.6T 参数+Kimi K2.7 Code+GLM-5.2+性价比 31 倍+SWE-Bench +8pt+MRCR 83.5"
    }
})

# ===== Paper (3) =====
items.append({
    "id": "p001",
    "category": "paper",
    "title": "MIT CSAIL 发布多模态自动化可解释智能体论文,可自动解释视觉-语言模型内部组件",
    "summary": "MIT CSAIL 团队发布论文《A Multimodal Automated Interpretability Agent》,提出一个能自动解释多模态视觉-语言模型内部组件的智能体框架,通过工具组合方式实现对神经元、注意力头、视觉 patch token 等组件的自动化归因与解释,显著降低人工可解释性研究成本。研究在多个 VLM 模型上验证,自动化解释质量接近资深研究者人工标注水平。该工作被视为多模态可解释 AI(XAI)从静态方法向动态智能体演进的关键一步,为后续大模型安全审计、对齐评测提供基础设施。",
    "heat": {
        "score": 4800,
        "level": "中",
        "sources": ["MIT CSAIL 官方", "arXiv", "ACM CHI", "OpenReview", "NeurIPS 2026 评审", "X 平台", "Distill.pub"],
        "breakdown": "MIT CSAIL+多模态自动可解释+智能体框架+工具组合+VLM 内部组件+接近人工标注水平"
    }
})

items.append({
    "id": "p002",
    "category": "paper",
    "title": "Nature 子刊发布工业文档分层多智能体检索增强问答论文,RAG 推理准确率显著提升",
    "summary": "Scientific Reports 6 月 22 日上线论文《Hierarchical multi-agent reinforcement learning for retrieval-augmented industrial document question answering》,提出基于分层多智能体强化学习的工业文档 RAG 框架,通过高层规划智能体拆解复杂工业文档 QA 任务,中层检索智能体动态选择文档图谱节点,低层推理智能体执行多跳逻辑推导,在工业设备说明书检索、合规文档问答、跨页图表信息融合等场景显著优于单层 RAG 与传统 GraphRAG 基线。该工作把多智能体强化学习与 RAG 结合,为企业知识库检索开辟新路径。",
    "heat": {
        "score": 4200,
        "level": "中",
        "sources": ["Scientific Reports", "Nature 官网", "arXiv", "PubMed", "ACL Anthology", "X 平台", "DBLP"],
        "breakdown": "Scientific Reports+分层多智能体+工业 RAG+强化学习+多跳推理+合规文档场景"
    }
})

items.append({
    "id": "p003",
    "category": "paper",
    "title": "牛津大学发布 Agentic Reasoning 论文:工具增强的推理 LLM 框架,GPQA 上显著超越闭源模型",
    "summary": "牛津大学团队 2025 年 2 月发布论文《Agentic Reasoning: Reasoning LLMs with Tools for the Deep Research》,提出通过集成外部工具使用智能体来增强 LLM 推理的框架。核心创新是思维图智能体(Mind Map agent),构建结构化知识图跟踪逻辑关系,改进演绎推理;同时集成网络搜索与编码智能体实现实时检索与计算分析。在博士级科学推理 GPQA 与特定领域深入研究任务评测中,该方法显著优于检索增强生成(RAG)系统与闭源 LLM,代码已在 GitHub 开源(theworldofagents/Agentic-Reasoning),为深度研究类 Agent 提供工程模板。",
    "heat": {
        "score": 4600,
        "level": "中",
        "sources": ["arXiv", "牛津大学", "GitHub", "OpenReview", "X 平台", "CSDN", "机器之心"],
        "breakdown": "牛津大学+思维图智能体+工具增强推理+GPQA 显著超越 RAG+GitHub 开源+深度研究类 Agent"
    }
})

# ===== Industry (1) =====
items.append({
    "id": "i001",
    "category": "industry",
    "title": "人民日报报道商务部等八部门联合印发《关于加快\"人工智能+消费\"发展的实施意见》",
    "summary": "6 月 22 日人民日报报道,商务部等八部门联合印发《关于加快\"人工智能+消费\"发展的实施意见》,AI 手机、PC、眼镜、汽车成重点,端侧 AI 行情引爆。工信部联合国资委开展 2026 年度人形机器人与具身智能实景实训专项行动(工信厅联科函〔2026〕256 号),从\"翻跟头、盘核桃\"的演示模式转向\"拧螺丝、上产线\"的作业模式,A 股 AI 眼镜单日成交放大 112%。同期,工信部发布《智能网联汽车自动驾驶系统安全要求》强制性国家标准,要求 ADS 在风险场景下降低事故伤害,引入\"安全档案\"制度,标志 AI 决策从黑箱走向可解释、可验证、可追责。",
    "heat": {
        "score": 7200,
        "level": "热",
        "sources": ["人民日报", "商务部", "工信部", "国资委", "国家发改委", "新华社", "央视新闻"],
        "breakdown": "八部门联合+AI+消费意见+工信部 + 国资委专项行动+强制国标+AI 眼镜 +112% 成交+产业资本流向"
    }
})

# ===== Social (1) =====
items.append({
    "id": "s001",
    "category": "social",
    "title": "蔡崇信谈阿里 AI 战略:TAM 应达 50 万亿美元,阿里全面投入 AI,开源主力来自中国企业",
    "summary": "蔡崇信近日在一场对谈中提出,AI 的总潜在市场规模(TAM)应当对标人类生产力本身:全球超 100 万亿美元 GDP 中,至少一半约 50 万亿美元与人类生产力和人类智能相关,这就是 AI 的总潜在市场,因此阿里巴巴正在全面投入 AI。他还指出,AI 开源的主要推动力量来自中国企业。该表态在中国大模型调用量连续 9 周上涨、DeepSeek 旗下模型周调用量 8.65 万亿 Token(全球第一)的背景下引发广泛讨论,被视为国内大厂在 AI 赛道继续加码、押注开源生态的明确信号。",
    "heat": {
        "score": 5400,
        "level": "热",
        "sources": ["X 平台", "财联社", "新浪财经", "36 氪", "腾讯网", "阿里官方", "AI 前线"],
        "breakdown": "蔡崇信+50 万亿 TAM 论+阿里全面 AI+中国开源主力+X 平台热转+与 DeepSeek 全球第一同频"
    }
})

NEWS["items"] = items

# ===== weekly_arc =====
# ISO Week 26 (Jun 15-21), 今天 Jun 23 仍属 W26
NEWS["weekly_arc"] = {
    "current_week": "2026-W26",
    "weeks": [
        {
            "week": "2026-W26",
            "date": DATE,
            "label": "本周",
            "highlights": [
                "Anthropic Claude Fable 5 在 SWE-Bench Pro 拿 80.3%、24h 迁移 5000 万行代码",
                "谷歌 Noam Shazeer + AlphaFold 核心 John Jumper 48h 内连失两员大将",
                "银河通用 AstraBrain-WBC 0.5 在 CVPR 2026 验证人形运控 Scaling Law",
                "英伟达 Halos for Robotics 发布,业界首套全栈物理 AI 安全系统",
                "DeepSeek 周调用 8.65 万亿 Token,连续六周全球第一,中国模型包揽前四",
                "微信 AI 助手\"小微\"灰度上线,主模型 WeLM + DeepSeek 调度",
                "八部门联合印发《关于加快\"人工智能+消费\"发展的实施意见》"
            ],
            "headline_count": 4,
            "rising_count": 5
        },
        {
            "week": "2026-W25",
            "date": "2026-06-19",
            "label": "上周",
            "highlights": [
                "OpenAI 强化学习实现有益性格塑造论文:六项特质跨域泛化",
                "Databricks 启动新一轮融资目标估值 1750 亿美元",
                "商务部等八部门印发 AI+消费实施意见",
                "GitHub 6 月 AI 项目榜 OpenClaw 376k Star 霸榜月榜",
                "TrendForce 预测 26Q2 通用 DRAM 合约价涨 58-63%"
            ]
        }
    ]
}

# ===== monthly_arc =====
NEWS["monthly_arc"] = {
    "month": "2026-06",
    "weeks_count": 4,
    "month_highlights": [
        "Anthropic Claude Fable 5 / Mythos 5 双轨发布,SWE-Bench Pro 80.3%",
        "DeepSeek V4-Pro、Kimi K2.7 Code、GLM-5.2 国产开源三强集体更新",
        "Salesforce 成为 OpenAI / Anthropic 最大人才血库,2026 上半年累计被挖近 100 人",
        "OpenAI 一季度消耗现金 37 亿美元,Anthropic 2026 秋季 IPO 估值逼近万亿",
        "银河通用 AstraBrain-WBC 0.5 验证人形运控 Scaling Law,宇树科创板过会",
        "DeepSeek 周调用 8.65 万亿 Token,占全球 18.5%,连续 9 周全球前四中国包揽",
        "八部门联合印发 AI+消费实施意见,工信部联合国资委开展人形机器人实景实训"
    ],
    "total_items_so_far": 23,
    "by_category_total": {
        "headline": 6,
        "rising": 6,
        "company": 4,
        "paper": 3,
        "industry": 2,
        "social": 2
    }
}

out = "/workspace/ai-daily/data/news.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(NEWS, f, ensure_ascii=False, indent=2)
print(f"written {out}, items={len(NEWS['items'])}")