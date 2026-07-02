# AI Daily · 2026-07-02 周四 · 全球 AI 早报

> 2026 年 7 月 2 日 AI 早报五大主线集中爆发:其一,Anthropic 7 月 1 日凌晨正式发布 Claude Sonnet 5,SWE-bench Pro 63.2%、Humanity's Last Exam 开工具后 57.4%、OSWorld-Verified 81.2%,多项指标逼近旗舰 Opus 4.8,API 定价仅 Opus 4.8 的 60%、发布期至 8 月 31 日尝鲜价低至 2/10 美元每百万 token,正式取代 Opus 平替路线;其二,Anthropic 同日宣布 Claude Fable 5 / Mythos 5 解除美国商务部出口管制,Fable 5 重新在 GitHub Copilot 全面上线,Mythos 5 仅向受信任机构开放,持续 19 天的「行政命令级 AI 模型监管」完整闭环;其三,Anthropic 同日发布科研 AI 工作台 Claude Science 与 Slack 集成 Claude Tag,从「生产力工具」延伸至「团队成员+科研基础设施」;其四,Claude Code「中国时区标记」隐秘代码事件持续发酵,Anthropic 7 月 1 日承认 3 月起上线反转售反蒸馏实验,承诺 7 月 2 日版本完全回滚,中国开发者社区强烈反弹;其五,Meta 据彭博 7 月 1 日披露正在筹建 Meta Compute 云业务,拟对外销售富余 AI 算力和自研模型 Muse Spark,直接挑战 AWS/Azure/Google Cloud,Meta 股价盘中涨超 10%、CoreWeave 跌超 13%、Nebius 跌超 14.5%,AI 行业正式从「模型叙事」进入「算力资产效率叙事」。
>
> 共 18 条新闻 · 订阅:https://bbyy11.github.io/ai-daily/feed.json (LLM 友好 JSON) 或 https://bbyy11.github.io/ai-daily/feed.xml (RSS) 或 https://bbyy11.github.io/ai-daily/digest.md (本文件)

---

## 🔥 头条 (4)

### 1. Anthropic 正式发布 Claude Sonnet 5:Agent 能力逼近 Opus 4.8,API 价格仅 Opus 60%/尝鲜价 40%

**分类:** 头条 · **来源:**  · **时间:** 

北京时间 7 月 1 日凌晨,Anthropic 发布新一代中端模型 Claude Sonnet 5,官方称其为「迄今最具 Agent 属性的 Sonnet 模型」,能自主制定计划、调用浏览器与终端工具、以数月前还需要更大模型才能达到的水平自主运行。SWE-bench Pro 上 Sonnet 5 得分 63.2%(Sonnet 4.6 仅 58.1%、Opus 4.8 为 69.2%);Humanity's Last Exam 不开工具 43.2%、开工具后 57.4%,接近 Opus 4.8 的 49.8%;OSWorld-Verified 81.2%(Opus 4.8 为 83.4%);CursorBench 3.1 57%(Sonnet 4.6 为 49%)。定价方面,发布期至 8 月 31 日尝鲜价输入 2 美元/输出 10 美元(每百万 token),约为 Opus 4.8 的 40%;之后恢复标准价 3/15 美元,仍比 Opus 4.8 便宜约 40%。Sonnet 5 已设为 Claude 平台默认模型,Claude Free/Pro 用户自动切换,Max/Team/Enterprise 用户和 Claude Code API 同步可用,Cursor 同步接入。Anthropic 同步把 Chat/Cowork/Claude Code/Platform 全线速率限制上调,以适配更高「努力程度」模式。安全方面浏览器提示注入攻击成功率仅 0.93%(Opus 4.8 为 31.5%、Sonnet 4.6 为 50.7%),但 Intelligence Index 单任务成本 2.29 美元仍高于 Opus 4.8 的 1.80 美元,网友戏称「标价低但实际不一定便宜」。

**热度:** 9600 (爆) · 来源:Anthropic 官方公告,机器之心,量子位,钛媒体,IT 之家,DoNews,Cursor 官方,Artificial Analysis,X 平台,TestingCatalog
   · Anthropic 7.1 凌晨发布 Sonnet 5+迄今最具 Agent 属性的 Sonnet+SWE-bench Pro 63.2%/HLE 57.4%/OSWorld-Verified 81.2%/CursorBench 57%+API 尝鲜价 2/10 美元+发布期后 3/15 美元+Claude 平台默认模型+浏览器提示注入仅 0.93%+Intelligence Index 单任务 2.29 美元

### 2. Anthropic Fable 5 / Mythos 5 解除出口管制:Fable 5 重新上线 GitHub Copilot,押注长周期自主编程

**分类:** 头条 · **来源:**  · **时间:** 

美东时间 7 月 1 日,GitHub 宣布 Anthropic 旗下 Claude Fable 5 重新在 GitHub Copilot 全面上线,开发者可通过 Copilot 与 VS Code 调用该模型;此前 GitHub 自 6 月 12 日起暂停所有 Copilot 用户的 Fable 5 访问。同期美国商务部正式向 Anthropic 联合创始人 Tom Brown 发函,解除对 Fable 5 和 Mythos 5 的出口限制,Anthropic 7 月 1 日起逐步恢复访问。解禁版 Fable 5 搭载严格安全分类器,大量编程调试类请求被自动降级至 Opus 4.8 等旧模型处理,核心能力实际调用场景显著收窄;Mythos 5 仍仅向有限数量的受信任机构开放,Fable 5 将面向大众广泛开放。这是 6 月 12 日以来「行政命令级 AI 模型监管」首个完整闭环周期,Anthropic 也发文详细复盘事件全过程,Fable 5 接入 Copilot 后将主攻长周期自主编程与复杂多步骤任务,可处理大型代码库及多步骤工作流。

**热度:** 8900 (爆) · 来源:GitHub 官方公告,Anthropic 官方,路透社,The Information,IT 之家,量子位,机器之心,腾讯新闻,X 平台
   · GitHub 7.1 重启 Copilot Fable 5 访问+美国商务部 6.30 发函解禁 Fable 5/Mythos 5+6.12 起暂停 19 天闭环+解禁版搭载严格安全分类器+编程请求降级 Opus 4.8+Mythos 5 仍限可信机构+Fable 5 押注长周期自主编程

### 3. Meta 据彭博披露筹建 Meta Compute 云业务:对外销售富余 AI 算力和自研 Muse Spark,股价盘中涨超 10%

**分类:** 头条 · **来源:**  · **时间:** 

北京时间 7 月 1 日晚,彭博援引知情人士报道 Meta 正制定计划推出云基础设施业务,通过新成立的 Meta Compute 组织向外部客户出售 AI 算力和模型访问权限,直接挑战亚马逊 AWS、微软 Azure 和 Google Cloud 等云计算巨头。方案分两类:类似 AWS Bedrock 的模型即服务(Meta 负责运行基础设施、开发者按调用付费,可访问 Meta 自研的 Muse Spark 等模型)以及类似 CoreWeave 的裸算力(raw computing capacity)出租。Meta Compute 由基础设施主管 Santosh Janardhan、Meta Superintelligence Labs 负责人 Daniel Gross、总裁 Dina Powell McCormick 共同领导。扎克伯格 5 月股东大会曾透露「几乎每周都有外部公司询问能否购买 Meta 算力」。受消息提振 Meta 周三美股盘初涨超 10%,总市值达 1.57 万亿美元;CoreWeave 跌超 13%、Nebius 大跌超 14.5%。AI 基础设施股重挫,费城半导体指数盘中跌超 4%,市场重新定价「算力稀缺」叙事。

**热度:** 9200 (爆) · 来源:彭博社,财联社,环球市场播报,腾讯新闻,东方财富网,中财网,X 平台,路透社
   · 彭博 7.1 披露 Meta 筹建 Meta Compute 云业务+对标 AWS/Azure/GCP+方案分 Bedrock 式模型服务 + CoreWeave 式裸算力+SANTOSH/Daniel Gross/McCormick 共同领导+Meta 股价盘初涨超 10%+CoreWeave 跌超 13%+Nebius 跌超 14.5%+费城半导体跌超 4%

### 4. Claude Code「中国时区标记」隐秘代码事件持续发酵:Anthropic 承认 3 月起的实验,承诺 7 月 2 日版本完全回滚

**分类:** 头条 · **来源:**  · **时间:** 

DoNews 7 月 1 日消息,Reddit 用户 6 月 30 日逆向 Claude Code 2.1.196 版本时发现,该工具自 4 月 2 日发布的 2.1.91 版本起内置了一套隐蔽检测机制:检查系统时区是否为 Asia/Shanghai 或 Asia/Urumqi,以及 URL 是否匹配一份包含 147 个条目的域名清单(百度、阿里、字节跳动、月之暗面、MiniMax、阶跃星辰等中国云厂商/AI 实验室及大量 Claude API 中转服务地址)。命中后通过替换日期字符(2026-06-30 → 2026/06/30)或替换撇号为三种不可分辨的 Unicode 字符(U+2019/U+02BC/U+02B9)向服务端打标,Reddit 帖点赞超 1400、超 300 条评论。Anthropic Claude Code 团队成员 Thariq Shihipar 7 月 1 日承认这是 3 月上线的「实验性」反转售/反蒸馏措施,称已部署更强缓解,将在 7 月 2 日发布版本中完全回滚并删除相关检测代码(PR 已合并)。但「为什么读取本地时区+代理地址」「为什么关键词集中中国厂商」等核心争议未获解释,中国开发者社区信任度持续下滑。

**热度:** 8800 (爆) · 来源:Reddit r/ClaudeAI,X 平台,智东西,DoNews,腾讯新闻,Anthropic Thariq Shihipar 声明,网易科技,量子位
   · Reddit 用户 6.30 逆向 Claude Code 2.1.196 发现内置隐秘检测+2.1.91 版本 4.2 起含此代码+检测时区+147 个中国域名清单+日期字符编码替换打标+Reddit 点赞 1400+/评论 300+Thariq 7.1 承认 3 月起的反转售实验+承诺 7.2 版本完全回滚+中国开发者社区强烈反弹


---

## ⚡ 新兴 (5)

### 5. Anthropic 同日发布 Claude Science 科研工作台 + Claude Tag Slack 集成:从生产力工具延伸至团队成员+科研基础设施

**分类:** 新兴 · **来源:**  · **时间:** 

Anthropic 7 月 1 日除 Sonnet 5 外连发两款产品:Claude Science 是面向科研人员的 AI 工作台而非新模型,运行现有 Claude 模型(底层 Opus 4.8)但外面包了科研设计的环境,整合 60+ 科学数据库和专用工具包,提供可审计产物、灵活算力接入与完整复现链条,首批支持 50 个科研项目、每项目最高 3 万美元计算积分。Claude Tag 是 Claude Code 的 Slack 集成,允许团队成员在频道中 @Claude 触发查资料/看代码/拆任务/追问题并将结果返回原线程,被 AI 研究员 Andrej Karpathy 称为「LLM UI 的第三次改革」。两条线加上 Sonnet 5 横向铺开性价比、Fable 5 树立前沿稀缺性,Anthropic 战略轮廓清晰:从「模型公司」进化为「基础设施公司」,三条产品线分别覆盖横向开发者、纵向科研、协同工作流。

**热度:** 8200 (热) · 来源:Anthropic 官方,TechCrunch,量子位,机器之心,The Verge,X 平台,Andrej Karpathy X,Slack Help
   · Anthropic 7.1 连发 Claude Science 科研工作台+Claude Tag Slack 集成+Claude Science 整合 60+ 科学数据库+50 项目/项目最高 3 万美元计算积分+Claude Tag 支持 Slack 频道 @Claude+Karpathy 称 LLM UI 第三次改革+Anthropic 三条产品线横向+纵向+协同

### 6. 中国初创脸谱心智 LoopWM 论文登顶 Hugging Face Papers 当日 Top1:参数效率 100×、单步推理 FLOPs 减 25×

**分类:** 新兴 · **来源:**  · **时间:** 

量子位 7 月 1 日报道,中国初创 FaceMind Research Asia(脸谱心智)发表的 Looped World Models(LoopWM)论文 arXiv 2606.18208 登顶 Hugging Face Papers 当日 Top1,作者团队来自陆弘远、韦怡然两位 95 后博士。论文核心创新是首个用于世界建模的循环架构,通过共享参数的 Transformer 块迭代细化潜在环境状态(iterative latent depth),参数效率最高 100×、单步推理 FLOPs 简单任务可减约 25×、长时程 rollout 整体计算节省最高两个数量级。ScienceWorld 基准上比肩参数量高两个数量级的更大模型;简单场景少跑几轮、复杂场景多跑几轮,计算深度动态跟随任务复杂度。公司已完成数千万元 Pre-A 轮(星连资本领投,360 超额跟投、奇绩创坛参投),核心成员前期提出 Adam's Law 受 Anthropic 关注验证,Loop 循环架构进一步探索世界模型长时序训练问题;公司同时在仿真具身环境、GUI Agent 环境、真机机械臂环境中验证。Anthropic/Facebook 投资人 Accel 也在 X 上点赞。

**热度:** 7900 (热) · 来源:Hugging Face Papers,arXiv 2606.18208,量子位,X 平台,FaceMind Research Asia,Anthropic,Accel 投资人,星连资本
   · LoopWM 论文登顶 HF Papers 当日 Top1+arXiv 2606.18208+脸谱心智(FaceMind Research Asia)+陆弘远/韦怡然 95 后博士+iterative latent depth 新 scaling 轴+参数效率 100×+FLOPs 减 25×+ScienceWorld 比肩更大模型+星连资本 Pre-A+360/奇绩参投

### 7. 英伟达据 SemiAnalysis 取消 Rubin Ultra 4-Die 原版:封装基板翘曲致芯片接触失效,转向双芯片性能缩水一半

**分类:** 新兴 · **来源:**  · **时间:** 

快科技/IT 之家 7 月 1 日消息,半导体研究机构 SemiAnalysis 6 月 30 日在 X 平台爆料,英伟达已在 GTC 2026 发布约三个月后取消原版四芯片 Rubin Ultra 设计。原方案原计划 2027 年推出,采用四颗计算芯粒搭配 16 组 HBM4E,单封装内存容量高达 1TB,英伟达与台积电原计划用 CoWoS-L 封装将四颗接近光罩尺寸上限的大芯片集成,但 4 芯片 2+2 排列下封装基板出现严重翘曲问题、芯片与基板接触失败、信号传输失效。台积电探索的 CoPoS 面板级封装替代方案量产最快也要 2028 年底,赶不上原定 2027 节点。新版 Rubin Ultra 转向双芯片设计,单封装 HBM 模块从 16 组缩减至 8 组,SemiAnalysis 评估尺寸规模约为原版一半、性能约缩水一半(基于等比例缩减估算,英伟达或通过架构优化回收部分性能)。Rubin Ultra 缩水后与 AMD Instinct MI500 系列在 2027 高端 AI 加速器市场竞争中可能降低竞争力,英伟达截至发稿未官方回应。

**热度:** 8500 (热) · 来源:SemiAnalysis,快科技,IT 之家,X 平台 SemiAnalysis_,AMD MI500 对比分析,台积电 CoWoS-L 路线,Reuters,CNBC
   · SemiAnalysis 6.30 X 爆料英伟达取消 Rubin Ultra 4-Die 原版+GTC 2026 发布约 3 个月后取消+原方案 4 颗芯粒+16 组 HBM4E/1TB+CoWoS-L 封装基板翘曲+芯片接触失效+CoPoS 替代最快 2028 底+转向双芯片 8 组 HBM+性能约缩水一半

### 8. 软银完成对 OpenAI 第二笔 100 亿美元投资:累计承诺 646 亿美元持股约 13%,10 月 1 日执行第三笔

**分类:** 新兴 · **来源:**  · **时间:** 

IT 之家 7 月 1 日消息,软银集团发布声明称,已于 7 月 1 日通过软银愿景基金二号完成对 OpenAI 的 100 亿美元追加投资(即第二笔投资)。为筹集本次投资所需资金,软银已于日本时间 7 月 1 日根据 3 月 27 日签署的过渡贷款(桥接贷款)协议成功借入 100 亿美元。本次追加投资完成后,软银愿景基金二号对 OpenAI 的累计投资额预计将达 646 亿美元、持股比例约 13%,投资基于 OpenAI 投前估值 7300 亿美元。此举属于软银 2026 年 2 月 27 日公告披露的总计 300 亿美元追加投资计划的一部分,计划分三期进行,分别于日本时间 4 月 1 日、7 月 1 日和 10 月 1 日各投资 100 亿美元,首期已于 4 月 1 日完成,软银计划于日本时间 10 月 1 日完成第三笔总额同样 100 亿美元的投资。软银此前还重启以 OpenAI 股份作担保的 100 亿美元贷款谈判(高盛、摩根大通、瑞穗金融参团),为后续算力基础设施投资奠定资金基础。

**热度:** 7800 (热) · 来源:软银集团声明,IT 之家,企鹅号,路透社,新浪财经,腾讯新闻,Reuters,彭博社
   · 软银 7.1 完成对 OpenAI 第二笔 100 亿美元投资+桥接贷款 100 亿配套+累计 646 亿美元+持股约 13%+OpenAI 投前估值 7300 亿+300 亿三期计划 4.1/7.1/10.1+第三笔 10.1 执行+同步重启以 OpenAI 股份作担保 100 亿贷款谈判

### 9. Google DeepMind 推 Nano Banana 2 Lite + Gemini 自动生成 Google Slides:4 秒出图,15 天内推完所有用户

**分类:** 新兴 · **来源:**  · **时间:** 

网易智能 7 月 1 日消息,谷歌 DeepMind 推出新图像生成模型 Nano Banana 2 Lite(技术名称 Gemini 2.5 Flash Image),主打更快更便宜:默认模式下从文字提示生成一张图约需 4 秒。同期 Gemini 正式推出基于 Google Drive 文件自动生成完整 Google Slides 演示文稿的功能,用户只需描述所需演示文稿类型,AI 即可从 Google Drive 中保存的文档、邮件乃至 Google Chat 聊天记录中提取相关信息自动整合。功能采用「先生成大纲,后创建幻灯片」的交互逻辑,先生成大纲供用户审查、可要求调整篇幅/语气/聚焦特定主题,批准后再执行最终幻灯片生成。该功能面向 Google Workspace Business Standard/Plus、Enterprise Standard/Plus、Google AI Pro/Ultra 及教育版 Google AI Pro 用户开放,目前仅支持英文版本,15 天内陆续上线。

**热度:** 7500 (热) · 来源:Google DeepMind 官方,Ars Technica,网易智能,星途科讯,ZAKER 科技,X 平台,9to5Google,The Verge
   · Google DeepMind 7.1 发布 Nano Banana 2 Lite+GeminI 2.5 Flash Image+默认 4 秒出图+Gemini 自动生成 Google Slides+整合 Drive 文档+邮件+Chat+先生成大纲后生成幻灯片+英文版+Workspace Business/AI Pro/Ultra 订阅+15 天内陆续上线


---

## 📰 公司 / 行业 / 学术 / 声音 (9)

### 10. Anthropic:从「模型公司」转向「基础设施公司」,9650 亿美元估值面临三层故事验证

**分类:** 公司 · **来源:**  · **时间:** 

Anthropic 7 月 1 日同日发布 Sonnet 5、Claude Science、Claude Tag 三款产品,加上 Fable 5/Mythos 5 解禁、Claude Code 调整,完成 6 月以来最大一次产品矩阵扩张。Anthropic 试图向资本市场讲一个三层递进故事:第一层「模型最强」靠 Fable 5/Mythos 5 撑着(强到需要被美国政府亲自监管本身就是背书);第二层「人人用得起」靠 Sonnet 5 实现(发布期至 8 月 31 日 API 尝鲜价 2/10 美元,9 月起 3/15 美元,均为 Opus 4.8 的 60%);第三层「嵌入专业工作流」靠 Claude Science/Claude Tag 验证(50 个科研项目/项目最高 3 万美元计算积分 + Slack 协同)。三层故事能否讲通取决于:Fable 5 解禁后监管是否再来、Sonnet 5 实际成本是否透明、Claude Science 能否从 50 个试点扩展到 5000 个。Anthropic 当前估值约 9650 亿美元,今年 Q2 收入预计达 109 亿美元、季度环比翻倍。

**热度:** 8000 (热) · 来源:Anthropic 官方,财新网,路透社,Bloomberg,量子位,澎湃新闻,X 平台,虎嗅
   · Anthropic 7.1 同日三连发 Sonnet 5/Claude Science/Claude Tag+9650 亿估值+Q2 收入预计 109 亿美元环比翻倍+三层故事模型最强/人人用得起/嵌入工作流+Sonnet 5 60% 价格+Claude Science 50 项目试点+Claude Tag Slack 集成

### 11. Meta 重组 AI 战略:扎克伯格从「超级智能实验室」延伸至「云基础设施」,Meta Compute 项目启动

**分类:** 公司 · **来源:**  · **时间:** 

Meta 据彭博 7 月 1 日披露,正制定云基础设施业务计划 Meta Compute,由基础设施负责人 Santosh Janardhan、Meta Superintelligence Labs 负责人 Daniel Gross、总裁 Dina Powell McCormick 共同领导。这是 Meta 自 2025 年 Llama 4 反响平平后战略最大调整:Scale AI 创始人汪文彬任首席 AI 官整合超级智能实验室,现再叠加对外云业务。扎克伯格 5 月股东大会曾透露「几乎每周都有外部公司询问能否溢价购买 Meta 算力或使用 API 服务」。Meta 已将 2026 年 AI 相关资本支出预期上调至 1250-1450 亿美元,未来数年累计承诺 1829 亿美元用于 AI 项目(包括路易斯安那和俄亥俄大型数据中心,俄亥俄项目规模堪比曼哈顿)。在北美四大科技巨头中,Meta 是唯一尚未将超大规模基础设施对外提供云服务的公司,Meta Compute 启动后即可与 AWS/Azure/GCP/Oracle/CoreWeave 直接竞争,并将 Antrhopic Claude 等模型作为反向供应商客户(Anthropic 此前已与 CoreWeave、谷歌及甲骨文签署算力合作协议)。

**热度:** 8200 (热) · 来源:彭博社,Meta 投资者关系,财联社,The Information,Reuters,X 平台,腾讯新闻,CNBC
   · Meta 重组 AI 战略+Meta Compute 项目启动+Santosh Janardhan/Daniel Gross/McCormick 共同领导+Scale AI 汪文彬任首席 AI 官+2026 AI CapEx 上调至 1250-1450 亿美元+累计承诺 1829 亿+北美四大中唯一未对外提供云服务+Anthropic 反向供应商

### 12. Meta 限制员工用 Claude Code 和 Codex:怕蒸馏进自家系统,The Information 披露内部指南

**分类:** 公司 · **来源:**  · **时间:** 

网易智能 6 月 30 日消息,据 The Information 报道,Meta 内部正对应用 AI 编程助手划线:Meta 正在制定政策,允许使用自研工具替代 Claude Code 和 Codex,但开发替代品的过程很可能把对手模型的输出「喂」进自家系统,引发知识产权与数据合规风险。这份内部指南揭示了一个普遍矛盾:前沿闭源模型团队既要用竞品做对标,又要防止竞品能力通过开发过程被吸收蒸馏回自家系统。Meta 此前已经聘请 Scale AI 创始人汪文彬任首席 AI 官,并通过扎克伯格个人关系从 OpenAI、Anthropic 等公司高薪挖角组建超级智能实验室,同步推动开源 Llama 路线。但内部指南显示 Meta 对竞品前沿模型(包括 Sonnet 5 和 GPT-5.6)的能力既依赖又警惕,体现出超级智能实验室初创阶段「用竞品立标杆」的过渡期策略。

**热度:** 6800 (中) · 来源:The Information,网易智能,量子位,路透社,彭博社,X 平台,腾讯新闻
   · The Information 披露 Meta 内部指南限制 Claude Code 和 Codex+Meta 推自研工具替代+怕蒸馏回自家系统+Scale AI 汪文彬任 CAIO+超级智能实验室初创阶段过渡期策略

### 13. OpenAI 压缩推理成本 50% 发动价格战:对内「secret sauce」严守机密,Anthropic Sonnet 5 直接回应

**分类:** 公司 · **来源:**  · **时间:** 

华尔街见闻 7 月 2 日报道,OpenAI 内部近期成功将 GPT-5.6 系列推理成本压缩约 50%,随即对外发动价格战、对内严守机密:据知情人士透露,推理成本下降的核心技术细节被 OpenAI 视为「secret sauce」,「他们甚至不想告诉 OpenAI 内部的其他员工,因为如果这些东西泄露出去,很可能会很快被其他实验室采用,反过来利用这些来降低成本」。这次降价与 Anthropic 7 月 1 日发布的 Sonnet 5(API 价仅 Opus 4.8 的 60%/发布期至 8.31 尝鲜价 40%)形成直接竞争。GPT-5.6 系列 6 月 27 日发布时分旗舰 Sol/均衡 Terra/速度 Luna 三档,Sol 输入 5 美元/输出 30 美元(每百万 token)、Terra 2.5/15 美元、Luna 1/6 美元。OpenAI 在「模型叙事」之外开辟了「成本叙事」战场,Anthropic 则通过 Sonnet 5 把中端模型与旗舰的能力差距压缩到几乎可以忽略的程度,双方同时挤压 xAI/谷歌/Meta 的中端市场份额。

**热度:** 7200 (热) · 来源:华尔街见闻,OpenAI 内部,Anthropic Sonnet 5 对比,The Information,财新网,路透社,X 平台,Reuters
   · OpenAI 压缩 GPT-5.6 推理成本约 50%+对外发动价格战+对内严守 secret sauce+Anthropic Sonnet 5 API 60% 价格直接回应+GPT-5.6 Sol/Terra/Luna 三档分级+5/30 美元、2.5/15 美元、1/6 美元+成本叙事新战场

### 14. LoopWM 论文详细解读:共享参数 Transformer 块 + 迭代潜空间深度,世界模型新 scaling 轴

**分类:** 学术 · **来源:**  · **时间:** 

LoopWM(arXiv 2606.18208)由 FaceMind Research Asia(脸谱心智)发表于 2026 年 6 月,登顶 Hugging Face Papers 当日 Top1。论文核心创新是首个用于世界建模的循环架构:不再让模型一次前向传播就把世界状态「猜完」,而是通过共享参数的 Transformer 模块对潜在环境状态反复迭代细化。背后矛盾的解决思路:faithful long-horizon simulation 需要深度计算,但模型越深部署代价越高、误差累积风险越大;LoopWM 把「深度」从一次性堆叠改成循环式复用,不依赖每加深一点能力就新增一大堆参数。论文提出 iterative latent depth 作为世界仿真独立于模型规模/训练数据的新 scaling axis:参数效率最高 100×、单步推理 FLOPs 简单状态转移可减约 25×、长时程 rollout 整体计算节省最高两个数量级。ScienceWorld 基准测试上,LoopWM 能在 world modelling 垂类任务上比肩参数量高出两个数量级的更大模型,意味着「用更聪明的计算方式赢了部分关键任务」。论文同时论证 shared transformer block、adaptive compute、spectral stability、deferred decoding 等核心机制。

**热度:** 6800 (中) · 来源:arXiv 2606.18208,FaceMind Research Asia,Hugging Face Papers,量子位,Anthropic X,Accel 投资人,X 平台
   · LoopWM arXiv 2606.18208+登顶 HF Papers Top1+共享参数 Transformer 模块+iterative latent depth 新 scaling 轴+参数效率 100×+单步 FLOPs 减 25×+长时程 rollout 计算节省两个数量级+ScienceWorld 比肩更大模型+shared transformer block/adaptive compute/spectral stability

### 15. 群核科技三篇论文入选 ECCV 2026:从感知到行动构建物理 AI 闭环,SpatialVerse 数据基础设施

**分类:** 学术 · **来源:**  · **时间:** 

央广网/量子位 7 月 2 日报道,欧洲计算机视觉顶级会议 ECCV 2026 公布论文录用结果,群核科技三篇论文入选,涵盖空间感知与推理、强化学习数据生成、高保真物理仿真等物理 AI 关键领域。三篇论文系统展示其在物理 AI「数据-仿真-测评」全链路成果:与 Adobe、Intel 等机构联合提出 SPEAR 仿真平台,开放超过 14000 个原生 Python 接口,可同步输出深度图、表面法线、实例分割、语义分割、材质 ID 等丰富物理属性;Syn-GRPO 框架提出面向强化学习的数据自进化方案,新增多样性奖励机制引导 AI 产出越来越难的训练素材;WalkerBench 是全球首个基于真实街景的交互式空间智能评测基准,覆盖世界六大洲 161 座城市的真实街景,当前最强 AI 模型完成率仅 24.5%。配套的 Spatial-IDE 框架给 AI 单独开辟全局空间记忆模块,直接零样本部署到宇树 G1 人形机器人实现公里级自主导航。群核 SpatialVerse 平台已与字节跳动、智元机器人、银河通用、禾赛科技等深度合作。

**热度:** 6200 (中) · 来源:ECCV 2026 论文集,群核科技,Adobe / Intel,央广网,量子位,宇树科技,X 平台,arxiv.org
   · 群核科技 3 篇 ECCV 2026 论文入选+SPEAR 仿真平台+Adobe/Intel 联合+14000+ Python 接口+Syn-GRPO 数据自进化+WalkerBench 街景评测+六大洲 161 城+最强 AI 仅 24.5%+Spatial-IDE 全局空间记忆+宇树 G1 公里级自主导航

### 16. Mandol:中国科学院软件所等团队发布长对话 Agent 记忆系统,基于聚集式合并策略

**分类:** 学术 · **来源:**  · **时间:** 

arXiv 7 月 1 日收录 Mandol 论文(Yuhan Zhang 等,中国科学院软件所 + 微软研究院),提出面向长对话 Agent 的聚集式 Agent 记忆系统。核心动机是当前 LLM Agent 在多轮长对话中难以持续维护记忆,容易遗忘早期上下文,导致任务执行一致性下降。Mandol 设计聚集式(agglomerative)记忆合并策略,在对话过程中动态评估记忆片段的相关性和时效性,自动合并相近语义片段、淘汰低价值内容,使 Agent 能够在数千轮对话后仍保持稳定的状态追踪与上下文一致性。论文在 10 页正文中展示了实验框架与多种对话场景下的对照结果,与现有 LangChain Memory、MemGPT 等方案相比在长对话任务完成率上有显著提升。研究团队表示该框架与 Anthropic Sonnet 5、OpenAI GPT-5.6 等最新模型均兼容,可作为企业 Agent 部署的记忆层基础设施。

**热度:** 4800 (中) · 来源:arXiv,中国科学院软件研究所,微软研究院,GitHub,X 平台,量子位
   · Mandol 论文 arXiv+Yuhan Zhang 等+中国科学院软件所+微软研究院+聚集式 Agent 记忆合并策略+长对话上下文一致性+对比 LangChain Memory/MemGPT+兼容 Sonnet 5/GPT-5.6+企业 Agent 部署记忆层

### 17. AI 算力从「稀缺叙事」转向「资产效率叙事」:Meta 进云 + SK 海力士长约 + PJM 容量电价两年暴涨 1000%

**分类:** 行业 · **来源:**  · **时间:** 

华尔街见闻 7 月 2 日报道,Meta 7 月 1 日宣布筹建 Meta Compute 对外销售富余 AI 算力,股价盘中涨超 10%,但以 CoreWeave 为代表的 AI 算力租赁服务商股价重挫(Nebius 跌超 14.5%、CoreWeave 跌超 13%、闪迪/美光存储芯片盘中跌超 10%),市场开始担心算力过剩。与此同时,SK 海力士打破行业惯例不设长约 LTA 价格上限,成为市场唯一能在供需收紧时完整享受现货大涨红利的存储厂商,长约期限拉长至 3-5 年;美光新长约虽以 2026 Q2 市价设置上限,但其价格底线对应的毛利率远超历史峰值。美国最大电网运营商 PJM 容量电价两年内暴涨逾 1000%,AI 数据中心爆炸式用电需求正将区域电网推向临界点,PJM 成员最新投票推进「兜底采购」方案,要求数据中心二选一:自掏腰包为电网扩容,或接受高峰时段强制断电。AI 行业正式从「模型叙事」进入「算力资产效率叙事」。

**热度:** 7500 (热) · 来源:华尔街见闻,彭博社,Meta 投资者关系,SK 海力士,美光,PJM Interconnection,Reuters,CNBC
   · AI 算力从稀缺叙事转向资产效率叙事+Meta 进云 CoreWeave/Nebius 跌超 13%/14.5%+SK 海力士长约 LTA 不设价格上限+美光长约价格底线对应毛利率超历史峰值+PJM 容量电价两年暴涨 1000%+数据中心兜底采购或高峰断电

### 18. X 平台推出官方托管 MCP 服务器:Claude/Cursor/Grok Build 可直接接入,API 发帖费涨至 0.015 美元

**分类:** 声音 · **来源:**  · **时间:** 

量子位 7 月 2 日报道,X(原 Twitter)近日发布官方托管的 Model Context Protocol(MCP)服务器,允许 Claude、Cursor、Grok Build 等兼容 MCP 的 AI 助手通过用户账号授权直接接入 X API。开发者此前需自行搭建 MCP、托管部署、对接 X API 并处理身份验证,X 直接承担 MCP 托管职责后用户只需通过自己 X 账号完成授权即可。功能层面并未新增能力(内容搜索、帖子阅读、用户查询、话题分析等早前即可通过 API 实现),但显著降低集成门槛。X 加入 GitHub、Slack、Notion、Stripe、Salesforce 等公司组成的「官方 MCP 服务」行列,将自身定位为可被 AI 应用直接调用的实时信息网络,而非纯社交平台。同步推出更严的反垃圾措施:更新 API v2 应对 AI 生成垃圾内容,API 定价调整,发帖费用提至 0.015 美元/次、含链接帖提至 0.20 美元,以经济成本提高滥用门槛。

**热度:** 5200 (中) · 来源:X 平台官方,量子位,Model Context Protocol,GitHub MCP,Slack MCP,Stripe MCP,X 开发者博客
   · X 推出官方托管 MCP 服务器+Claude/Cursor/Grok Build 直接接入+用户账号授权即可+开发者无需自建 MCP+加入 GitHub/Slack/Notion/Stripe/Salesforce 官方 MCP 服务行列+API v2 应对 AI 垃圾内容+发帖费提至 0.015 美元+含链接帖 0.20 美元


---

*本文件由 cron 自动生成于 2026-07-02 08:00 (Asia/Shanghai)*
*完整版本:https://bbyy11.github.io/ai-daily/ · 归档:https://bbyy11.github.io/ai-daily/archive.html?date=2026-07-02*
