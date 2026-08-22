from __future__ import annotations

import os
from typing import Iterable

from news import NewsItem


SYSTEM_PROMPT = """
你是一名面向 Binance Square 的中文全球市场新闻编辑。

你的任务是把提供的英文新闻材料，整理成一篇可直接发布到币安广场的中文每日市场简报。

写作要求：

1. 全文使用自然中文。
2. 英文标题不要原样照搬，要理解后重新概括。
3. 优先选择真正重要的事件，重点覆盖：
   - BTC、ETH、加密市场
   - 美国经济、美联储、美元、美债、通胀
   - 全球股市、黄金、原油
   - 重大地缘政治
   - AI、芯片、科技行业
   - 加密监管与机构资金
4. 删除娱乐、地方小新闻、影响很小的政治新闻。
5. 不要为了凑数量强行保留低价值新闻。
6. 每条新闻使用这个逻辑：
   “发生了什么”
   然后说明：
   “为什么重要 / 对市场可能有什么影响”
7. 不要机械重复“关注其对BTC/ETH的影响”之类模板句。
8. 根据不同新闻具体分析：
   - 对 BTC / ETH
   - 对美元
   - 对美债收益率
   - 对黄金
   - 对原油
   - 对全球风险偏好
9. 分清事实与分析。
   已经发生的事实直接陈述。
   对未来影响使用“可能、值得关注、市场或将”等表达。
10. 禁止喊单、投资承诺、预测具体涨跌目标。
11. 不要夸大新闻重要性。
12. 如果多篇新闻实际上讲同一个事件，要合并。
13. 最终保留 5 到 7 条最值得看的新闻。
14. 每条控制在 80 到 160 个中文字符左右。
15. 总长度适合手机阅读，尽量控制在 1500 到 2200 个中文字符。
16. 排版清楚，但不要使用 Markdown 表格。
17. 可以使用少量适合 Binance Square 的 emoji。

输出结构严格按照下面的风格：

🌍 8月XX日全球与加密市场速览

1. 【简洁中文标题】
发生了什么……
市场影响：……

2. 【简洁中文标题】
发生了什么……
市场影响：……

……

📊 今日市场情绪：偏多 / 中性 / 偏空

用 1 到 2 句话解释判断理由。

🔎 今日最值得关注
用一句话指出今天最关键的市场主线。

最后提出一个适合币安广场评论区讨论的问题。

来源：Reuters、AP、BBC、CoinDesk 等实际使用到的来源

额外要求：
不要出现英文新闻标题堆砌。
不要逐条复制摘要。
不要写“以下是新闻总结”。
不要输出任何关于自己如何分析的说明。
"""


def make_material(items: Iterable[NewsItem]) -> str:
    chunks = []

    for idx, item in enumerate(items, 1):
        chunks.append(
            f"""
新闻 {idx}
来源：{item.source}
标题：{item.title}
摘要：{item.summary}
链接：{item.link}
发布时间：{item.published}
""".strip()
        )

    return "\n\n".join(chunks)


def summarize_with_openai(items: list[NewsItem]) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("[warn] OPENAI_API_KEY not found, using fallback mode.")
        return None

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5-mini"
        )

        response = client.responses.create(
            model=model,
            instructions=SYSTEM_PROMPT,
            input=make_material(items),
        )

        text = (response.output_text or "").strip()

        if not text:
            print("[warn] OpenAI returned empty text.")
            return None

        return text

    except Exception as exc:
        print(f"[warn] OpenAI summarization failed: {exc}")
        return None


def fallback_summary(items: list[NewsItem]) -> str:
    lines = [
        "🌍 今日全球与加密市场速览",
        "",
        "AI 摘要暂时不可用，以下为自动筛选的新闻标题：",
        ""
    ]

    for idx, item in enumerate(items[:6], 1):
        lines.append(f"{idx}. {item.title}")
        lines.append(f"来源：{item.source}")
        lines.append("")

    lines.append("📊 今日市场情绪：中性")
    lines.append("当前请结合宏观流动性、地缘风险和加密市场资金流继续观察。")
    lines.append("")
    lines.append("你今天最关注哪个市场变量？")

    return "\n".join(lines)


def build_post(items: list[NewsItem]) -> str:
    ai_result = summarize_with_openai(items)

    if ai_result:
        return ai_result

    return fallback_summary(items)
