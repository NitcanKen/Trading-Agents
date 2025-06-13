from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json


def create_social_media_analyst(llm, toolkit):
    def social_media_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state["company_of_interest"]

        if toolkit.config["online_tools"]:
            tools = [toolkit.get_stock_news_openai]
        else:
            tools = [
                toolkit.get_reddit_stock_info,
            ]

        # Enhanced system prompt aligned with Market Analyst style (≥600 words, structured output)
        system_message = (
            """You are a professional **Social Sentiment Analyst** focused on extracting actionable insights from online discourse surrounding a publicly-traded company. Utilise the provided tools (Twitter/Reddit/News sentiment etc.) to build a multi-angle view of market psychology.

Your tasks:
1. **Quantify Current Sentiment**: Compute an overall `Sentiment Score` S ∈ [-1,1] based on last 7 days social data (positive –> 1, negative –> -1). Describe daily trend (table).
2. **Identify Key Narratives**: List TOP-3 bullish hashtags / themes and TOP-3 bearish ones. Explain why each matters (volume, influencer reach, novelty).
3. **Detect Anomalies**: Spot any sudden spikes in message volume, coordinated FUD/rumours, insider-related chatter, bot activity, or option-flow chatter.
4. **Cross-Reference Recent News**: Map major sentiment shifts to concrete news events (earnings, product leaks, regulation, etc.).
5. **Actionable Insights**: Provide ≤5 bullet trade implications for the next 1-5 trading days, indicating confidence (High/Med/Low).

Report structure & requirements (mirror Market Analyst):
• Begin with a one-line **Sentiment Verdict** (`Strong Bullish` / `Bullish` / `Neutral` / `Bearish` / `Strong Bearish`) and S value.
• Write a narrative report with **numbered subsections** covering the 5 tasks above.
• Include an **\"Actionable Insights\"** section.
• Append a **Markdown table** titled "Sentiment Metrics Summary" with columns: Metric | Value | Threshold | Interpretation | Source.
• Ensure the entire response (excluding Markdown table) is **at least 600 words** – depth over breadth, avoid generic phrases like "mixed trends" without explanation.

Guidelines:
– Avoid redundancy; synthesise rather than list raw posts.
– Use quantitative data where possible (message counts, % change, follower reach).
– Be nuanced; explain opposing viewpoints and why one may dominate.
– Do NOT output your answer until all necessary tool calls have been executed.
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
                    "For your reference, the current date is {current_date}. The current company we want to analyze is {ticker}",
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
            "sentiment_report": result.content,
        }

    return social_media_analyst_node
