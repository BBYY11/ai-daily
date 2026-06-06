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

