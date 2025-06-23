"""
Setup script for the TradingAgents package.
"""

from setuptools import setup, find_packages

setup(
    name="tradingagents",
    version="0.2.3",
    description="Multi-Agents LLM Financial Trading Framework with GUI Interface",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="TradingAgents Team",
    author_email="yijia.xiao@cs.ucla.edu",
    url="https://github.com/TauricResearch/TradingAgents",
    packages=find_packages(),
    install_requires=[
        "typing-extensions",
        "langchain-openai",
        "langchain-experimental",
        "pandas",
        "yfinance",
        "praw",
        "feedparser",
        "stockstats",
        "eodhd",
        "langgraph",
        "chromadb",
        "setuptools",
        "backtrader",
        "akshare",
        "tushare",
        "finnhub-python",
        "parsel",
        "requests",
        "tqdm",
        "pytz",
        "redis",
        "chainlit",
        "rich",
        "questionary",
        "streamlit",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "mypy",
        ],
        "gui": [
            "streamlit",
            "pandas",
        ],
    },
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "tradingagents=cli.main:app",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="trading, finance, llm, multi-agent, ai, machine-learning, investment",
    project_urls={
        "Bug Reports": "https://github.com/TauricResearch/TradingAgents/issues",
        "Source": "https://github.com/TauricResearch/TradingAgents",
        "Documentation": "https://github.com/TauricResearch/TradingAgents/blob/main/README.md",
    },
)
