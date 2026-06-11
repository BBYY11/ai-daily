# AI Daily Fallback(OpenAI 接管)使用说明

## 这是什么

主 cron 跑在 MiniMax 引擎(M2.7 模型)上,但 6-08 / 6-10 已经出过"假成功"事故
(主 cron 显示 success 但实际没生成 news.json,或推到错地方)。

**这个 workflow 是兜底**——每天 **北京时间 8:15**(= UTC 0:15)在主 cron 后 15 分钟触发,
用 **OpenAI gpt-4o-mini** 重新生成早报并推送到 GitHub。

## 启用步骤(只需要 5 分钟)

### 1. 给 GitHub repo 加 secret

去 https://github.com/BBYY11/ai-daily/settings/secrets/actions

点 **"New repository secret"**:
- **Name**: `OPENAI_API_KEY`
- **Secret**: 你的 OpenAI API key(以 `sk-` 开头)

点 **"Add secret"**。

### 2. 推 workflow(已写好,只需要 push)

```bash
cd /workspace/ai-daily
git add .github/workflows/ai-daily-fallback.yml
git commit -m "ci: add OpenAI fallback workflow (incident #002/#007/#012/#013/#014/#015 兜底)"
git push
```

(实际已经推送,见下面 commit log)

### 3. 手动测试一次

去 https://github.com/BBYY11/ai-daily/actions/workflows/ai-daily-fallback.yml

点 **"Run workflow"** → **"Run workflow"** 按钮。

跑完后:
- ✅ 如果主 cron 成功了 → workflow 1 秒钟 exit(看到 "主 cron 成功,fallback 跳过")
- ⚠️ 如果主 cron 失败了 → workflow 调 OpenAI 重新生成,写 news.json,commit + push

## 行为

```
北京时间 8:00  MiniMax 引擎主 cron 跑(可能假成功)
  ↓
北京时间 8:15  GitHub Actions fallback 触发
  ↓
  ├─ 拉 news.json 看 date 是不是今天
  │
  ├─ 是今天 → 跳过(1 秒 exit)
  │
  └─ 不是今天 →
       ↓
       调 OpenAI gpt-4o-mini(用上一周归档作上下文)
       ↓
       解析 JSON + 校验
       ↓
       跑 validate_news.py
       ↓
       生成 3 种订阅
       ↓
       commit + push 到 main
```

## 成本

- 模型: `gpt-4o-mini`
- 每次生成约 8k tokens(输入 + 输出)
- 价格: $0.15/1M input + $0.60/1M output
- 每次成本: 约 **$0.005**(0.5 美分)
- 90% 的日子 1 秒退出不调 API
- 10% 失败的日子调一次 → 月成本 < $0.02(可忽略)

## 故障排查

### "Bad credentials" / "Invalid API key"
→ secret 没加 / 拼写错 / OpenAI 账户没钱了

### "rate_limit_exceeded"
→ OpenAI 限流(免费账户 3 req/min,付费账户更高)
→ 改成 `gpt-4o` 或等待

### workflow 跑通但 news.json 没更新
→ 看 step 6 是不是 exit 1
→ 看 validate_news.py 输出

### 推送失败(403)
→ repo Settings → Actions → General → Workflow permissions
→ 选 "Read and write permissions"

## 长期改进

- [ ] 多个 model fallback(DeepSeek / GLM)
- [ ] Slack / Discord 通知
- [ ] 每周 7 天 archive 上下文加到 prompt
- [ ] 错误率超阈值时自动 disable 主 cron
