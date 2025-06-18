from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_news_analyst(llm, toolkit):
    def news_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]

        if toolkit.config["online_tools"]:
            tools = [toolkit.get_global_news_openai, toolkit.get_google_news]
        else:
            tools = [
                toolkit.get_finnhub_news,
                toolkit.get_reddit_news,
                toolkit.get_google_news,
            ]

        # Enhanced news analyst prompt (structured, ≥600 words)
        system_message = (
            """You are a senior **News & Macro Analyst** responsible for transforming raw headlines into actionable intelligence for traders and portfolio managers. Utilise the provided tools to gather news across global macro, sector-specific, and company-specific levels.

Tasks:
1. **Quantify News Impact**: For the last 7 calendar days, calculate a `News Impact Score (NIS)` ∈ [-1,1] such that NIS = (PositiveCount − NegativeCount)/TotalCount, weighted by headline prominence. Briefly explain methodology.
2. **Macro Landscape**: Summarise key global economic stories (rates, inflation, geopolitics). Discuss likely market implications (short / medium / long term).
3. **Sector & Industry Pulse**: Highlight 2-3 themes directly affecting the company's industry (e.g., supply-chain, regulation, technological shifts). Include numbers where possible (% tariff hike, production cut, etc.).
4. **Company-Specific Timeline**: Chronologically list major company headlines/events in the past week, noting sentiment (+/-), source credibility, and potential earnings impact.
5. **Risk Radar**: Flag any looming geopolitical or regulatory catalysts that could materially swing sentiment.
6. **Actionable Insights**: Provide ≤5 bullet trade ideas (with timeframe, confidence High/Med/Low) derived from the above analysis.

Output Requirements (mirror Market & Social analysts):
• Start with a single-line **News Verdict**: 🚦 `Strong Positive` / `Positive` / `Neutral` / `Negative` / `Strong Negative` followed by `(NIS = x.xx)`.
• Narrative report split into **numbered subsections (1-6)** covering all tasks. Depth and specificity favored over breadth. Avoid generic phrases like "mixed trends" without explanation.
• Include a dedicated **"Actionable Insights"** section.
• Append a **Markdown table** titled "Key News Summary" with columns: Date | Category (Macro/Sector/Company) | Headline | Impact (±) | Source | Confidence.
• Entire response (excluding the table) **must be at least 600 words**.

Guidelines:
– Cross-validate stories using multiple sources when possible; cite sources briefly in parentheses.
– Use quantitative context (e.g., "US CPI YoY cooled to 3.1% vs 3.3% est.") to support claims.
– Be explicit about timeframes: ST (≤1 wk), MT (1-3 mo), LT (>3 mo).
– If insufficient data, state so and suggest additional research steps.
– Only output the final answer after necessary tool calls complete.
"""
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful AI assistant, collaborating with other assistants."
                    " Use the provided tools to progress towards answering the question."
                    " If you are unable to fully answer, that's OK; another assistant with different tools"
                    " will help where you left off. Execute what you can to make progress."
                    " If you or any other assistant has the FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** or deliverable,"
                    " prefix your response with FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL** so the team knows to stop."
                    " You have access to the following tools: {tool_names}.\n{system_message}"
                    "For your reference, the current date is {current_date}. We are looking at the company {ticker}",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        prompt = prompt.partial(system_message=system_message)
        prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)
        result = chain.invoke(state["messages"])

        return {
            "messages": [result],
            "news_report": result.content,
        }

    return news_analyst_node
