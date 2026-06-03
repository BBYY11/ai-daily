# AI Daily · 全球 AI 早报

> 每天 08:00 (Asia/Shanghai) 自动生成、永久归档的全球 AI 资讯网页。
> 部署在 GitHub Pages,完全自动运行,无需人工维护。

## 在线访问

👉 **https://bbyy11.github.io/ai-daily/**

| 入口 | 用途 |
|---|---|
| [今日](https://bbyy11.github.io/ai-daily/) | 每天 8:00 自动刷新的当日早报(15-20 条新闻) |
| [本月](https://bbyy11.github.io/ai-daily/monthly.html) | 上周摘要 + 1-5 月总结(块 1 每周一更新,块 2 每月最后一天更新) |
| [周报归档](https://bbyy11.github.io/ai-daily/weekly_archive.html) | 所有历史周报(W22 起,每周一追加) |
| [单周详情](https://bbyy11.github.io/ai-daily/weekly_view.html?week=2026-W22) | 单周报内容 + Markdown / JSON / 打印 3 种下载 |
| [每日归档](https://bbyy11.github.io/ai-daily/archive.html) | 所有历史日期(2026-05-29 起) |
| [单日快照](https://bbyy11.github.io/ai-daily/archive-view.html?date=2026-06-03) | 单日早报只读视图 |
| [⚡ RSS Feed](https://bbyy11.github.io/ai-daily/feed.xml) | RSS 2.0 订阅源,给阅读器 + AI Agent 用 |

## 功能

- **多源信源池**:55+ 渠道,覆盖头部(OpenAI / Anthropic / NVIDIA / 阿里 / 字节)+ 新兴(HN / Reddit / GitHub Trending / Product Hunt / X)+ 学术(arXiv / Hugging Face)+ 行业(Polymarket / 财联社)+ 社区声音
- **15-20 条每日新闻**:分头条 / 新兴 / 公司 / 论文 / 行业 / 声音 6 类
- **多源热度估算**:每条新闻的 ▲ 分数是综合估算(HN 点数 + GitHub 涨星 + X 提及 + 媒体覆盖),不是单一排名;hover 可看明细
- **新兴项目高亮**:品红色标识,显示 GitHub 24h 涨星 / HN 点数 / Product Hunt 排名等具体数字
- **55+ 词条悬浮百科**:hover 任何技术名词出"AI 百科"弹层(分类 + 简述 + 详细 + 外部链接)
- **上周摘要**(本月页块 1):每周一 8:00 自动生成,讲清上周 7 天 AI 圈主要事件 + 5 大主题
- **月度趋势总结**(本月页块 2):每月最后一天 8:00 自动追加该月总结(趋势分析 + 关键事件 + 关键数据 + 展望下月)
- **永久归档**:每日 / 每周 / 每月的快照都永久保存,不会丢失
- **周报下载**:每周报可下载 Markdown / JSON / 打印 PDF 3 种格式

## 自动化时间表

| 时间 | 触发 | 动作 |
|---|---|---|
| **每天 8:00** | ai-daily-0800 | 抓 55 信源 → 整理当日 → 写 news.json → 归档昨日 → 推 GitHub |
| **每周一 8:00** | ai-daily-weekly-summary | 算上周 7 天 → 生成 weekly_summary.json → 永久归档到 archive/weekly/ → 推 GitHub |
| **每月最后一天 8:00** | ai-daily-monthly-summary | 读当月所有日 → 追加到 monthly_archive.json → 推 GitHub |
| **每 6 小时** | ai-daily-healthcheck | 验证主页 / 归档 / cron 状态,异常时主动通知 |

## 数据流

```
cron 触发
  ↓
[抓信源] web_search × 55 次
  ↓
[整理] news.json 覆盖写入(今日 15-20 条)
  ↓
[归档] fetch_news.py 检查 news.json.date 旧则归档
  ↓
[推送] push_to_github.sh 用 GITHUB_TOKEN 推 bbyy11/ai-daily
  ↓
[GitHub Pages] 1-2 分钟自动刷新
```

## 文件结构

```
ai-daily/
├── index.html              # 主页(今日早报)
├── monthly.html            # 本月脉络(上周摘要 + 1-5 月总结)
├── weekly_archive.html     # 周报归档列表
├── weekly_view.html        # 单周详情 + 下载按钮
├── archive.html            # 每日归档列表
├── archive-view.html       # 单日早报快照
│
├── data/
│   ├── news.json           # 当日(覆盖)
│   ├── terms.json          # 词条百科
│   ├── weekly_summary.json # 上周摘要(覆盖)
│   ├── monthly_archive.json # 月度总结(追加)
│   ├── search_queries.txt  # 信源查询
│   └── archive/
│       ├── index.json      # 每日索引
│       ├── YYYY-MM-DD.json # 每日快照
│       └── weekly/
│           ├── index.json  # 周报索引
│           └── YYYY-Www.json # 周报永久归档
│
├── scripts/                # 后台脚本
│   ├── fetch_news.py
│   ├── push_to_github.sh
│   ├── gen_weekly_summary.py
│   ├── archive_weekly.py
│   └── gen_monthly_summary.py
│
├── README.md               # 本文件
├── PROJECT_SUMMARY.md      # 项目状态报告
├── PROJECT_FILES.md        # 完整文件清单
└── .gitignore              # 排除本地截图等
```

## 自定义

### 加新信源
编辑 `scripts/fetch_news.py` 的 `SOURCE_POOL` 字典。

### 改主页视觉
编辑 `index.html` 的 CSS(头部 + tab + 卡片样式)。

### 改周报 / 月报样式
分别编辑 `weekly_view.html` / `monthly.html`。

### 加新词条
编辑 `data/terms.json`,加:
```json
"你的术语": {
  "name": "显示名",
  "category": "分类",
  "summary": "一句话",
  "detail": "详细解释",
  "links": [{"label": "参考", "url": "https://..."}]
}
```

## License

MIT
