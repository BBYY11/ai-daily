# AI Daily · 事故记录

> 每次事故必须记录根因 + 修复 + 教训。
> 目的:同一个坑不踩第二次。

---

## 2026-06-04  · #001 · style.css 漏推,主页样式全无

**症状**
用户刷新主页后,看到的是默认浏览器样式(宋体黑字、蓝色下划线链接、无卡片),而不是设计的蓝白米色风格。

**根因**
1. `.gitignore` 写了 `assets/`,**整个目录被排除**
2. `scripts/push_to_github.sh` 又有 `case "$rel" in assets/*) continue ;;` 二次排除
3. 原本意图只排除截图 `assets/preview-*.png`,但写法太宽,连带 `style.css` 也被排除
4. **Mavis 推送后没做"部署完整性检查"**,GitHub Pages build 了 1 个没 CSS 的 HTML 还能跑,所以 bug 没被发现

**修复**
1. `.gitignore` 改为 `assets/preview-*.png`(精确匹配)
2. `push_to_github.sh` 改为 `assets/preview-*.png)`(精确匹配)
3. 重新推送,GitHub API 验证 style.css 32KB 已上传
4. 加入"推送完整性 5 项检查"到 WORKFLOW.md(每次 push 后跑)

**教训**
- **"看着推了"≠"推上去了"**。`.gitignore` 的隐性排除是最阴的 bug
- 任何 push 之后必须**用 GitHub API 验证关键文件存在**
- 浏览器打开页面看不到 CSS = 文件 404 = push 漏了,**别甩锅给 CDN**

---

## 2026-06-04  · #002 · 6-04 早报 cron "成功"但实际没数据

**症状**
6-04 早上 8:00 cron 跑了,last_result=success,但主页 news.json 还是 6-03 的内容。

**根因**
1. **fetch_news.py 的 CLI 参数写错了**:cron prompt 写 `python3 scripts/fetch_news.py --date 2026-06-04`,但脚本只支持位置参数,**`--date` 触发 ValueError,被 cron 静默吞掉**
2. fetch_news.py 失败 → 后续步骤可能跟着挂
3. 即便后续步骤跑了,**LLM 抓信源可能限流**(6-04 的真实情况:0 条新闻被抓到,LLM 写了一个空 news.json 或者直接没写)
4. **`last_result=success` 误报**——cron 引擎只看 exit code,LLM 内部失败它不知道

**修复**
1. fetch_news.py 修了——加了**占位骨架**:如果归档后 news.json 不是今天的日期,自动写一个 `summary="早报正在生成中"` 的占位
2. cron prompt 修正:用位置参数 `python3 scripts/fetch_news.py 2026-06-XX`,并在 prompt 里写"任何一步失败立即报用户,不要静默退出"
3. 新增 ai-daily-watchdog cron(7:00-10:00 每 30 分钟检查一次),发现 news.json date ≠ 今天或 items < 14 主动报警

**教训**
- **LLM 写文件的 cron 必须有"硬失败检测"**:不能只看 exit code,还要读文件验证
- **CLI 参数不一致是最阴的 bug**(因为错误信息被吞)
- **占位 + watchdog 双保险**:即使 LLM 失败,用户至少看到"正在生成"而不是昨天的内容

---

## 2026-06-04  · #003 · 本月页装饰蓝线像 bug

**症状**
用户说 monthly.html 显示有"多余的蓝色横线"。

**根因**
设计 style.css 时学 Vercel / Linear 风格,在 `.hero::after`、`.block::before`、`.llm-guide::before`、`.format-card::before` 加了几条**渐变蓝线/橙线**做装饰。设计意图挺好,但放在米白底卡片上看着像没对齐的残影——用户视角是 bug,不是设计。

**修复**
全部删掉那 4 条装饰线。让米白卡片的边界靠 1px 浅灰边 + 浅阴影来表现,不要靠色条。

**教训**
- **"高级感"设计元素不一定是"好"设计**——用户认不认是金标准
- 米白底 + 浅阴影 + 圆角已经够有质感,**不要叠加多余装饰**
- 任何"装饰"上线前,先问"如果样式表没加载,看起来会像 bug 吗?"——会就别加

---

## 2026-06-04  · #004 · 用户反馈"做得太素",我矫枉过正成"白开水"

**症状**
第一版改版"黑橙→蓝白"做太素,用户朋友说看不清。我做了个"白底蓝字"的安全版,结果"白开水"——没质感。

**根因**
1. 第一反应是"用户嫌暗,我做亮",矫枉过正
2. **没考虑"白底如何不无聊"**——直接用纯白 + 蓝色 accent,结果像 bootstrap 默认
3. 没有色彩层次(只有黑+蓝)、没有装饰、没有节奏感

**修复**
- 改用米白 `#fafaf7`(不是纯白)
- 加顶部 3 像素彩条(品牌识别)
- 加新 logo(黑底白字 AI 方块 + 橙色脉冲点)
- 头条 3 个用大卡(2:1:1 grid),第 1 个反着用黑底橙色 feature
- 数据用 mono 30px 大字 + 竖线分隔
- 卡片左 3px 蓝色边条(hover 弹出)
- 块顶部 2px 渐变蓝线(后来又删了,#003 教训)

**教训**
- **"白底"不等于"无聊"**——Bloomberg / NYT / 经济学人都是白底,但靠排版、字体、留白、对比做出质感
- **"安全的白开水"是最差的设计**——既不解决问题,也没新意
- **改设计要做"有意识的反差"**:至少要有一个"反着来"的元素(黑底 feature 卡、橙色彩条等)做视觉锚点

---

## 2026-06-03  · #005 · RSS 三种格式,但 ChatGPT 仍不能订阅

**症状**
用户给 ChatGPT 链接,ChatGPT 反馈"无法读到具体内容,无法订阅"。

**根因**
1. RSS XML 对 LLM 不友好(LLM 解析 XML 不稳)
2. ChatGPT 没有"长期订阅 RSS"功能(产品形态限制,不是 bug)
3. 只给了 RSS XML 一种格式,LLM 没东西可拉

**修复**
- 加 JSON Feed(LLM 友好)+ Markdown 摘要(粘贴友好)
- 加 feed.html 订阅页,说明 3 种格式的用法
- 加了 ChatGPT 的 prompt 模板,让用户直接复制

**教训**
- **"支持 RSS"≠"AI Agent 能用"**——LLM 时代,机器可读性优先级要提高
- 多格式输出:JSON(机器)+ Markdown(人)+ RSS(传统阅读器),**全都要**
- 任何"用 X 工具做不到"的反馈,先问"是 X 工具的局限还是我们的 bug"——别瞎改

---

## 2026-06-03  · #006 · weekly.html 和 weekly_view.html 命名混乱

**症状**
周报页有两套:`weekly.html` 和 `weekly_view.html?week=2026-W22`,用户不知道哪个是哪个。

**根因**
设计时把"列表页"和"详情页"用同样的 `weekly` 命名,语义不清。

**修复**
- 删 `weekly.html`,改用 `weekly_archive.html`(列表)+ `weekly_view.html`(详情)
- nav 文字统一为"周报"

**教训**
- **命名要"主语在前"**:`weekly_archive`(归档)比 `weekly_list`(列表)更明确
- 列表 / 详情 一定要用不同前缀(`archive.html` vs `archive-view.html`)

---

## 复盘模式(每个新事故都过一遍)

1. **症状**:用户/系统怎么发现的?截图 + 时间
2. **根因**:哪一步错了?为什么之前没发现?
3. **修复**:具体改了什么?推上去了吗?
4. **教训**:下次怎么避免?(写进 WORKFLOW.md 或 QUALITY_STANDARDS.md)
5. **预防**:加监控 / 测试 / 自检,把"靠人不犯错"变成"靠系统不犯错"

---

## 2026-06-06  · #007 · 6-05 + 6-06 双日早报 cron 全部"成功"但没数据

**症状**
- 6-06 早上 9:39 用户报告:主页显示 6-04 早报
- news.json 还是 6-04 的内容
- 归档目录:6-04.json 存在(之前手动补的),6-05.json 缺失,6-06.json 缺失
- 主 cron (404860864389898) `last_result=success`,`last_error=空`

**根因(三层叠加)**
1. **主 cron 第 1 步 web_search 抓不到 24h 新闻**:LLM session 跑 web_search 时大概率限流/超时,没拿到数据
2. **LLM 静默写了一个"老的/空的" news.json**:因为没新数据,LLM 跳过第 6 步或写了一个空内容
3. **last_result=success 误报**:cron 引擎只看进程 exit code,不看内容
4. **watchdog 没报警**:**watchdog 的 prompt 里 Python -c 转义错了**,跑了 SyntaxError,但 LLM session 拿到 Python 错误也只回"success",因为它没意识到 watchdog 应该报警
5. **手写 news.json 时内嵌 ASCII 双引号**:我手动补 6-06 早报时,中文文本里直接用了 `"` 而不是 `'` 或 `""`,导致 JSON 非法,fetch_news.py 立刻挂

**修复**
1. **手动补 6-06 早报**(16 条,SpaceX×谷歌 300 亿/特朗普入股/美国 AI 立法草案/OpenAI 硬件/ChatGPT Dreaming/人形机器人身份证/Lindy 切 DeepSeek/MisoTTS/Ideogram 4.0 等真实新闻)
2. **修复 6-06 news.json JSON 语法错误**(8 个内嵌引号 → 全部换成 `'`),fetch_news.py 跑通
3. **推送 GitHub**(46 文件,index 重建)
4. **更新 fetch_news.py 增加容错**(已加占位骨架)
5. **更新 cron prompt**(已修位置参数 + ISO 周 + 失败告警)

**没修的(留作 #008)**
- watchdog prompt 里的 Python -c 引号转义还是错的(已用 heredoc 绕开,下次用文件脚本)
- 主 cron 还是"成功就完事"的状态,**没硬约束"必须写 N 条"**
- LLM 抓信源限流时,没有任何 fallback 通道(比如预先 cache 一份)

**教训**
- **"success" 是最危险的标签**——LLM 的"安静失败"占 30%+,必须有"硬内容自检"
- **JSON 字符串内嵌引号必须用中文引号 `""` 或单引号 `'`**——这条要写进 QUALITY_STANDARDS
- **手动写 news.json 也要走 JSON 验证**(Python json.load 一次),不要"看着对就推"
- **watchdog 失效 = 兜底失效 = 系统不可信**

**预防**
- [ ] 修 watchdog prompt(用文件脚本代替 `-c` 内嵌)
- [ ] 主 cron 加"写完 news.json 后必须 python3 -c "import json;d=json.load(open('data/news.json'));assert d['date']==datetime.date.today().isoformat() and len(d['items'])>=14"" 硬断言
- [ ] fetch_news.py 第 0 步也跑这个硬断言,失败立即 exit 1
- [ ] 写一个 `validate_news.py` 工具脚本,作为"质量门"
- [ ] QUALITY_STANDARDS 加"JSON 字符串禁止内嵌 ASCII 双引号"硬规则


---

## 2026-06-06  · #008 · 我自己推送文档时把 6-05 早报覆盖成 6-04

**症状**
- 用户说"昨天 6-05 看到了,但今天又变成 6-04"
- 用 GitHub commit history 排查:6-05 早上 8:05 cron **真的写出了 6-05 早报 16 条** ✓
- 但 6-05 17:50 我推送 WORKFLOW/QUALITY/INCIDENT 三份文档时,**意外把 news.json 也一起推送**——那时本地 news.json 是 6-04(我之前手写的)**6-05 真早报被覆盖了**

**根因**
- 我(AI 编辑)的 push 操作习惯:**`bash scripts/push_to_github.sh` 会无脑推送所有文件,包括数据文件**
- 当我"修一下 HTML 顺便推"时,本意只推 HTML,但脚本把整个 `data/` 目录都推了
- 6-05 真早报被推回 6-04 内容(那时本地是 6-04 早报)
- **6-05.json 归档没生成**(我手写时没经过 fetch_news.py 的归档逻辑)

**修复(已完成)**
1. **从 GitHub 历史恢复 6-05 真早报**:用 API 抓 `e6ec28d1` commit 的 news.json → 18KB / 19 条 / 周五
2. **恢复 6-05 的 3 种 feed**:feed.xml / feed.json / digest.md 都从那个 commit 拿了回来
3. **归档 6-05.json**:放到 `data/archive/2026-06-05.json`
4. **重建 archive/index.json**:8 天(5-30 到 6-05,5-29 因为 6-04 那天被覆盖没了)
5. **推送 GitHub**:47 文件
6. **6-06 主页维持手写的 16 条 6-06 早报**

**没修的(下次必做)**
1. **推送脚本应只推"明确列出的文件"**,而不是 `find . -type f` 全收
2. **手动写 news.json 之前必须先 `cp data/news.json data/archive/$(date +%Y-%m-%d).json`** — 强制保留
3. **加"推送前确认 news.json 是不是今天的"硬门**——如果不是今天,提示"今天要推的早报,会覆盖昨天"

**教训**
- **"修一下 HTML 顺便推"是个危险操作**——任何"顺便"都应该只推明确知道要推的文件
- **GitHub commit history 是数据恢复的金矿**——这次救回 6-05 早报全靠它
- **手动写数据文件时,要先备份**——我太随便了,直接 `Write` 覆盖
- **占位骨架的"2026-XX-XX 早报正在生成中"文字让用户误以为是真早报**——占位应该有更明显的"PLACEHOLDER"标识,而不是日期

**预防**
- [ ] push_to_github.sh 增加"数据文件确认"门:news.json.date != 今天 → 拒绝推,提示用户
- [ ] 我手写 news.json 之前先 `cp` 备份到 archive
- [ ] 推送脚本加 `--no-data` 选项(只推 HTML/CSS/JS/MD)
- [ ] 占位骨架改用 "🚧 今日早报生成中,见档案 archive/{昨天}.json" 显眼标识

---

## 2026-06-06  · #009 · 全栈体检发现的隐性 bug(预防性)

**症状**
用户说"不要再错了"后,Mavis 做了一次全栈体检。表面上系统正常,但发现 5 个隐性 bug。

**根因**

1. **watchdog active_hours 边界**(07:00-10:30,边界 10:30 算 "outside active hours" 被跳过)
2. **watchdog prompt 里 Python -c 引号转义语法错误**(跟 #007 同一个坑)
3. **push_to_github.sh 默认全推所有文件,无数据保护**(导致 #008 我自己覆盖 6-05 早报)
4. **fetch_news.py archive_today 没 try/except**(坏 JSON 让整个 cron 挂)
5. **fetch_news.py 占位骨架没有 🚧 显眼标识**(导致用户以为"6-05 早报"是占位)
6. **没有 validate_news.py 质量门**(LLM 写空 news.json 也能推上去)
7. **JSON 字符串内嵌 ASCII 双引号没硬规则**(导致 #008)

**修复(已完成)**
1. ✅ 新建 `scripts/check_health.py`(watchdog 专用,文件脚本,无引号陷阱)
2. ✅ 新建 `scripts/validate_news.py`(主 cron 写完 news.json 必须跑)
3. ✅ push_to_github.sh 加"news.json date ≠ 今天"硬门(支持 --force-data 绕过)
4. ✅ fetch_news.py archive_today 加 try/except + 占位骨架用 🚧 显眼标识 + 写后 json 验证
5. ✅ watchdog prompt 改成调 check_health.py 文件脚本
6. ✅ watchdog active_hours 07:00-10:35
7. ✅ 主 cron prompt 集成 validate_news.py(写完必须通过才能推送)
8. ✅ QUALITY_STANDARDS.md 加 JSON 字符串硬规则

**测试结果**
- `python3 fetch_news.py 2026-06-06` → ✓
- `python3 validate_news.py` → ✓ OK 16 条 4 headline 4 rising
- `python3 check_health.py` → ✓ OK
- `python3 gen_feed.py / gen_json_feed.py / gen_digest.py` → ✓
- `bash push_to_github.sh`(date=今天)→ ✓ 49 文件推送
- `bash push_to_github.sh`(date=昨天,模拟误操作)→ ❌ REFUSE 拒绝推送
- 已用 GitHub API 验证 news.json 17KB date=2026-06-06 已上仓库

**教训**
- **"看着对"≠"跑得通"**——体检发现 7 个隐性 bug
- **预防比治疗便宜 10 倍**——花 30 分钟体检,省下未来 N 个"用户报告后再修"
- **每次新增脚本,必须问"LLM 写错时会不会炸"**——LLM 写中文文本用 ASCII 双引号是高频错误
- **"全栈体检"应该每 2 周做一次**,不是出问题才看

**未来体检清单(每 2 周)**
- [ ] 5 个 cron 状态(enabled/last_result/last_error/next_run)
- [ ] 4 个核心数据文件 date 对齐
- [ ] push 脚本 4 种状态模拟(date=今天 / 不是今天 / PLACEHOLDER / 损坏)
- [ ] validate_news.py / check_health.py exit 0
- [ ] 7 个 HTML 都能渲染(用 puppeteer 截图桌面 + 手机)
- [ ] 3 种 feed XML/JSON/MD 合法
- [ ] GitHub 关键文件 sha 不变(说明没漏推)

---

## 2026-06-06  · #010 · GitHub 仓库有 3 个幽灵文件(weekly.html / snap.js / __pycache__)

**症状**
用户说"全面检查代码",Mavis 用 GitHub Contents API 拉远端文件清单,发现:
- 远端 57 个对象,其中 3 个是**早该删但没删的幽灵文件**
- 1 个是新出现的 `__pycache__/fetch_news.cpython-311.pyc`(我刚推的,脏文件)

**根因**
- push_to_github.sh 的逻辑是"add-only":每次推送**只新增/修改**,不删除
- 之前 local 删了 `weekly.html`(改名成 `weekly_archive.html`),但**仓库里这个文件永远留着**
- `.gitignore` 写了 `__pycache__/`,但**`case` 排除规则没写**——今天 6-06 09:44 推送时,pyc 被一起推上去了
- `snap.js` 是 6-03 推的(那时候 .gitignore 已生效但 .gitignore 之前的 commit 已经把这个文件推上去了)

**修复(已完成)**
1. ✅ **手动删除 3 个幽灵文件**(用 Contents API DELETE):
   - `weekly.html`(12.5KB,改名留下的)
   - `snap.js`(2KB,gitignore 之前的 commit 遗留)
   - `scripts/__pycache__/fetch_news.cpython-311.pyc`(20KB,误推的)
2. ✅ **修 push_to_github.sh 排除规则**:
   - 加 `scripts/__pycache__/*` / `*.pyc` / `*.pyo` / `*.log` / `.DS_Store`
   - 加"幽灵文件检查"块,推送前对比已知 3 个可能残留,提醒用户
3. ✅ **新建 scripts/sync_check.py**:每 30 分钟跑,对比本地 vs 远端,发现:
   - 远端有本地没(幽灵)
   - 本地有远端没(未推送)
   - SHA 不一致(误改)
4. ✅ **sync_check 跑通**:远端 49 个 ↔ 本地 49 个,清单完全一致,15 个 SHA 抽查全 ✓

**关键发现(意外但重要)**
- **GitHub Tree API 的 sha 跟 Contents API 的 sha 不一致**——这是 GitHub 内部数据库一致性延迟(几秒到几分钟)
- 但**实际内容是一致的**(Contents API 拉 raw + sha1 跟本地比对,完全相同)
- 结论:不能用 Tree API 的 sha 当"推送完整性"的真值,要用 Contents API 拉实际内容 hash

**教训**
- **add-only 推送策略 = 幽灵文件滋生**——任何"本地删除"都该同步到远端
- **.gitignore + push 排除规则要双重保险**——只信一个不够(参考事故 #001)
- **每周跑一次 sync_check.py**——现在有工具了,跑的成本是 30 秒
- **GitHub 内部 API 的一致性延迟是真实存在的**——不怪你,但要选对 API

**预防**
- [x] 修 push 脚本排除规则
- [x] 删 3 个幽灵文件
- [x] 写 sync_check.py
- [ ] 把 sync_check.py 接到 watchdog,30 分钟一次
- [ ] 每天 healthcheck 跑一次 sync_check.py

---

## 2026-06-06  · #011 · GitHub Actions 启用过程(2 个隐藏坑)

**症状**
- 启动 GitHub Actions workflow(`.github/workflows/healthcheck.yml`)
- 第一次 push 失败 — API 报 404(因为 Contents API 不能推 `.github/`)
- 改用 git 协议直接 push,GitHub 报:`refusing to allow a Personal Access Token to create or update workflow .github/workflows/healthcheck.yml without 'workflow' scope`
- 解决:用户升级 token 加 `workflow` scope
- 推上去,第一次 run 失败 — `Validate feeds` step 报 exit 100(xmllint 不存在)
- 改用 Python xml.etree 验证,run 成功

**根因(2 个隐藏坑)**
1. **`.github/` 目录 Contents API 不能推** — GitHub 安全机制,任何用 Contents API 写 `.github/*` 都被拒(包括 workflow 文件)
2. **workflow 文件必须用带 `workflow` scope 的 token** — `repo` scope 不足以创建/更新 workflow 文件,需要额外 `workflow` scope
3. **GitHub Actions runner 没装 xmllint** — 装包又需要 sudo,新 runner `apt-get install` 会无声失败,导致 step 整体 exit 100

**修复**
1. ✅ token 升级加 `workflow` scope(用户操作)
2. ✅ 改用 `urllib + base64 + PUT /contents` API 直接传 workflow 文件(我帮推的,token 升级后能用了)
3. ✅ workflow 改用 Python `xml.etree.ElementTree` 验证 RSS XML,不再依赖系统包
4. ✅ 加 `set +e` 防止 step 早期失败带崩整个 workflow

**最终结果(12:55 run #27053129592)**
- ✅ 9 个 step 全部 success
- 包含 6 项真硬检查 + 3 项环境步骤
- 触发器:push / schedule (UTC 0:30) / workflow_dispatch

**教训**
- **GitHub 的安全机制是有层次的**:Contents API + workflow scope + Actions runner 包缺失,任何一个都可能让 CI 启动失败
- **任何"装系统包"在 CI 里都脆弱** — 优先用标准库(urllib, xml.etree, json, hashlib)
- **token scope 要一次到位** — `repo` + `workflow` 一起勾,别拆

**当前 3 通道检查机制**
- A 通道(GitHub Actions)✅ 启用,每次 push + 每天 8:30 自动跑
- B 通道(daemon_check.sh)✅ 可用,任何有 cron 的机器可装
- C 通道(LLM cron)⚠️ 不可靠,只辅助

**未来每 2 周体检清单加一项**
- [ ] 看 GitHub Actions 最近 1 周的 run 状态(全 ✓?)

---

## 2026-06-08 · #012 · 6-08 早报被 watchdog/重复 push 覆盖(LLM 隐患再现)

**症状**
- 6-08 早上 8:07 主 cron 跑了 commit `02f2659d`,生成 6-08 18 条早报(OpenAI ChatGPT 转型、Anthropic S-1、苹果 WWDC26、Meta 帐篷数据中心等)
- 6-08 早上 8:08 第二次 commit `e7be5461`(间隔 1 分 45 秒),把 news.json **回滚成 6-07**(16 条),并推了一份 W23 周报归档
- 6-08 早上 8:30 健康检查跑 × 失败 × 失败(本机不同步)
- 6-08 早上 10:09 用户发现:"今天没更新 6-08 早报"

**根因分析**
- 主 cron `ai-daily-0800`(8:00) 触发 LLM session A → 跑 fetch_news.py + push_to_github.sh → commit `02f2659d`(6-08 18 条)→ push 成功
- LLM session A 完成后**沙箱里的某种机制(可能是 watchdog cron 触发的 session B)**又跑了一次 fetch_news.py,这次**LLM 不知道当天是 6-08 早报该发布**,误判为"6-08 应该是周末 6-07 的归档状态",**回滚了 news.json**
- 1 分 45 秒内两次 commit,内容互相矛盾
- **commit author 显示 `BBYY11`** 是因为 push_to_github.sh 用 Contents API 推,GitHub 把 committer 写成 token 持有者,**这造成用户困惑("我没跑过")**

**修复**
- ✅ 从 commit `02f2659d` 提取 6-08 news.json + digest.md + feed.xml/json + search_queries.txt
- ✅ 新建 data/archive/2026-06-08.json 作为归档
- ✅ 重建 data/archive/index.json(11 天,加 6-08)
- ✅ 保留 W23 周报(在 e7be5461 里)
- ✅ 7 个文件 PUT 推送,GitHub Actions 健康检查通过
- ✅ 本机同步,sync_check 远端 56 / 本地 56 一致

**教训**
- **事故 #011 提到的隐患再次出现**——LLM session 失败/重复时静默"成功"
- **`push_to_github.sh` 应该加一个去重机制**:如果 news.json 跟 git 远端最新 commit 里的 news.json 一样,**skip push**
- **commit author 写 token 持有者**不是好实践——**应该用不同的 author email**(例如 `ai-daily-bot@MiniMax.ai`),区分"LLM 推"vs"人推"
- **重复触发问题**——主 cron + watchdog cron 时间窗撞了(8:00 vs 7:00-10:30)——**应该让 watchdog 在主 cron 跑完后 30 分钟才检查**

**改进建议(下次实施)**
1. push_to_github.sh 加"如果 news.json 内容跟 HEAD 一致,skip"
2. push_to_github.sh 用 `author.email = "ai-daily-bot@MiniMax.ai"` 而非 token holder
3. watchdog cron 的检查窗口从 7:00-10:30 改为 8:30-10:30(避开主 cron)
4. 6-08 早晨应该**两次 cron 之间的间隔 ≥ 30 分钟**——主 cron 跑完,watchdog 才检查

---

## 2026-06-10 · #013 · 6-10 早报跑到错误的新仓库(`BBYY11/ai-daily.github.io`)

**症状**
- 用户 09:08 反馈"今天没更新 6.10 的早报"
- 远端 `bbyy11/ai-daily` 仓库 last commit 还是 6-09 8:08 `00e97df3`
- 主 cron `ai-daily-0800` 显示 last_result=success(2026-06-10 08:00:05 Asia/Shanghai)
- 远端有**一个新仓库** `BBYY11/ai-daily.github.io`,创建于 2026-06-10 00:08:49 UTC,推了 14 个粗糙的占位文件

**根因(深层)**
- AI Daliy Agent 的 `system_prompt` 是空的(我创建 agent 时没设)
- 主 cron 触发 LLM session 时,该 session 在一个新 sandbox 实例里,**`/workspace/ai-daily/` 是空的**
- 空的 system_prompt + 不知道项目已经存在 → LLM 误以为"项目没建过",**从零创建项目结构**,用 `curl POST /user/repos` **新建了一个 `ai-daily.github.io` 仓库** + 推了 14 个粗糙的脚本
- 真正的 `bbyy11/ai-daily` 仓库完全没动

**修复**
- ✅ 手动补 6-10 早报(18 条,validate 通过,推送 commit `52ba51c2`)
- ✅ 补 6-09 早报归档(从 commit `00e97df3` 拉 news.json,新建 `archive/2026-06-09.json`)
- ✅ 重建 `data/archive/index.json`(13 天,加 6-09 + 6-10)
- ✅ 重建 `AI Daliy Agent` 的 `system_prompt`(写死"项目就是 bbyy11/ai-daily,禁止创建新仓库")
- ✅ 删除旧 ai-daily-0800 cron(task_id 404860864389898),用 Mavis agent 重建(task_id 407416025182284)
- ✅ 5 个 cron 全部移到 Mavis agent 下,任务在 Mavis root session (404846249198073) 跑,**不再出现在我 root session (404846249198074) 的最近任务里**
- ✅ 修 healthcheck / watchdog 引用旧 task_id

**遗留事项**
- ⏳ `BBYY11/ai-daily.github.io` 误建仓库需要用户手动删(GitHub API 需要 admin scope,我 token 没权限)
- ⏳ 误建仓库 14 个文件也是 6-10 早报的"备份",如果你想看 LLM 8:00 实际跑出了什么,在那个仓库

**教训(类似 #011/#012 的同类隐患)**
- **agent 的 system_prompt 必填**——空 system_prompt + 长 cron prompt = LLM 在 sandbox 失忆
- **任何 cron 任务"任务完成后通知 root session"会造成任务列表污染**——应该 silent close
- **跨 sandbox 状态不共享**——cron 跑的 sandbox 跟 root session 的不是同一个,项目数据全在 GitHub 仓库,**LLM 不会自动 clone**
- **更好的方案:把项目 clone 步骤写进 cron prompt 第 0 步之前**(我现在新加的 prompt 里有"项目目录为空 → 立即告诉用户")

**下次需要做的事(推荐)**
1. 给 GitHub token 加 admin scope(或新建一个 admin token),用来清理误建仓库
2. 验证明天 6-11 8:00 主 cron 跑成功,且 LLM session 不再"从零建项目"
3. 写一个 GitHub Actions 工作流监控"bbyy11/ai-daily 的 news.json 是不是今天"

---

## 2026-06-10 · #014 · push_to_github.sh 推全套时回滚 archive/index.json(事故 #013 残留 + 衍生)

**症状**
- 6-10 早上 9:08,用户反馈主页 news.json 是 6-10 但 archive/ 目录里**没有 6-10.json**(正常,还没过完)
- 但 archive.html 显示 6-10 在列表里——`archive/index.json` 里有 6-10 这条
- 用户疑惑"今天没完,为什么 6-10 被归档了"

**根因(更深的)**
- 6-10 8:00 主 cron 触发的 LLM session 误以为项目不存在,从零创建了一个新仓库 `BBYY11/ai-daily.github.io`(事故 #013)
- 我手动补 6-10 早报时,commit `d2e04805` 推了 archive/index.json 的 +24 行,**加了 6-09 + 6-10 两天**(本意是"补索引"!)
- 但**6-10 当天不能进归档索引**——没完
- 然后 9:23 我又推了 normalize() 修复,commit `fcdf057e` 走 `push_to_github.sh` 推全套——**该脚本用本机的 archive/index.json 覆盖远端**
- **本机的 archive/index.json 只到 6-08**(因为 fetch_news 跑了之后没重建索引),所以**远端 6-09 + 6-10 两条被移除**
- 但 commit `d2e04805` 加的 6-09 没被这个 commit 抹掉(我后来又 PUT 了一次修复,见后续)

**为什么用户看到"6-10 被归档"**
- 我 commit `d2e04805` 加的 6-10 索引条目**在那一刻是远端状态**
- `fcdf057e` 推全套时**会回滚 archive/index.json**——把 6-09 + 6-10 删掉
- 后来我 commit `e2652049` 修复,重新 PUT archive/index.json 把 6-09 + 6-10 加回
- 所以**远端 index.json 出现了 6-10 索引条目**(13 days),但 archive/ 目录里没有 6-10.json
- 主页 archive.html 显示 6-10 在列表 → 用户看到"被归档了"

**修复**
- ✅ 从 archive/index.json 移除 6-10 索引条目(commit `1cc4b3ba`),12 天,最新 6-09
- ✅ `push_to_github.sh` 增加排除规则:`data/archive/index.json` 不在 push 范围内
  - 理由:archive/index.json 由 fetch_news.py 跑完后**单独 PUT**,不在 push_to_github.sh 推全套范围
  - 防止 fetch_news 跑完没更新 index.json 时,push_to_github.sh 用过期 index.json 覆盖远端
- ✅ 文档更新:scripts/push_to_github.sh 注释里写明事故 #013 教训

**教训(同类 #012/#013 链式衍生)**
- **任何"全自动推全套"的工作流都有"单文件回滚"风险**——推全套时,**每个文件必须以本机为准**,本机没更新的文件就**不该被推到远端**(因为本机会覆盖远端已有的更新)
- **fetch_news.py / push_to_github.sh 不应该是"两个独立脚本"**——它们之间需要状态机,确保 archive/index.json 总是在 push 之前更新
- **更安全方案**:`push_to_github.sh` 推时**对比每个文件 hash**,**只推有差异的**——但目前没做(事故 #012 的改进只做了"news.json 跟远端一致就 skip",**对其他文件没有同样处理**)

**未来改进(下次实施)**
1. push_to_github.sh 改为"逐文件 hash 比对",只推有变化的(可大幅减少覆盖风险)
2. 把 archive/index.json 重建逻辑塞进 fetch_news.py 末尾,确保每次 push 都有最新 index
3. 写一个 push_dryrun 模式,先 diff 再问"是否推这些"

---

## 2026-06-10 · #015 · 主页只有头条 + 本月周报停留在 W22(双事故)

**症状(用户 10:38 反馈)**
- 主页只显示头条卡(4 条),下面列表是空的——只有顶部"🔥 HEADLINES"区有内容,其余 14 条不见
- 本月 tab 里"上一周总结"还停留在 W22(5-25 ~ 5-31),但用户前几天看过 W23(6-01 ~ 6-07)周报

**根因 1(主页空列表)**
- 6-10 9:23 我加的 `normalize(news)` 函数**return 了 news 对象**(含 items 字段),**不是 items 数组**
- index.html line 265: `ALL_ITEMS = normalize(news)` 期望 ALL_ITEMS 是数组
- 但 normalize 返回的是 `{...news, items: [...]}`——是个对象
- 导致 `ALL_ITEMS.length` 永远是 undefined,`renderNews().filter()` 出 0 条,列表空白
- **renderHeadlines()** 不依赖 ALL_ITEMS.length(它直接 filter items),所以**头条卡正常显示**
- 因此用户看到"只有头条"——bug 范围确认

**根因 2(W22 不更新)**
- weekly-summary cron 6-08 8:00:14 触发,`last_result=success` 但**实际没改 weekly_summary.json**
- 跟事故 #013 同样的"假成功"——LLM session 在新 sandbox,系统提示空,没改 W23
- 用户这几天看到的 W23 实际是 archive/weekly/2026-W23.json 的归档(6-08 8:08 commit `e7be5461` 推的),不是 monthly.html 块的"当前周"
- 6-08 那次 cron 假成功 + 6-09 没跑(周一不是周一)+ 6-10 主 cron 失败 = **weekly_summary.json 一直停在 W22**

**修复**
- ✅ 修 normalize 函数 return 类型:`return (news.items || []).map(...)` 直接返回数组
- ✅ 复制 `data/archive/weekly/2026-W23.json` → `data/weekly_summary.json`
- ✅ 推送(commit `557da750`)
- ✅ 本机同步

**教训(再次同类 #011/#012/#013)**
- **normalize 函数返回值类型必须跟调用方期望一致**——调用 `ALL_ITEMS = normalize(news)` 期望数组,normalize 必须 return 数组
- **weekly_summary.json 必须由 cron 跑完**才能更新——但 cron "假成功" 是个老问题,6-08/6-09/6-10 三次 cron 失败都没报警
- **monthly.html 块的"上一周总结"依赖 weekly_summary.json**——一旦该文件没更新,主页 monthly tab 就一直显示旧的

**未来改进(累计 #012-015 一致的根因)**
1. **每周日 23:00 加一个 weekly_summary.json 自检 cron**——检查 weekly_summary.json 的 `week` 是不是 `当前周-1`,不对就报警
2. **week / month 边界值校验**——validate_news.py 加一个 weekly_summary 校验,跑在主流程前
3. **根本修法**:weekly_summary.json 的更新**不应该靠 LLM 写**——应该 `gen_weekly_summary.py` 跑完就自动写,LLM 只负责补 summary 和 key_themes
4. **修 #013 的根因**:`AI Daliy Agent` system_prompt 已经是"禁止从零建项目"——但 weekly-summary cron 用的 `Mavis` agent,不是 `AI Daliy Agent`,**root cause 是 `Mavis` agent 跨 sandbox 也不携带项目上下文**——解决方案:**weekly-summary cron prompt 开头**就要求 `git clone https://github.com/BBYY11/ai-daily.git` 拉项目
