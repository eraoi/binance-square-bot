# Binance Square Daily News Bot

每天自动抓取国际与加密新闻，生成适合 Binance Square 的中文简报，并通过 Binance Square OpenAPI 发布。

## 功能

- 每天自动运行，默认日本时间 08:00
- 抓取国际、宏观、科技/AI、加密新闻
- 可选使用 OpenAI API 生成更自然的中文总结与市场影响分析
- 没有 OpenAI API Key 时也可运行，会退化为标题精选 + 规则化市场影响提示
- 自动调用 Binance Square OpenAPI 发布
- 支持手动运行和 Dry Run
- 日志中不会打印完整 Binance API Key

## 你需要添加的 GitHub Secrets

进入仓库：

Settings → Secrets and variables → Actions → New repository secret

添加：

### 必需

`BINANCE_SQUARE_OPENAPI_KEY`

填你的 Binance Square OpenAPI Key。

### 可选，但强烈推荐

`OPENAI_API_KEY`

用于把英文新闻整理成更自然、简洁的中文币安广场稿件。

如果不添加，程序仍可运行，但内容质量会明显低一些。

## 运行方式

### 自动运行

GitHub Actions 默认每天：

- 23:00 UTC
- 日本时间 08:00

### 手动测试

进入：

Actions → Binance Square Daily News → Run workflow

建议第一次选择：

`dry_run = true`

这样只生成文章并打印预览，不发布。

确认内容正常后，再用：

`dry_run = false`

进行真实发布。

## 新闻来源

程序使用公开 RSS 源，默认包括：

- BBC World
- The Guardian World
- CoinDesk
- Cointelegraph

你可以在 `src/news.py` 中修改。

## Binance Square API

发布接口：

`POST https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add`

程序通过：

`X-Square-OpenAPI-Key`

请求头鉴权。

## 安全

不要：

- 把 API Key 写进代码
- 把 API Key 提交到 Git
- 把 API Key 发到公开 Issue
- 把 API Key 放进 README

只放 GitHub Secrets。

## 本地运行

Python 3.11+

```bash
pip install -r requirements.txt

export BINANCE_SQUARE_OPENAPI_KEY="your_key"
export OPENAI_API_KEY="optional"

python -m src.main --dry-run
```

真实发布：

```bash
python -m src.main
```

## 说明

自动发帖属于无人值守外部发布行为。建议先 Dry Run 几天，观察新闻筛选和措辞，再开启每日自动发布。
