# AI Daily · 全球 AI 早报

> 每天 08:00 (Asia/Shanghai) 自动生成的全球 AI 资讯网页。
> 信源覆盖 35+ 头部英文 / 中文 / 学术 / 行业 / 社交渠道,带技术词条悬浮百科,周月发展脉络视图。

## 公网链接(GitHub Pages 版)

启用 GitHub Pages 后,你的早报链接形如:
```
https://<你的用户名>.github.io/<仓库名>/
```
例如 `https://mavis.github.io/ai-daily/`

---

## 🛠️ 部署到 GitHub Pages(5 分钟)

### 第 1 步:创建 GitHub 仓库

1. 打开 https://github.com/new
2. Repository name 填 `ai-daily`(或任意名字)
3. **Public**(必须 Public,Pages 才免费)
4. **Add a README file** 不勾选
5. 点 Create repository

### 第 2 步:上传代码(三种方式任选)

**方式 A:网页直接拖(最简单,推荐)**
1. 仓库页点 `uploading an existing file` 链接
2. 把 `ai-daily-github.zip` 解压后的**所有文件和文件夹**直接拖进去
3. 点 Commit changes

**方式 B:Git 命令行(如果你装了 git)**
```bash
unzip ai-daily-github.zip
cd ai-daily
git init
git add .
git commit -m "init: ai-daily"
git branch -M main
git remote add origin https://github.com/<你的用户名>/ai-daily.git
git push -u origin main
```

**方式 C:GitHub Desktop**
- 打开 GitHub Desktop → File → Add local repository → 选解压后的 `ai-daily` 文件夹 → Publish

### 第 3 步:启用 Pages

1. 仓库页 → Settings → Pages(左侧菜单)
2. Source 选 `Deploy from a branch`
3. Branch 选 `main` / folder 选 `/ (root)`
4. 点 Save
5. 等 1-3 分钟,刷新页面,会显示一行:
   > Your site is live at `https://<你的用户名>.github.io/ai-daily/`

### 第 4 步:打开看看

访问那个链接,应该能看到完整的早报。`/archive.html` 是归档页。

---

## 📁 文件结构

```
ai-daily/
├── index.html              # 主页(单文件,无构建步骤)
├── archive.html            # 归档列表
├── archive-view.html       # 单日快照视图
├── data/
│   ├── news.json           # 今日新闻
│   ├── terms.json          # 词条百科
│   ├── search_queries.txt  # 信源查询清单
│   └── archive/
│       ├── index.json      # 归档索引
│       └── YYYY-MM-DD.json # 每日快照
├── scripts/                # 本地运行的脚本(不部署,放 GitHub 只是存档)
│   ├── fetch_news.py
│   ├── push.py
│   └── daily.sh
└── README.md
```

---

## 🤖 自动化(可选)

`scripts/` 是给 cron 任务用的本地脚本,**GitHub Pages 部署不需要它**。

如果要让早报**每天自动更新**到 GitHub Pages,需要:
1. 一个能跑 cron 的机器(云函数/服务器/我所在的 Mavis)
2. 每天跑 fetch_news.py → 重写 data/news.json → git push 到你的仓库
3. GitHub Pages 几分钟后自动刷新

现在最小化可用:把 news.json / terms.json 改一下,git push 一次,几分钟后公网更新。

---

## 📦 信源池

英文头部官方:OpenAI / Anthropic / Google DeepMind / NVIDIA / Meta / Mistral / xAI
英文头部媒体:TechCrunch / The Verge / Wired / MIT Tech Review / VentureBeat / IEEE Spectrum / The Decoder
中文头部:机器之心 / 量子位 / 新智元 / 智东西 / PaperWeekly / 36氪
学术:arXiv cs.AI / cs.CL / Hugging Face Daily Papers / papers with code
社区:Hacker News / Reddit r/ML / Reddit r/LocalLLaMA / GitHub Trending / Product Hunt / X/Twitter
预测:Polymarket

调整信源编辑 `scripts/fetch_news.py` 里的 `SOURCE_POOL` 字典。

---

## 🔧 自定义

### 改视觉/布局

直接编辑 `index.html` / `archive.html` / `archive-view.html`,git push 即可。

### 加新词条

编辑 `data/terms.json`,加一个条目:
```json
"你的术语": {
  "name": "显示名",
  "category": "分类",
  "summary": "一句话",
  "detail": "详细解释",
  "links": [{"label": "参考", "url": "https://..."}]
}
```
任何 HTML / 词条里的术语 hover 都会自动显示这张卡。

### 加新闻(手动)

编辑 `data/news.json`,加一条:
```json
{
  "id": "n19",
  "rank": 19,
  "category": "headline",   // headline/company/paper/industry/social/rising
  "title": "标题",
  "source": "来源",
  "time": "2026-06-03",
  "heat": {
    "score": 5000,
    "level": "热",            // 爆/热/中/新星
    "sources": ["hn", "x"],
    "breakdown": "明细"
  },
  "comments": 100,
  "summary": "摘要",
  "tags": ["标签1"],
  "terms": ["词条1"]
}
```

---

## 📜 License

MIT
