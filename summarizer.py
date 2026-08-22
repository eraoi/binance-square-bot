from __future__ import annotations

import os
from typing import Iterable

from news import NewsItem


SYSTEM_PROMPT = """你是一名面向 Binance Square 的全球市场新闻编辑。
请把提供的新闻材料整理成一篇可直接发布的中文市场简报。

要求：
1. 只使用材料中出现的事实，不编造数字、日期或事件。
2. 优先保留真正影响 BTC、ETH、风险资产、美元、黄金、油价、全球风险偏好的事件。
3. 每条用“发生了什么 + 为什么重要/可能影响什么”的结构。
4. 明确区分事实和分析，分析使用“可能、值得关注、市场可能”等措辞。
5. 不做投资承诺，不喊单。
6. 总长度控制在约 1200 到 1800 个中文字符，过长时主动压缩。
7. 最后给出“今日市场情绪：偏多 / 中性 / 偏空”三选一，并用一句话解释。
8. 最后一行给一个适合 Binance Square 讨论的问题。
9. 文末用“来源：”列出本次实际使用到的媒体名称，避免贴一长串 URL。
10. 输出纯正文，不要 Markdown 表格。
"""


def make_material(items: Iterable[NewsItem]) -> str:
    chunks = []
    for idx, item in enumerate(items, 1):
        chunks.append(
            f"""[{idx}]
来源: {item.source}
标题: {item.title}
摘要: {item.summary}
链接: {item.link}
"""
        )
    return "\n".join(chunks)


def summarize_with_openai(items: list[NewsItem]) -> str | None:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        model = os.getenv("OPENAI_MODEL", "gpt-5-mini")

        response = client.responses.create(
            model=model,
            instructions=SYSTEM_PROMPT,
            input=make_material(items),
        )
        text = (response.output_text or "").strip()
        return text or None
    except Exception as exc:
        print(f"[warn] OpenAI summarization failed: {exc}")
        return None


def fallback_summary(items: list[NewsItem]) -> str:
    lines = ["🌍 今日全球与加密市场速览", ""]

    for idx, item in enumerate(items[:7], 1):
        title = item.title.strip()
        lower = f"{item.title} {item.summary}".lower()

        if any(x in lower for x in ["bitcoin", "btc", "ethereum", "eth", "crypto", "etf"]):
            impact = "关注其对加密市场资金流、风险偏好与 BTC/ETH 波动的影响。"
        elif any(x in lower for x in ["fed", "inflation", "rate", "treasury", "jobs", "gdp"]):
            impact = "宏观数据和利率预期可能影响美元、债券收益率以及加密资产估值。"
        elif any(x in lower for x in ["oil", "war", "missile", "sanction", "attack"]):
            impact = "地缘风险可能通过油价、避险情绪和通胀预期传导至全球市场。"
        elif any(x in lower for x in ["ai", "nvidia", "openai", "chip", "semiconductor"]):
            impact = "科技与 AI 资本开支变化值得关注，也可能影响成长股和风险资产情绪。"
        else:
            impact = "这条新闻可能影响全球风险偏好，值得继续观察后续发展。"

        lines.append(f"{idx}. {title}")
        lines.append(f"   {impact}")
        lines.append(f"   来源：{item.source}")
        lines.append("")

    lines.append("今日市场情绪：中性")
    lines.append("主要变量仍取决于宏观流动性、地缘风险和加密市场自身资金流。")
    lines.append("")
    lines.append("你觉得今天最可能主导 BTC 波动的是宏观、地缘局势，还是加密市场自身消息？")
    return "\n".join(lines)


def build_post(items: list[NewsItem]) -> str:
    return summarize_with_openai(items) or fallback_summary(items)
