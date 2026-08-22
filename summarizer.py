from __future__ import annotations

from datetime import datetime
from typing import Iterable

from news import NewsItem


def contains(text: str, words: list[str]) -> bool:
    text = text.lower()
    return any(word.lower() in text for word in words)


def zh_title(item: NewsItem) -> str:
    text = f"{item.title} {item.summary}".lower()

    if contains(text, ["bitcoin", "btc"]):
        if contains(text, ["77k", "support", "rally", "surge", "jump"]):
            return "BTC重回关键价格区间，市场关注后续支撑"
        if contains(text, ["etf"]):
            return "比特币ETF资金动向成为市场焦点"
        return "比特币市场出现新的重要变化"

    if contains(text, ["ethereum", "eth"]):
        return "以太坊市场出现新的资金与价格变化"

    if contains(text, ["fed", "federal reserve", "interest rate", "rates"]):
        return "美联储政策预期继续影响全球风险资产"

    if contains(text, ["inflation", "cpi", "ppi"]):
        return "通胀数据继续牵动利率与风险资产定价"

    if contains(text, ["oil", "crude", "pipeline", "opec"]):
        return "能源市场出现新变化，油价风险值得关注"

    if contains(text, ["tariff", "trade war", "trade"]):
        return "贸易政策出现新变化，全球市场关注后续影响"

    if contains(text, ["war", "missile", "attack", "ceasefire", "iran", "israel", "ukraine", "russia"]):
        return "地缘局势继续升温，避险情绪受到关注"

    if contains(text, ["ai", "artificial intelligence", "nvidia", "chip", "semiconductor"]):
        return "AI与芯片行业出现新进展"

    if contains(text, ["gold"]):
        return "黄金维持强势，避险资金动向值得关注"

    if contains(text, ["stablecoin", "crypto regulation", "sec", "cftc"]):
        return "加密监管与行业政策出现新进展"

    return item.title[:50]


def event_summary(item: NewsItem) -> str:
    text = f"{item.title} {item.summary}".lower()

    if contains(text, ["bitcoin", "btc"]):
        return "比特币近期价格和资金表现出现明显变化，市场正在重新评估关键支撑位与后续风险偏好。"

    if contains(text, ["ethereum", "eth"]):
        return "以太坊近期价格和资金流出现变化，市场开始重新关注ETH相对BTC的表现。"

    if contains(text, ["fed", "federal reserve", "interest rate", "rates"]):
        return "市场正在重新评估美联储未来利率路径，美元和美债收益率也因此受到影响。"

    if contains(text, ["inflation", "cpi", "ppi"]):
        return "最新通胀相关消息重新影响市场对利率和货币政策的预期。"

    if contains(text, ["oil", "crude", "pipeline", "opec"]):
        return "能源市场出现新的供应或政策变化，油价和通胀预期可能随之波动。"

    if contains(text, ["tariff", "trade war", "trade"]):
        return "最新贸易政策出现调整，相关国家之间的关税与产业链预期受到市场关注。"

    if contains(text, ["war", "missile", "attack", "ceasefire", "iran", "israel", "ukraine", "russia"]):
        return "最新地缘事件继续影响能源、黄金和全球避险情绪。"

    if contains(text, ["ai", "artificial intelligence", "nvidia", "chip", "semiconductor"]):
        return "AI和芯片产业继续出现新的资本开支、产品或需求变化。"

    if contains(text, ["gold"]):
        return "黄金近期保持强势，反映部分资金仍在寻求避险和对冲。"

    if item.summary:
        summary = item.summary.strip()
        if len(summary) > 120:
            summary = summary[:120] + "。"
        return summary

    return "这条新闻正在受到市场关注，后续发展值得继续观察。"


def market_impact(item: NewsItem) -> str:
    text = f"{item.title} {item.summary}".lower()

    if contains(text, ["bitcoin", "btc", "ethereum", "eth"]):
        return "市场影响：短线可能直接影响BTC与ETH的资金流和波动率，同时带动整体加密市场风险偏好。"

    if contains(text, ["fed", "interest rate", "inflation", "cpi", "ppi", "jobs", "gdp"]):
        return "市场影响：如果利率预期继续偏高，美元和美债收益率可能维持强势，并压制高波动风险资产；若预期转向宽松，则可能利好加密资产和成长股。"

    if contains(text, ["oil", "crude", "pipeline", "opec"]):
        return "市场影响：油价上涨可能重新推高通胀预期，并通过利率和风险偏好间接影响BTC、科技股和黄金。"

    if contains(text, ["war", "missile", "attack", "ceasefire", "iran", "israel", "ukraine", "russia"]):
        return "市场影响：地缘风险升温通常利好黄金和避险资产，同时可能压制全球风险偏好，并放大能源价格波动。"

    if contains(text, ["tariff", "trade war", "trade"]):
        return "市场影响：贸易摩擦可能推高成本与通胀预期，并影响美元、股票和加密市场风险偏好。"

    if contains(text, ["ai", "artificial intelligence", "nvidia", "chip", "semiconductor"]):
        return "市场影响：AI投资和芯片需求继续影响科技股估值，也会间接影响全球风险资金对高成长资产的配置。"

    if contains(text, ["gold"]):
        return "市场影响：黄金走强通常意味着避险需求或美元预期发生变化，也值得观察其与BTC之间的资金轮动。"

    return "市场影响：这件事可能通过全球风险偏好、美元或资金流变化间接影响加密市场。"


def sentiment(items: list[NewsItem]) -> tuple[str, str]:
    bullish = 0
    bearish = 0

    for item in items:
        text = f"{item.title} {item.summary}".lower()

        if contains(text, ["rally", "surge", "jump", "gain", "approval", "inflow"]):
            bullish += 1

        if contains(text, ["war", "attack", "inflation", "tariff", "selloff", "drop", "sanction"]):
            bearish += 1

    if bullish >= bearish + 2:
        return "偏多", "风险资产动能相对更强，市场资金情绪有所改善，但仍需关注宏观和地缘变量。"

    if bearish >= bullish + 2:
        return "偏空", "宏观或地缘风险占据主导，风险偏好受到压制，加密市场短线波动可能加大。"

    return "中性", "当前多空因素交织，市场仍在等待更明确的宏观和资金面信号。"


def build_post(items: list[NewsItem]) -> str:
    now = datetime.utcnow()
    month = now.month
    day = now.day

    selected = items[:6]

    lines = [
        f"🌍 {month}月{day}日全球与加密市场速览",
        ""
    ]

    for idx, item in enumerate(selected, 1):
        lines.append(f"{idx}. {zh_title(item)}")
        lines.append(event_summary(item))
        lines.append(market_impact(item))
        lines.append(f"来源：{item.source}")
        lines.append("")

    mood, reason = sentiment(selected)

    lines.append(f"📊 今日市场情绪：{mood}")
    lines.append(reason)
    lines.append("")

    if selected:
        first = zh_title(selected[0])
        lines.append("🔎 今日最值得关注")
        lines.append(f"今天最值得跟踪的主线是：{first}。")
        lines.append("")

    lines.append("你觉得今天最可能主导BTC波动的是宏观、地缘局势，还是加密市场自身资金流？")

    return "\n".join(lines)
