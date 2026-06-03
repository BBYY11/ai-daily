# AI Daily · 项目状态总报告

> 截至 2026-06-03 15:20 (Asia/Shanghai) · 用户: bbyy11 · 维护者: Mavis (General agent)

## 1. 一句话总结

一个由 AI 自动维护、每天 8 点刷新的全球 AI 早报网页,部署在 GitHub Pages,带周报归档 + 月度趋势分析双层结构。所有自动化通过 4 个 mavis cron 任务驱动。

## 2. 线上访问

| 入口 | URL | 用途 |
|---|---|---|
| **今日** | https://bbyy11.github.io/ai-daily/ | 每天 8:00 自动刷新的当日早报 |
| **本月** | https://bbyy11.github.io/ai-daily/monthly.html | 上周摘要(块 1)+ 1-5 月总结(块 2) |
| **周报归档** | https://bbyy11.github.io/ai-daily/weekly_archive.html | 所有历史周报(W22 起,每周一追加) |
| **单周详情** | https://bbyy11.github.io/ai-daily/weekly_view.html?week=2026-W22 | 单周周报,可下载 3 种格式 |
| **每日归档** | https://bbyy11.github.io/ai-daily/archive.html | 所有历史日期(2026-05-29 起) |
| **单日快照** | https://bbyy11.github.io/ai-daily/archive-view.html?date=2026-06-03 | 单日早报只读视图 |
| **RSS Feed** | https://bbyy11.github.io/ai-daily/feed.xml | RSS 2.0 订阅源(阅读器 + AI Agent 通用) |

## 3. 自动化流水线(4 个 cron 任务)

| 任务 ID | 名称 | 触发 | 功能 |
|---|---|---|---|
| `404860864389898` | ai-daily-0800 | 每天 8:00 | 抓 55 个信源 + 整理 15-20 条新闻 + 写 news.json + 归档昨日 + 生成 RSS + 推 GitHub |
| `405116951241538` | ai-daily-weekly-summary | 每周一 8:00 | 生成上周摘要 + 永久归档周报 + 推 GitHub |
| `405117857231745` | ai-daily-monthly-summary | 每月 28-31 8:00 | 当月最后一天才真正生成 + 追加到 monthly_archive + 推 GitHub |
| `404859549492193` | ai-daily-healthcheck | 每 6 小时 | 验证主页/news.json/归档/刷新节奏是否正常,异常时主动通知 |

**自动化写入路径**:
```
cron 触发
  ↓
[抓信源] web_search × N 次
  ↓
[整理] news.json 覆盖写入
  ↓
[归档] fetch_news.py 检查 news.json.date 是否旧,旧则归档
  ↓
[推送] push_to_github.sh 用 GITHUB_TOKEN_BBYY11_V2 推 GitHub
  ↓
[GitHub Pages] 1-2 分钟自动刷新
```

## 4. 数据流(当前)

```
data/
├── news.json                 ← 主页(每天覆盖)
├── terms.json                ← 词条百科(累积)
├── weekly_summary.json       ← 块 1 数据(每周覆盖)
├── monthly_archive.json      ← 块 2 数据(每月追加 1 条)
├── search_queries.txt        ← 55 条信源查询(脚本生成)
├── archive/
│   ├── index.json            ← 每日归档索引
│   ├── 2026-05-29.json ~ 2026-06-03.json  ← 6 天历史
│   └── weekly/
│       ├── index.json        ← 周报索引
│       └── 2026-W22.json     ← W22 周报(1 周)
└── archive/weekly/...

scripts/
├── fetch_news.py             ← 归档昨日 news.json
├── push_to_github.sh         ← GitHub Contents API 推送
├── gen_weekly_summary.py     ← 生成 weekly_summary.json 骨架
├── gen_monthly_summary.py    ← 追加到 monthly_archive.json
├── archive_weekly.py         ← 永久归档 weekly_summary → archive/weekly/
├── gen_extra.py              ← 旧种子生成(2026-06-01 / 06-03 历史)
├── gen_monthly.py            ← 旧种子生成(1-5 月)
└── daily.sh                  ← 旧入口,不再使用
```

## 5. 关键产品决策(已与用户确认)

| 决策 | 状态 |
|---|---|
| 主页"今日" = news.json 每天覆盖 | ✅ |
| 主页"本月" = 块 1(上周摘要)+ 块 2(1-5 月) | ✅ |
| "周"概念删除,只剩"今日/本月/归档"3 个 tab | ✅ |
| 周报永久归档 + 3 种下载(Markdown/JSON/打印) | ✅ |
| 月报块 1 每周一更新 / 块 2 每月最后一天更新 | ✅ |
| 信源池 35+ 渠道 | ✅ |
| 6 月还没过完,暂不进入月报(等 6/30 cron 加) | ✅ |
| 词条 hover 显示 AI 百科 | ✅ |
| 多源热度(▲9.6k 爆/热/中/新星)透明来源 | ✅ |

## 6. 已知状态 / 待办

### 已完成
- [x] 整个流水线跑通(cron + 推送 + 渲染)
- [x] GitHub Pages 部署成功(https://bbyy11.github.io/ai-daily/)
- [x] 6 天每日归档(2026-05-29 ~ 2026-06-03)
- [x] 1 周周报归档(W22)
- [x] 5 个月度总结(2026-01 ~ 2026-05)
- [x] 词条百科 55 个
- [x] 推送 token 用 secret 加密存储(GITHUB_TOKEN_BBYY11_V2)

### 暂未做
- [ ] 微信推送(用户已说"算了")
- [ ] 主题切换(深色/亮色)
- [ ] RSS 订阅
- [ ] 多语言(英文版)
- [ ] weekly.html 永久删除(已删了但代码片段还在,无所谓)

### 等待时间触发
- [ ] 6/8 周一 8:00:`ai-daily-weekly-summary` 自动归档 W23
- [ ] 6/30 8:00:`ai-daily-monthly-summary` 自动追加 2026-06 月总结
- [ ] 每 6 小时:healthcheck 自动跑

## 7. 变更日志(本次)

| 日期 | 变更 |
|---|---|
| 2026-06-02 | 初始版本:14 条新闻 + tab + 词条 hover + 周月脉络 |
| 2026-06-03 09:00 | 切 GitHub Pages 部署(原 platform 部署服务挂) |
| 2026-06-03 10:00 | 06-01 / 06-03 历史归档补齐 |
| 2026-06-03 11:30 | 架构重整:主页 = 06-03 今日,tab 跳独立 weekly/monthly 页 |
| 2026-06-03 12:00 | 删 weekly.html,monthly 改为块 1+块 2 两段式,1-5 月总结 |
| 2026-06-03 14:30 | 删 monthly 顶部 hero 装饰块,新增周报永久归档 + 3 种下载 |

## 8. 关键文件大小

```
index.html            ~31 KB
monthly.html          ~13 KB
weekly_view.html      ~11 KB
weekly_archive.html   ~7 KB
archive.html          ~6 KB
archive-view.html     ~7 KB
data/weekly_summary.json  ~3 KB
data/monthly_archive.json ~12 KB
data/terms.json       ~21 KB
data/news.json        ~16 KB
```

(用户如果想看完整代码,直接看 /workspace/ai-daily/ 下对应文件)

## 9. 后续怎么继续

如果用户想要:
- **加新信源**:编辑 `scripts/fetch_news.py` 的 `SOURCE_POOL` 字典
- **改主页样式**:编辑 `index.html`
- **改月度趋势分析模板**:编辑 `data/monthly_archive.json` 的对应月字段
- **加新功能**(搜索/标签/收藏/翻译等):跟维护者 Mavis 提
- **完全重建**:删除整个 `/workspace/ai-daily/` 目录 + GitHub repo,从头开始

## 10. 联系维护者

所有自动化跑在 mavis 平台(Mavis agent),由 cron 调度。任何修改、报错、需求都跟 Mavis 对话。
