# 🚀 TradingAgents Quick Start Guide

Get started with TradingAgents in under 5 minutes! This guide covers both CLI and GUI interfaces.

## ⚡ Prerequisites

1. **Python 3.10+** installed
2. **API Keys** ready:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   export FINNHUB_API_KEY="your_finnhub_api_key"
   ```

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/TauricResearch/TradingAgents.git
cd TradingAgents

# Create virtual environment
conda create -n tradingagents python=3.13
conda activate tradingagents

# Install dependencies
pip install -r requirements.txt
```

## 🖥️ GUI Interface (Recommended)

### Start the GUI
```bash
streamlit run streamlit_app.py
```
Or on Windows:
```bash
./run_gui.bat
```

### Quick Analysis Steps
1. **Open browser** → `http://localhost:8501`
2. **Configure** (sidebar):
   - Select models (e.g., o4-mini, gpt-4o-mini)
   - Choose analysts (Market, Social, News, Fundamentals)
   - Set debate rounds (1-5)
3. **Analyze** (New Analysis tab):
   - Enter ticker (e.g., `AAPL`)
   - Select date
   - Click `🚀 Run Analysis`
4. **Review Results** → 5 organized tabs with detailed insights
5. **View History** → History tab shows all past analyses

### Key GUI Features
- ✅ **Two-tab interface**: New Analysis + History
- ✅ **Real-time progress tracking**
- ✅ **Color-coded results** (🟢 BUY, 🔴 SELL, 🟡 HOLD)
- ✅ **Complete analysis history** with search and download
- ✅ **Reset functionality** for ChromaDB issues
- ✅ **Professional styling** with organized tabs

## 💻 CLI Interface

### Start CLI
```bash
python -m cli.main
```

### Quick CLI Steps
1. **Select ticker** from the list or enter custom
2. **Choose date** for analysis
3. **Configure** LLMs and parameters
4. **Watch** agents work in real-time
5. **Review** results in terminal

## 📊 Understanding Results

### Analysis Components
1. **📈 Analyst Team Reports**
   - Market Analysis (technical indicators)
   - Social Sentiment (social media analysis)
   - News Analysis (news impact assessment)
   - Fundamentals Analysis (financial metrics)

2. **💭 Research Team Debate**
   - Bull Researcher arguments (positive outlook)
   - Bear Researcher arguments (negative outlook)
   - Research Manager decision (balanced assessment)

3. **📈 Trading Plan**
   - Trader's investment strategy
   - Entry/exit recommendations
   - Risk considerations

4. **⚖️ Risk Management**
   - Multi-perspective risk analysis
   - Risk mitigation strategies
   - Final risk assessment

5. **🏛️ Portfolio Management**
   - Final BUY/SELL/HOLD decision
   - Position sizing recommendations
   - Overall portfolio impact

### Decision Types
- **🟢 BUY**: Strong positive signals, good entry opportunity
- **🔴 SELL**: Strong negative signals, recommend exit
- **🟡 HOLD**: Mixed signals, maintain current position
- **📋 Other**: Custom decision with specific reasoning

## 📁 File Organization

All analyses are automatically saved:
```
analyses/
├── AAPL_20240115_143022_analysis.txt
├── TSLA_20240115_151045_analysis.txt
└── SPY_20240116_092314_analysis.txt
```

## 🔧 Quick Troubleshooting

### ChromaDB Issues
- **GUI**: Click the `🔄 Reset` button
- **CLI**: Restart the application
- **Manual**: Delete any `chroma_db/` folders

### API Errors
- Verify API keys are set correctly
- Check API rate limits
- Try using lighter models (o4-mini, gpt-4o-mini)

### Memory Issues
- Reduce number of selected analysts
- Lower debate rounds (1-2)
- Use smaller models

## 🎯 Recommended Configurations

### **Quick Analysis** (Fast & Cost-Effective)
- **Models**: o4-mini + gpt-4o-mini
- **Analysts**: Market + News
- **Debate Rounds**: 1
- **Risk Rounds**: 1

### **Comprehensive Analysis** (Thorough)
- **Models**: gpt-4.1 + gpt-4o-mini
- **Analysts**: All (Market, Social, News, Fundamentals)
- **Debate Rounds**: 3
- **Risk Rounds**: 2

### **Research Focus** (Deep Analysis)
- **Models**: o3 + gpt-4.1-mini
- **Analysts**: All analysts
- **Debate Rounds**: 5
- **Risk Rounds**: 3

## 📚 Next Steps

1. **Explore History** → Use GUI History tab to review patterns
2. **Try Different Tickers** → Compare analyses across sectors
3. **Experiment with Models** → Test different LLM combinations
4. **Review Documentation** → Check [README.md](README.md) and [GUI_Setup_Guide.md](GUI_Setup_Guide.md)
5. **Join Community** → [Discord](https://discord.com/invite/hk9PGKShPK) | [GitHub](https://github.com/TauricResearch/)

## 🔗 Quick Links

- 📖 [Full Documentation](README.md)
- 🖥️ [GUI Setup Guide](GUI_Setup_Guide.md)
- 🔧 [ChromaDB Troubleshooting](CHROMADB_RESET_SOLUTION.md)
- 📋 [Changelog](CHANGELOG.md)
- 🐛 [Report Issues](https://github.com/TauricResearch/TradingAgents/issues)

---

**Happy Trading! 📈**

> **Disclaimer**: TradingAgents is for research purposes. Past performance does not guarantee future results. Not financial advice. 