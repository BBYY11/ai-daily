# AI Daily · 运行流程标准

> 目标:让每日早报的产出**可重复、可验证、可恢复**。
> 任何改动,先看这份文件。

---

## 1. 每日 8:00 主流程(ai-daily-0800 cron)

### 1.1 标准步骤(必须严格按序)

```
[0] 归档旧数据
    bash: cd /workspace/ai-daily && python3 scripts/fetch_news.py 2026-06-XX
    说明: 位置参数,不是 --date flag
    行为: 如果 news.json 的 date 跟今天不同 → 归档到 archive/{旧date}.json + 写占位骨架
          重建 archive/index.json(7+ 天的清单)

[1-3] 抓信源 + 整理(LLM 自主)
    web_search × 55+ 信源
    web_fetch 核验 3-5 条
    整理 15-20 条新闻,分布:
      headline≥3 / rising≥4(带 rising_metrics) / company≥3 / paper 2-3 / industry 1-2 / social 1-2

[4] 每条生成 heat {score, level, sources, breakdown}
[5] 提取 8-12 个高频词条,合并写入 terms.json
[6] 重写 news.json(date=今天, weekday, generated_at, summary, stats, items, weekly_arc, monthly_arc)
    ⚠️ ISO 周编号要对(6-04 周四 = 2026-W23,每月 1 号 = 那个月的 W0n)
[7] 生成 3 种订阅源
    python3 scripts/gen_feed.py
    python3 scripts/gen_json_feed.py
    python3 scripts/gen_digest.py
[8] 推送
    bash scripts/push_to_github.sh
[9] 响应用户,告知条数 + 状态
```

### 1.2 失败处理(关键)

| 步骤失败 | 行为 |
|---|---|
| [0] fetch_news.py 失败 | 报用户,等手动处理。**不要继续往下走** |
| [1-3] web_search 全部限流 | 报用户,**不要用空数据写 news.json**(等手动补) |
| [6] 写 news.json 时 context 超长 | 拆成 2 步:先写 5 条 rising,再追加 10 条其余 |
| [8] push 失败 | 自动重试 1 次,还失败则报用户(检查 GITHUB_TOKEN_BBYY11_V2) |
| 任何步骤 | **不静默**。last_result=success 但内容空 = bug |

### 1.3 推送完整性自检(必做,新增!)

每次 push 后,**Mavis 必须跑 5 个文件存在性检查**:

```bash
for f in data/news.json assets/style.css index.html feed.xml feed.json digest.md; do
  curl -s -H "Authorization: token $GITHUB_TOKEN_BBYY11_V2" \
    "https://api.github.com/repos/bbyy11/ai-daily/contents/$f" | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{\"✓\" if \"size\" in d else \"✗\"} {sys.argv[1]} {d.get(\"size\",\"-\")}')" "$f"
done
```

**任意一个 ✗ → 立刻重推**(用 `bash scripts/push_to_github.sh` 第二次,幂等)

### 1.4 字段自检

推送完成后,Mavis 必须确认:
- `news.json` 的 date == 今天
- `items` 数量 >= 14
- `summary` 长度 >= 80 字
- 没有 `PLACEHOLDER` 标记
- `weekly_arc.weeks` 第一项 date == 今天

---

## 2. Watchdog 流程(ai-daily-watchdog cron)

### 2.1 触发时间
每天 7:00 / 7:30 / 8:00 / 8:30 / 9:00 / 9:30 / 10:00(覆盖主 cron 窗口 + 30 分钟延时)

### 2.2 检查项(7 项)

```python
# 1. news.json.date == 今天?
# 2. items 数量 >= 14?
# 3. summary 长度 >= 80?
# 4. 没有 PLACEHOLDER 标记?
# 5. weekly_arc.weeks[0].date == 今天?
# 6. 主 cron (404860864389898) last_result == success?
# 7. assets/style.css 在 GitHub 上(防 .gitignore 反扑)?
```

### 2.3 异常响应

| 异常 | 行动 |
|---|---|
| 7:00 发现 news.json 不是今天 | 报用户,等 8:00 主 cron |
| 8:30 仍不是今天 | **Mavis 立即手动补**(从 web_search 抓今天新闻) |
| 9:00 还不行 | 报用户 + 提供"我自己写一份"的选项 |
| items < 14 | 报用户"可能 LLM 抓信源失败",Mavis 手动补 3-5 条 |

---

## 3. 每周一 8:00 周报流程(ai-daily-weekly-summary cron)

### 3.1 标准步骤
```
[1] python3 scripts/gen_weekly_summary.py   # 生成骨架(day_links 填好)
[2] LLM 读 7 天归档,提炼 summary + key_themes
[3] 写回 weekly_summary.json
[4] python3 scripts/archive_weekly.py        # 永久归档到 archive/weekly/{week}.json
[5] bash scripts/push_to_github.sh          # 推送
```

### 3.2 ISO 周定义
- 周一 → 周日 = 1 个 ISO 周
- 例:2026-05-25(周一)→ 2026-05-31(周日) = 2026-W22
- 每周一的 cron 任务是生成**上周一-上周日**的周报

---

## 4. 每月最后一天 8:00 月报流程(ai-daily-monthly-summary cron)

### 4.1 触发逻辑
- cron 每天 8:00 触发(28-31 号)
- 脚本自己判断:只有**今天是该月最后一天**才生成,否则 exit
- 6 月还没过完,绝对不要进 monthly_archive.json

### 4.2 步骤
```
[1] python3 scripts/gen_monthly_summary.py    # 自动判断 + 生成骨架
[2] LLM 提炼 trend_summary / key_events / data_points / look_ahead
[3] 写回 monthly_archive.json(只追加,不改已有月份)
[4] bash scripts/push_to_github.sh
```

---

## 5. 健康检查(ai-daily-healthcheck cron,每 6 小时)

跑 5 个核心指标:
1. 主页可访问性
2. data/news.json 的 date
3. 主 cron 状态
4. 周月归档完整性
5. monthly.html 块 1/块 2 渲染

---

## 6. 推送通道(目前)

| 类型 | 通道 | 状态 |
|---|---|---|
| GitHub Pages | https://bbyy11.github.io/ai-daily/ | ✅ 主通道 |
| RSS / JSON / Markdown | /feed.xml /feed.json /digest.md | ✅ |
| 微信推送 | MiniMax bot 不能主动推 | ❌ |
| 邮件推送 | **待用户授权邮箱** | ⏳ |
| 浏览器快捷指令 | 用户可自己设 | ⏳ |

---

## 7. 命名规范

- **文件**:小写 + 下划线(`news.json`, `monthly_archive.json`, `weekly_summary.json`)
- **HTML 页面**:kebab-case(`archive-view.html`, `weekly_view.html`)
- **ISO 周**:`YYYY-Www`(例:`2026-W23`)
- **日期**:`YYYY-MM-DD`(例:`2026-06-05`)
- **类目**:`headline / rising / company / paper / industry / social`(6 类固定)

---

## 8. 真实检查机制(双通道)

### 8.1 通道 A:GitHub Actions(主要)

`.github/workflows/healthcheck.yml` 在以下情况触发:
- 每次 push 到 main
- 每天 UTC 0:30(=北京时间 8:30,主 cron 后 30 分钟)
- 手动 workflow_dispatch

跑 6 项检查:
1. 关键文件存在性
2. news.json schema 验证
3. index.html 引用 style.css
4. RSS/JSON Feed 合法
5. news.json 跟 archive 交叉一致
6. 文件总数合理性

**任一失败 → commit 状态显示 ✗ → 我会在下一个对话轮手动查 GitHub Actions log**

### 8.2 通道 B:服务器 cron(辅助)

如果用户在能跑 cron 的环境(自己的服务器、本地)装了 `scripts/daemon_check.sh`,加到 crontab:
```
*/30 * * * * /path/to/ai-daily/scripts/daemon_check.sh
```
脚本会跑 check_health + validate + sync_check,失败 exit 1。

### 8.3 通道 C:LLM session(补充,不可靠)

- ai-daily-watchdog(每 30 分钟 7-10:30)
- ai-daily-healthcheck(每 6 小时)
- ai-daily-0800(每天 8:00)

这些 LLM session **会失败而假装成功**(#002/#007/#008 教训),**不能依赖**。
只能作为辅助通知手段,真告警靠 A + B。

### 8.4 优先级

发现异常时,排查顺序:
1. 看 GitHub Actions 最近一次 run(通道 A)
2. 看 server daemon_check.log(通道 B,如果装了)
3. 看 cron last_error(通道 C)
4. **不要只看 cron last_result=success**——可能误报

---

## 8. 变更记录

| 日期 | 变更 | 原因 |
|---|---|---|
| 2026-06-05 | 新增推送完整性自检 | style.css 漏推事件 |
| 2026-06-05 | fetch_news.py 加占位骨架 | 防止 LLM 失败时主页空白 |
| 2026-06-05 | 新增 watchdog cron | 7 段时间点监控 |
| 2026-06-04 | 修复 --date flag 笔误 | 6-04 早报漏发 |
