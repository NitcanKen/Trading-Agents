import sys
from datetime import datetime

from tradingagents.agents.utils.agent_utils import Toolkit


def main():
    """Quick functional test for all primary technical indicators using online data."""
    # ensure we are using online tools
    toolkit = Toolkit(config={"online_tools": True})

    symbol = "AAPL"  # choose a highly-liquid ticker for reliability
    curr_date = datetime.today().strftime("%Y-%m-%d")

    indicators = [
        # Moving Averages
        "close_50_sma",
        "close_200_sma",
        "close_10_ema",
        # MACD related
        "macd",
        "macds",
        "macdh",
        # Momentum
        "rsi",
        "mfi",
        # Volatility / Bollinger
        "boll",
        "boll_ub",
        "boll_lb",
        "bb_width",
        "atr",
        # Volume weighted
        "vwma",
        # Trend strength
        "adx",
    ]

    success, failed = 0, 0
    for ind in indicators:
        try:
            tool_call = toolkit.get_stockstats_indicators_report_online
            # LangChain tools require .invoke with an input dict of arguments
            result = tool_call.invoke(
                {
                    "symbol": symbol,
                    "indicator": ind,
                    "curr_date": curr_date,
                    "look_back_days": 5,
                }
            )
            print(result)
            success += 1
        except Exception as exc:
            print(f"[FAIL] {ind}: {exc}")
            failed += 1

    print("\nSummary ->", success, "passed,", failed, "failed")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main() 