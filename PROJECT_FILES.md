# AI Daily · 项目文件清单

> 截至 2026-06-03 15:20 (Asia/Shanghai)

## 顶层 HTML 文件(6 个)

| 文件 | 用途 | 路由 |
|---|---|---|
| `index.html` | 主页 — 当日 18 条早报 + tab 切换 | `/` |
| `monthly.html` | 本月脉络 — 上周摘要 + 1-5 月总结 | `/monthly.html` |
| `weekly_archive.html` | 周报归档列表(永久保存) | `/weekly_archive.html` |
| `weekly_view.html?week=2026-W22` | 单周详情 + 3 种下载 | `/weekly_view.html` |
| `archive.html` | 每日归档列表 | `/archive.html` |
| `archive-view.html?date=2026-06-03` | 单日早报快照 | `/archive-view.html` |

## scripts/(7 个 Python 脚本 + 1 个 shell)

| 文件 | 触发 | 功能 |
|---|---|---|
| `fetch_news.py` | cron 第 0 步 | 检查 news.json 的 date,旧则归档到 archive/{旧date}.json |
| `push_to_github.sh` | cron 最后一步 | 用 GitHub Contents API 推送整个项目到 bbyy11/ai-daily |
| `gen_weekly_summary.py` | 每周一 cron | 算"上周一到上周日",读 7 天归档,生成 weekly_summary.json 骨架 |
| `archive_weekly.py` | 每周一 cron(第 4 步) | 复制 weekly_summary.json 到 archive/weekly/{week}.json(永久) |
| `gen_monthly_summary.py` | 每月 28-31 cron | 当月最后一天才真正追加到 monthly_archive.json |
| `gen_extra.py` | 一次性(已用) | 06-01 / 06-03 种子数据生成 |
| `gen_monthly.py` | 一次性(已用) | 1-5 月种子数据生成 |
| `daily.sh` | 已废弃,不再使用 | 早期入口 |

## data/(JSON 数据文件)

| 文件 | 大小 | 用途 |
|---|---|---|
| `data/news.json` | ~16 KB | 主页(每天覆盖)— 06-03 当前 14 条 |
| `data/terms.json` | ~21 KB | 词条百科 55 个 |
| `data/weekly_summary.json` | ~3 KB | W22 上周摘要(每周覆盖) |
| `data/monthly_archive.json` | ~12 KB | 1-5 月总结(每月追加) |
| `data/search_queries.txt` | ~2 KB | 55 条信源查询清单 |
| `data/archive/index.json` | 清单 | 每日归档索引 |
| `data/archive/2026-05-29.json` | 单日 | 5 月 29 日早报(7 条) |
| `data/archive/2026-05-30.json` | 单日 | 5 月 30 日早报(8 条) |
| `data/archive/2026-05-31.json` | 单日 | 5 月 31 日早报(8 条) |
| `data/archive/2026-06-01.json` | 单日 | 6 月 1 日早报(14 条) |
| `data/archive/2026-06-02.json` | 单日 | 6 月 2 日早报(18 条) |
| `data/archive/2026-06-03.json` | 单日 | 6 月 3 日早报(14 条) |
| `data/archive/weekly/index.json` | 清单 | 周报索引(当前 1 周) |
| `data/archive/weekly/2026-W22.json` | 单周 | W22 周报(5/25-5/31) |

## 文档 + 配置(4 个)

| 文件 | 用途 |
|---|---|
| `README.md` | GitHub Pages 用户使用说明 |
| `PROJECT_SUMMARY.md` | 内部项目状态总报告(本文档的伴生) |
| `PROJECT_FILES.md` | 本文件 — 完整文件清单 |
| `.gitignore` | 排除 assets/ 截图、snap.js、临时文件 |

## assets/(本地截图,不入 GitHub)

由 .gitignore 排除,不会部署到 GitHub Pages。包含:
- preview-top.png / preview-full.png — 主页截图
- preview-glossary.png / preview-heat.png — 交互效果截图
- preview-archive.png / preview-snapshot.png / preview-rising.png / preview-tab-rising.png / preview-weekly-archive.png / preview-weekly-view.png / preview-monthly.png — 各页面截图

## snap.js(本地工具,不入 GitHub)

Puppeteer 截图脚本,本地调试用。

## 当前未使用 / 已废弃

- `weekly.html` — 已删除(用户决定不要周 tab,改成 monthly.html 内块 1)
- `daily.sh` — 早期入口,已被 fetch_news.py + push_to_github.sh 取代
- `data/news.json` 顶层的 `weekly_arc` / `monthly_arc` 字段 — 现在由 monthly.html / weekly_summary.json 取代,主页不再用(但保留以防老代码依赖)

## Cron 任务(4 个,均在 mavis 平台)

| task_id | 名称 | 触发 |
|---|---|---|
| 404860864389898 | ai-daily-0800 | 每天 8:00 |
| 405116951241538 | ai-daily-weekly-summary | 每周一 8:00 |
| 405117857231745 | ai-daily-monthly-summary | 每月 28-31 8:00 |
| 404859549492193 | ai-daily-healthcheck | 每 6 小时 |

## Secrets(平台加密)

| 名称 | 用途 |
|---|---|
| GITHUB_TOKEN_BBYY11_V2 | 推送到 bbyy11/ai-daily 仓库的 PAT(只勾 `repo` 权限) |

## GitHub 仓库

- **仓库名**: bbyy11 / ai-daily
- **公网 URL**: https://bbyy11.github.io/ai-daily/
- **Pages 设置**: Source = Deploy from a branch / Branch = main / Folder = / (root)
