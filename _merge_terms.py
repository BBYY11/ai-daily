#!/usr/bin/env python3
"""合并 2026-06-23 高频词条到 terms.json,保留已有项,新增 10 个。"""
import json

with open("data/terms.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

new_terms = {
    "AstraBrain-WBC 0.5": {
        "name": "AstraBrain-WBC 0.5",
        "category": "学术 / 论文",
        "summary": "银河通用联合研究团队 2026 年 6 月在 CVPR 2026 发布的人形机器人通用小脑 GPT 基座大模型,20 亿帧人类行为数据、80.4M 参数,真机零样本泛化成功率 92.58%。",
        "detail": "论文 arXiv:2606.03985 已开源,首次在人形运动控制领域验证 Scaling Law 真实存在,在 MPJPE、MPJVE 等指标上全面超越 SONIC、TWIST、Any2Track,终结 MLP 时代,标志人形机器人运控进入 GPT 时刻。",
        "links": [
            {"label": "arXiv", "url": "https://arxiv.org/abs/2606.03985"}
        ]
    },
    "NVIDIA Halos for Robotics": {
        "name": "NVIDIA Halos for Robotics",
        "category": "硬件 / 平台",
        "summary": "英伟达 2026 年 6 月 22 日发布的业界首套全栈机器人安全系统,覆盖 AI 算力、系统软件、传感器数据、安全应用、检验认证全流程。",
        "detail": "三大模块:IGX Thor + Holoscan Sensor Bridge(硬件)、Halos OS(含 Halos Core + 外部感知安全蓝图,GitHub 开源)、Halos AI 系统检验实验室(全球首个获 ANSI 认可的功能安全 + AI 安全项目)。Agility 率先采用。",
        "links": []
    },
    "Claude Fable 5": {
        "name": "Claude Fable 5",
        "category": "基础模型",
        "summary": "Anthropic 2026 年 6 月 9 日发布的旗舰模型,与 Mythos 5 共享底层架构但面向不同用户,Fable 5 公开、内置动态风险控制自动切换 Opus 4.8。",
        "detail": "SWE-Bench Pro 评测 80.3%(比 GPT-5.5 的 58.6% 高 22 个百分点),ExploitBench 78.0%,Humanity's Last Exam(带工具调用)64.5%。内部测试 24 小时迁移 5000 万行 Ruby 代码。定价输入 10 美元、输出 50 美元/百万 token。",
        "links": []
    },
    "微信 AI 小微": {
        "name": "微信 AI 助手小微",
        "category": "产品 / 发布",
        "summary": "微信团队内测的原生 AI 助手,2026 年 6 月小范围灰度上线,主界面左上角出现小眼睛图标入口,主模型采用微信自研 WeLM 并调用 DeepSeek。",
        "detail": "支持文字或语音对话操作微信原生功能、调起小程序,可帮助用户发送消息、查询朋友圈、预约服务。这是微信首次在 13 亿月活生态内置原生 AI 入口,从工具型助手向对话即服务演进。",
        "links": []
    },
    "Manifold AI 流形空间": {
        "name": "Manifold AI 流形空间",
        "category": "公司 / 资本",
        "summary": "由前商汤高管武伟博士创立的国内第一家自研世界模型作为具身基础模型的创业公司,2025 年 5 月底成立,1 年完成 6 轮融资。",
        "detail": "6 月 22 日宣布完成新一轮数亿元融资,本轮投资方包括国新基金、淡马锡毅峰资本、北汽产投、芯能创投。PreA 轮融资总金额近 10 亿,跃升世界模型独角兽,也是业内首家同时覆盖室外/室内/空域 world model 的企业。",
        "links": []
    },
    "支付宝 AI 钱包": {
        "name": "支付宝 AI 钱包",
        "category": "产品 / 发布",
        "summary": "支付宝 2026 年 5 月 26 日正式推出的 AI 钱包,用户可在支付前、支付中对 Agent 任务进行实时管理,也能进行支付后的 Agent 账单查询。",
        "detail": "加上此前落地的 AI 付、AI 收两大核心产品,以及中国首个智能体商业信任协议和智能安全系统打造的可信可溯交易底座,支付宝正加速推进 AI 与支付的深度融合。ACT 协议 4 月升级至 2.0 版。",
        "links": []
    },
    "DeepSeek-V4-Flash": {
        "name": "DeepSeek-V4-Flash",
        "category": "基础模型",
        "summary": "DeepSeek 旗下轻量级模型,2026 年 6 月 15-21 日周调用量达 4.94 万亿 Token,连续五周位居 OpenRouter 全球第一。",
        "detail": "DeepSeek 旗下模型周调用总量达 8.65 万亿 Token,占全球总调用量 18.5%,连续六周位居第一。中国 AI 大模型周调用量 18.81 万亿 Token,连续八周超过美国稳居全球首位。",
        "links": []
    },
    "AMD 锐龙 AI Max+ 395": {
        "name": "AMD 锐龙 AI Max+ 395",
        "category": "硬件 / 芯片",
        "summary": "AMD 旗舰级 AI 处理器,Zen 5 架构、4nm 制程、16 核 32 线程、最高 5.1GHz,集成 Radeon 8060S 显卡 + XDNA 2 NPU(50 TOPS),128GB LPDDR5x 高频内存。",
        "detail": "联想百应 AI 主机 300 搭载,统一内存架构下最高分配 96GB 给显存,在 LM Studio 实测 GPT-OSS 120B 模型生成速度达 38.67 tok/s,延迟 0.47 秒,打破超大模型无法在本地流畅部署的瓶颈。",
        "links": []
    },
    "HPE Juniper QFX5252": {
        "name": "HPE Juniper Networking QFX5252",
        "category": "硬件 / 网络",
        "summary": "慧与科技(HPE)在 HPE Discover 2026 发布的全新 AI 网络交换机托盘,专为 AMD Helios 机架级 AI 平台设计。",
        "detail": "减少因等待数据导致 GPU 空转的网络延迟,与 QFX5140 推理集群交换机、Marvis 自动驾驶网络能力、Aruba Central 集成共同构成 HPE 整合 Juniper 后的 AI 网络产品组合,瞄准 AI 数据中心规模扩张的连接瓶颈。",
        "links": []
    },
    "AI+消费实施意见": {
        "name": "AI+消费 实施意见",
        "category": "政策 / 监管",
        "summary": "商务部联合发改委、工信部等八部门 2026 年 6 月联合印发的《关于加快人工智能+消费发展的实施意见》,推动 AI 手机、AI PC、智能眼镜、智能汽车等终端加快迭代。",
        "detail": "工信部联合国资委开展 2026 年度人形机器人与具身智能实景实训专项行动(工信厅联科函〔2026〕256 号)。工信部同步发布《智能网联汽车自动驾驶系统安全要求》强制性国家标准,要求 ADS 在风险场景下降低事故伤害,引入安全档案制度。",
        "links": []
    }
}

existing.update(new_terms)

with open("data/terms.json", "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"✅ terms.json 已合并:新增 {len(new_terms)} 个,合计 {len(existing)} 个")