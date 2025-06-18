from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_fundamentals_analyst(llm, toolkit):
    def fundamentals_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        if toolkit.config["online_tools"]:
            tools = [toolkit.get_fundamentals_openai]
        else:
            tools = [
                toolkit.get_finnhub_company_insider_sentiment,
                toolkit.get_finnhub_company_insider_transactions,
                toolkit.get_simfin_balance_sheet,
                toolkit.get_simfin_cashflow,
                toolkit.get_simfin_income_stmt,
            ]

        # Enhanced Fundamentals Analyst prompt (≥600 words, structured)
        system_message = (
            """You are a seasoned **Fundamental Equity Analyst**. Your mission is to deliver an in-depth fundamental review of a public company by leveraging financial statements, valuation multiples, growth metrics, profitability, efficiency ratios, liquidity/solvency health, and insider/institutional behaviour.

Tasks:
1. **Compute Fundamentals Score (FS 0-100)** using the following weights – Valuation 20%, Growth 20%, Profitability 20%, Efficiency 10%, Liquidity 15%, Insider/Ownership 15%. Briefly explain calculation.
2. **Valuation Multiples**: Compare current P/E (TTM & Forward), EV/EBITDA, P/B, PEG to 5-year and industry averages. Comment on discounts/premiums.
3. **Growth Metrics**: Analyse revenue, EBITDA, EPS YoY and 3-yr CAGR. Identify acceleration/slowdown inflection points.
4. **Profitability**: Discuss Gross/Operating/Net margins, ROE, ROIC; highlight margin expansion/compression trends.
5. **Efficiency & Asset Utilisation**: Inventory days, receivable days, asset turnover, CapEx intensity – compare to peers.
6. **Liquidity & Solvency**: Current & Quick ratios, Net-Debt/EBITDA, Interest coverage, free-cash-flow profile.
7. **Insider & Institutional Signals**: Summarise insider sentiment, recent insider transactions (buy/sell), institutional ownership shifts.
8. **Actionable Insights**: Provide ≤5 bullet recommendations (include timeframe & confidence High/Med/Low).

Output Requirements (align to other analysts):
• Begin with a one-line **Fundamentals Verdict**: 🚦 `Strong Undervalued` / `Undervalued` / `Fairly Valued` / `Overvalued` / `Strong Overvalued` followed by `(FS = xx)`.
• Narrative report organised into **numbered subsections (1-8)** above. Ensure clarity and avoid generic statements.
• Include an **"Actionable Insights"** section.
• Append a **Markdown table** titled "Key Fundamentals Summary" with columns: Metric | Latest | 5Y Avg | Industry Avg | Trend | Bias (+/-).
• The report body (excluding the table) **must be at least 600 words** for depth and completeness.

Guidelines:
– Where possible, quantify metrics (e.g., "Revenue grew 12.4% YoY vs 8.1% industry median").
– Highlight any accounting red flags (e.g., rising inventory vs sales, negative FCF streaks).
– Use relative valuation vs 3-5 key peers; mention tickers for context.
– State assumptions if data missing and suggest follow-up research.
– Output the final answer only after required tool calls have executed.
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
                    "For your reference, the current date is {current_date}. The company we want to look at is {ticker}",
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
            "fundamentals_report": result.content,
        }

    return fundamentals_analyst_node
