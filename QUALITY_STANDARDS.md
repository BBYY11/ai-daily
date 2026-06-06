# AI Daily · 质量标准

> 任何输出都必须达到以下标准。低于标准的,不发,重做。

---

## 1. 内容质量(新闻)

### 1.1 数量与分布

- **总条数**:15-20 条
- **分类硬指标**:
  - 头条(headline):**至少 3 条**
  - 新兴(rising):**至少 4 条**(必须带 rising_metrics)
  - 公司(company):至少 3 条
  - 论文(paper):2-3 条
  - 行业(industry):1-2 条
  - 声音(social):1-2 条
- **新兴类专属**:必须有 GitHub stars / HN points / X mentions 等**真实数据**

### 1.2 真实度

- ❌ 不得编造数据(估值、用户数、融资金额)
- ❌ 不得用"据悉"、"有消息"等模糊措辞填充
- ✅ 数字必须有出处("据 Sensor Tower"、"据路透社"、"彭博报道")
- ❌ 不得把 6-03 的新闻当 6-04 重复
- ❌ 不得用上周内容(7 天前的)充数

### 1.3 文本质量

- **标题**:**中文**、12-30 字、关键名词不缩略
- **summary**:80-200 字、说清楚"什么公司做了什么 + 数据点 + 意义"
- **source**:必须用 `/` 分隔的多源(例:`路透社 / 36氪 / 第一财经`)
- **time**:YYYY-MM-DD 格式
- **tags**:3-5 个,中文,小写
- **terms**:2-4 个,匹配 terms.json 中的词

### 1.4 热度(heat)

- **score**:**多源加权估算**,不是单一来源
- **level**:**爆 / 热 / 中 / 新星** 4 档,根据 score 范围:
  - 爆:>= 7500
  - 热:5000-7500
  - 中:3000-5000
  - 新星:1500-3000
- **sources**:从 [hn, x, github, reddit, ph, media, paper] 中选,至少 2 个
- **breakdown**:用 · 分隔的中文明细,例:"Build 大会主 keynote · ~2.4k HN points · ~10k X mentions"

### 1.5 词条百科(terms.json)

- 55+ 个,每月新增 5-10 个高频技术名词
- 字段:`{name, category, summary, detail, links}`
- **summary**:1 句话讲清是什么
- **detail**:2-3 句讲清技术意义或商业价值
- **links**:1-3 个外链(官方 / 论文 / 报道)

### 1.6 JSON 硬规则(事故 #008 教训)

- 【**任何 JSON 字符串内禁止内嵌 ASCII 双引号 `"`**】
  - 错:`"summary": "今天 AI 圈\"很火\""` ← 看着对,实际 JSON 合法,但 hand-writing 易写错
  - 对:`"summary": "今天 AI 圈‘很火’"`(单引号)或 `"summary": "今天 AI 圈“很火”"`(中文引号)
  - 验证:写完 news.json 立刻 `python3 -c "import json; json.load(open('data/news.json'))"` 不报错
- **所有手动写 JSON 之前先跑 validate_news.py** — 它有 try/except 兜底
- **占位骨架**必须以 `🚧 PLACEHOLDER` 开头,不能只有日期描述(避免被误认为真早报)

---

## 2. 视觉/交互质量(HTML)

### 2.1 设计 token(必须保持一致)

- 背景米白 `#fafaf7` / 卡片纯白 `#ffffff`
- 主色钴蓝 `#1e40af`(蓝色主)
- 强调橙 `#ea580c`(热度、活跃)
- 字号 800 weight,字间距 -0.025em
- 顶部 3 像素彩条(蓝→橙→紫)
- 卡片:1px 浅灰边 + 3px 蓝色左边条(hover 弹出) + 浅阴影
- **新页面/新组件必须用 assets/style.css 里现成的 token,不要写新颜色**

### 2.2 响应式(3 档)

| 尺寸 | 行为 |
|---|---|
| 桌面 >= 900px | 完整布局(1240px max-width) |
| 平板 600-900px | 简化版(2 列) |
| 手机 <= 600px | 紧凑版(单列 + 汉堡菜单 + 44px 按钮) |

### 2.3 性能

- 主页 < 200KB(HTML+CSS+JS 合计)
- LCP < 2 秒(本地)
- 字体用系统字体栈(不引 webfont)
- JS 单文件 < 25KB(无外部库)

---

## 3. 数据完整性

### 3.1 必做 5 项检查(每次推送前)

- [ ] `data/news.json` 的 date == 今天
- [ ] `data/news.json` items >= 14 条
- [ ] `data/news.json` summary >= 80 字
- [ ] `data/news.json` 无 PLACEHOLDER 标记
- [ ] `data/weekly_arc.weeks[0].date` == 今天

### 3.2 推送后必做 5 项验证(用 GitHub Contents API)

- [ ] `data/news.json` 在 GitHub 上(>= 10KB)
- [ ] `assets/style.css` 在 GitHub 上(>= 25KB,**这条是历史教训**)
- [ ] `index.html` 在 GitHub 上(>= 20KB)
- [ ] `feed.xml` 在 GitHub 上(>= 10KB)
- [ ] `feed.json` 在 GitHub 上(>= 10KB)

---

## 4. 可用性(用户体验)

### 4.1 手机端(权重最高,因为用户主要从微信进)

- 首屏 1 秒内能看到当天日期
- 头条 3 条不需滚动
- 列表 4 列折叠成 3 列(meta 单元隐藏)
- 按钮 44px 触摸友好
- 无横向滚动

### 4.2 阅读体验

- 段落左对齐(绝不居中,本项目硬要求)
- 行高 1.65-1.75(中文阅读舒适)
- 字号 14-16px(正文),18-22px(标题)
- 关键词 hover 弹出百科(桌面),不弹出(手机,避免误触)

### 4.3 可达性

- 所有图片有 alt
- 颜色对比度 >= WCAG AA(正文 4.5:1,大字 3:1)
- 键盘可导航(用真 button/a 不用 div)
- `<link rel="alternate">` 自动发现 RSS

---

## 5. 时间一致性

- **所有时间用 Asia/Shanghai**(本产品目标用户)
- **新闻 time 字段**:`YYYY-MM-DD`
- **ISO 周**:`YYYY-Www`
- **月份**:`YYYY-MM`
- **不得**用 ISO 8601 完整格式显示给用户(只内部存)

---

## 6. 不做的事

| 不做 | 原因 |
|---|---|
| 推送未验证的变更 | 历史教训:.gitignore 把 style.css 漏推 |
| 修改 HTML/JS/CSS 不更新文档 | 下次改动找不到上下文 |
| 改 cron prompt 不测一遍 | 今天 6-04 漏发的根因 |
| 静默吞错 | "last_result=success" 实际没数据 |
| 改风格(色/字/间距)不写 changelog | 视觉变更是不可逆的 |

---

## 7. 风格红线

- 不得去掉彩条(品牌识别)
- 不得改回黑底(已确认伤眼)
- 不得删除 weekly_archive / monthly 的"查看所有历史"链接
- 不得取消手机端汉堡菜单
- 不得在 HTML 里写内联颜色(必须用 style.css 变量)
