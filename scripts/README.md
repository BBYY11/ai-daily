# 真实检查机制部署指南

> 系统检查有 3 个通道。**GitHub Actions** 是最稳的,但**需要 token 加 `workflow` scope**——其他两个开箱即用。

---

## 通道 A:GitHub Actions(推荐,但需 token 升级)

### 工作原理
`.github/workflows/healthcheck.yml` 在以下情况自动跑:
- 每次 push 到 main 分支
- 每天 UTC 0:30 (=北京时间 8:30,主 cron 跑完后 30 分钟)
- 手动 workflow_dispatch

跑 6 项检查,任一失败 → GitHub 显示 ✗ → 我下次对话能查 GitHub Actions log

### 怎么启用

**1. 升级 token 加 `workflow` scope**

```
1. 去 https://github.com/settings/tokens
2. 找到 token(或新建,推荐新建)GITHUB_TOKEN_BBYY11_V3
3. 勾上:
   ✓ repo  (已有)
   ✓ workflow  (新增)
4. 生成后复制 token
5. 告诉我(我存到 secret)
6. 我用 V3 推 .github/workflows/healthcheck.yml
```

**2. 我推完后,GitHub Actions 会自动跑**

### 你能看到什么

- GitHub 仓库页面 → Actions 标签
- 看到 "AI Daily Health Check" workflow
- 绿色 ✓ 通过 / 红色 ✗ 失败
- 点进去看每一步日志

---

## 通道 B:服务器 daemon_check(开箱即用,辅助)

### 工作原理
`scripts/daemon_check.sh` 直接调 Python 检查脚本,**不靠 LLM,exit code 0/1 可靠**。

### 在哪跑

- 任何能跑 cron 的机器(你的 Mac/Windows + WSL/Linux、Linux 服务器、NAS 等)
- 我现在的开发 sandbox 是临时的,**不算长期可靠**

### 怎么用

**Mac/Linux**:
```bash
# 1. 把整个 ai-daily 目录复制到你能长跑的机器(或者 git clone)
cd /path/to/ai-daily

# 2. 编辑 crontab
crontab -e

# 3. 加一行(每 30 分钟跑一次)
*/30 * * * * /path/to/ai-daily/scripts/daemon_check.sh

# 4. 看结果
tail -f /tmp/ai-daily-daemon.log
```

**Windows + WSL**:
```bash
# WSL 里的 cron
*/30 * * * * /mnt/c/path/to/ai-daily/scripts/daemon_check.sh
```

### 失败时怎么知道

daemon_check.sh 当前只**写日志到 /tmp/ai-daily-daemon.log**,**不主动通知**。要告警需要:
- Mac:用 `terminal-notifier` / `osascript` 发系统通知
- Linux:用 `mail` 发邮件
- 或在 daemon_check 末尾加 `curl -X POST https://your-webhook/...`

**目前我建议**:每 30 分钟跑,**主动看 log**(或我下次帮你看)。

---

## 通道 C:LLM cron 任务(不可靠,只辅助)

5 个 cron 都是"触发 LLM session 跑任务",**不是真"检查"**:

| Cron | 行为 | 可靠度 |
|---|---|---|
| ai-daily-0800 | 触发 LLM 跑主流程 | ❌ 失败时 LLM 静默退出 |
| ai-daily-watchdog | 触发 LLM 跑 check_health.py | ⚠ LLM 看到 ALERT 也可能不报 |
| ai-daily-healthcheck | 触发 LLM 跑 5 项指标 | ⚠ 同上 |
| ai-daily-weekly-summary | 周一 8:00 跑 | ✅ 单次任务 |
| ai-daily-monthly-summary | 月末 8:00 跑 | ✅ 单次任务 |

**结论**:**不能依赖通道 C 报警**。事故 #002 / #007 / #008 都证明了。

---

## 推荐组合

| 场景 | 推荐 |
|---|---|
| 你的电脑 24h 开机 | 通道 A(主) + 通道 B(辅) |
| 你只有手机/笔记本,24h 不在线 | 通道 A(主) |
| 你想完全托管给 MiniMax | 通道 A + 通道 C(LLM watchdog) |

**最稳组合**:**A + B 一起开**——GitHub 跑远端,你的机器跑本地,双重保险。

---

## 当前状态

- ✅ `scripts/check_health.py` — watchdog 用,7 项硬检查
- ✅ `scripts/validate_news.py` — 主 cron 必跑,15+ 项质量门
- ✅ `scripts/sync_check.py` — 远端一致性检查
- ✅ `scripts/daemon_check.sh` — server-side 真硬检查
- ✅ `.github/workflows/healthcheck.yml` — 写好了,**未推送**(token 缺 workflow scope)
- ⏳ 通道 A 启用条件:**token 加 `workflow` scope**

---

## 启动通道 A 的命令(给 Mavis)

我这边,你升级完 token 给我之后:
1. 我把 `GITHUB_TOKEN_BBYY11_V3` 存到 secret
2. 改 push_to_github.sh 用 V3
3. 推 .github/workflows/healthcheck.yml
4. GitHub Actions 跑第一次,确认能过
5. 之后每次 push 自动跑
