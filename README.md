<p align="center">
  <img src="assets/TauricResearch.png" style="width: 60%; height: auto;">
</p>

<div align="center" style="line-height: 1;">
  <a href="https://arxiv.org/abs/2412.20138" target="_blank"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv"/></a>
  <a href="https://discord.com/invite/hk9PGKShPK" target="_blank"><img alt="Discord" src="https://img.shields.io/badge/Discord-TradingResearch-7289da?logo=discord&logoColor=white&color=7289da"/></a>
  <a href="./assets/wechat.png" target="_blank"><img alt="WeChat" src="https://img.shields.io/badge/WeChat-TauricResearch-brightgreen?logo=wechat&logoColor=white"/></a>
  <a href="https://x.com/TauricResearch" target="_blank"><img alt="X Follow" src="https://img.shields.io/badge/X-TauricResearch-white?logo=x&logoColor=white"/></a>
  <br>
  <a href="https://github.com/TauricResearch/" target="_blank"><img alt="Community" src="https://img.shields.io/badge/Join_GitHub_Community-TauricResearch-14C290?logo=discourse"/></a>
</div>

---

# TradingAgents: Multi-Agents LLM Financial Trading Framework (Original from https://github.com/TauricResearch/TradingAgents)

> 🎉 **TradingAgents** officially released! We have received numerous inquiries about the work, and we would like to express our thanks for the enthusiasm in our community.
>
> So we decided to fully open-source the framework. Looking forward to building impactful projects with you!

<div align="center">

🚀 [Quick Start](QUICK_START.md) | 📚 [TradingAgents](#tradingagents-framework) | ⚡ [Installation & CLI](#installation-and-cli) | 🖥️ [GUI Interface](#gui-interface) | 🎬 [Demo](https://www.youtube.com/watch?v=90gr5lwjIho) | 📦 [Package Usage](#tradingagents-package) | 🤝 [Contributing](#contributing) | 📄 [Citation](#citation)

</div>

## TradingAgents Framework

TradingAgents is a multi-agent trading framework that mirrors the dynamics of real-world trading firms. By deploying specialized LLM-powered agents: from fundamental analysts, sentiment experts, and technical analysts, to trader, risk management team, the platform collaboratively evaluates market conditions and informs trading decisions. Moreover, these agents engage in dynamic discussions to pinpoint the optimal strategy.

<p align="center">
  <img src="assets/schema.png" style="width: 100%; height: auto;">
</p>

> TradingAgents framework is designed for research purposes. Trading performance may vary based on many factors, including the chosen backbone language models, model temperature, trading periods, the quality of data, and other non-deterministic factors. [It is not intended as financial, investment, or trading advice.](https://tauric.ai/disclaimer/)

Our framework decomposes complex trading tasks into specialized roles. This ensures the system achieves a robust, scalable approach to market analysis and decision-making.

### Analyst Team
- Fundamentals Analyst: Evaluates company financials and performance metrics, identifying intrinsic values and potential red flags.
- Sentiment Analyst: Analyzes social media and public sentiment using sentiment scoring algorithms to gauge short-term market mood.
- News Analyst: Monitors global news and macroeconomic indicators, interpreting the impact of events on market conditions.
- Technical Analyst: Utilizes technical indicators (like MACD, RSI, ADX, and Bollinger Band Width) to detect trading patterns and forecast price movements.

<p align="center">
  <img src="assets/analyst.png" width="100%" style="display: inline-block; margin: 0 2%;">
</p>

### Researcher Team
- Comprises both bullish and bearish researchers who critically assess the insights provided by the Analyst Team. Through structured debates, they balance potential gains against inherent risks.

<p align="center">
  <img src="assets/researcher.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Trader Agent
- Composes reports from the analysts and researchers to make informed trading decisions. It determines the timing and magnitude of trades based on comprehensive market insights.

<p align="center">
  <img src="assets/risk.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

### Risk Management and Portfolio Manager
- Continuously evaluates portfolio risk by assessing market volatility, liquidity, and other risk factors. The risk management team evaluates and adjusts trading strategies, providing assessment reports to the Portfolio Manager for final decision.
- The Portfolio Manager approves/rejects the transaction proposal. If approved, the order will be sent to the simulated exchange and executed.

<p align="center">
  <img src="assets/trader.png" width="70%" style="display: inline-block; margin: 0 2%;">
</p>

## GUI Interface

TradingAgents now includes a beautiful, professional Streamlit-based web interface that makes it easy to run analyses and review results without command-line expertise.

### 🚀 Quick Start - GUI

Run the GUI with a single command:
```bash
streamlit run streamlit_app.py
```

Or use the convenient batch file on Windows:
```bash
./run_gui.bat
```

---
# 🚀 TradingAgents GUI Setup Guide

This guide will help you set up and run the beautiful Streamlit GUI for TradingAgents.

## 📋 Prerequisites for GUI Setup

You should have already:
- ✅ Cloned the repository
- ✅ Created a virtual environment
- ✅ Set up all API keys
- ✅ Python 3.10+ installed

## 🛠️ Setup Steps

### 1. Activate Your Virtual Environment

Open your terminal/PowerShell in your project directory and activate your virtual environment:

```bash
# Navigate to your project directory
cd TradingAgents

# Activate your virtual environment
# For conda:
conda activate tradingagents

# For venv on Windows:
.\venv\Scripts\Activate.ps1

# For venv on Linux/Mac:
source venv/bin/activate
```

### 2. Install Streamlit

Install the required Streamlit dependency:

```bash
pip install streamlit
```

Or install all requirements (which now includes Streamlit):

```bash
pip install -r requirements.txt
```

### 3. Run the GUI

You have two options:

#### Option A: Use the Batch File (Windows - Easiest)
Simply double-click `run_gui.bat` in the project folder.

#### Option B: Run Manually
```bash
streamlit run streamlit_app.py
```

### 4. Access the GUI

After running the command, you'll see output like:
```
Local URL: http://localhost:8501
Network URL: http://192.168.1.100:8501
```

Open your web browser and go to `http://localhost:8501`

## 🎯 How to Use the GUI

### 1. Main Interface Tabs

The GUI is organized into two main tabs:

#### 🚀 New Analysis Tab
This is where you run new stock analyses.

#### 📚 History Tab
View and explore all your previous analyses with detailed history management.

### 2. Configuration (Sidebar)
- **Models**: Choose from your available models (o4-mini, o3, gpt-4.1, etc.)
- **Debate Rounds**: Set how many rounds of debate between bull/bear researchers
- **Risk Rounds**: Set how many rounds of risk analysis discussion
- **Online Tools**: Enable/disable real-time data fetching
- **Analysts**: Select which analysts to include in the analysis

### 3. Analysis Input (New Analysis Tab)
- **Ticker Symbol**: Enter the stock symbol (e.g., AAPL, TSLA, SPY)
- **Analysis Date**: Choose the date for analysis (usually today)
- **Run Analysis**: Click the button to start the multi-agent analysis
- **Reset**: Clear system state and reset ChromaDB for analyzing new stocks

### 4. View Results (New Analysis Tab)
The results are organized in 5 tabs:
- **📊 Summary**: Executive summary and final decision
- **🔍 Analyst Reports**: Individual analyst team reports
- **💭 Research Debate**: Bull vs Bear arguments and manager decision
- **📈 Trading Plan**: Trader's investment plan
- **⚖️ Risk Analysis**: Risk management team analysis

### 5. Analysis History (History Tab)

**📊 Analysis Summary Table**
- View all past analyses in a sortable table
- See ticker, date, time, decision, and filename at a glance
- Quick overview of trading decisions with color-coded indicators

**🔍 Detailed Analysis Viewer**
- Select any historical analysis from the dropdown
- View complete analysis details in organized tabs:
  - **📊 Summary**: Key metrics and final decision
  - **🔍 Analyst Reports**: All team reports (Market, Social, News, Fundamentals)
  - **💭 Research Debate**: Bull vs Bear arguments and manager decision
  - **📈 Trading Plan**: Trading team recommendations
  - **⚖️ Risk Analysis**: Risk management analysis
  - **📄 Raw Data**: Full analysis file with download option

**📥 Download Capability**
- Download any analysis file for external use
- Files are saved in standard text format with complete details
- Perfect for sharing or further analysis

### 6. Saved Reports
All analysis results are automatically saved to the `.\analyses\` folder in `.txt` format with timestamps.

---
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


## 🎨 GUI Features

### Beautiful Interface
- Modern, clean design with professional styling
- Color-coded status indicators for each agent team
- Organized tabs for easy navigation
- Real-time progress tracking

### Comprehensive Configuration
- Easy model selection from your available models
- Adjustable analysis parameters
- Flexible analyst team selection
- Online/offline mode toggle

### Rich Results Display
- Executive summary with clear BUY/SELL/HOLD indicators
- Expandable sections for detailed reports
- Color-coded analysis outputs
- Automatic file saving with timestamps

### Analysis History Management
- Complete history of all analyses in one place
- Sortable summary table with key information
- Detailed viewer for any past analysis
- Download individual analysis files
- Easy comparison between different analyses

### Agent Status Tracking
- Visual representation of all agent teams
- Real-time status updates (Pending → Running → Completed)
- Team-based organization (Analyst, Research, Trading, Risk, Portfolio)

### System Management
- Built-in reset functionality for ChromaDB issues
- Clear system status indicators
- Session state management
- Automatic cleanup and organization

## 🔧 GUI Troubleshooting

### Port Already in Use
If port 8501 is busy, run with a different port:
```bash
streamlit run streamlit_app.py --server.port 8502
```

### Import Errors
Make sure your virtual environment is activated and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### API Key Issues
Ensure all your API keys are properly set in your environment variables:
- `OPENAI_API_KEY`
- `FINNHUB_API_KEY`
- Any other API keys required by your data sources

### Memory Issues
If you encounter memory issues with large analyses:
- Try reducing the number of selected analysts
- Reduce debate/risk discussion rounds
- Use lighter models (like gpt-4o-mini)

## 📁 GUI File Structure

After setup, your project will have these key files:
```
TradingAgents/
├── streamlit_app.py          # Main GUI application
├── run_gui.bat              # Easy launcher for Windows
├── analyses/                # Auto-generated analysis results
│   ├── AAPL_20240115_143022_analysis.txt
│   ├── TSLA_20240115_151045_analysis.txt
│   └── SPY_20240116_092314_analysis.txt
├── requirements.txt         # Updated with all dependencies
└── ... (existing files)
```

---

# ChromaDB Reset Solution

## Problem
The TradingAgents application was experiencing ChromaDB connection issues after running the first analysis, with errors like:
```
❌ Analysis failed: Could not connect to tenant default_tenant. Are you sure it exists?
```

This required users to restart the entire application to analyze another stock.

## Root Cause
- ChromaDB was creating persistent storage files that remained locked after analysis completion
- The ChromaDB client instances weren't being properly cleaned up between analyses
- Persistent ChromaDB files in the `chroma_db/` directory were causing tenant connection conflicts

## Solution Implemented

### 1. Enhanced Memory Management (`tradingagents/agents/utils/memory.py`)

**Key improvements:**
- **In-memory first approach**: ChromaDB now defaults to in-memory storage (faster, no cleanup needed)
- **Temporary directory fallback**: If in-memory fails, uses temporary directories that are properly tracked
- **Robust reset functionality**: Added `reset()` method that properly cleans up ChromaDB instances
- **Windows-friendly cleanup**: Handles Windows file locking issues with delayed cleanup at program exit
- **Automatic garbage collection**: Forces garbage collection to release file handles before cleanup

**New features:**
```python
# In-memory ChromaDB (preferred)
settings = Settings(allow_reset=True, is_persistent=False)

# Automatic cleanup at program exit
atexit.register(_cleanup_at_exit)

# Robust reset method
def reset(self):
    # Properly cleans up ChromaDB and reinitializes
```

### 2. TradingAgentsGraph Reset (`tradingagents/graph/trading_graph.py`)

**Added reset functionality:**
```python
def reset(self):
    """Reset all ChromaDB memories and clear internal state"""
    # Resets all 5 memory instances (bull, bear, trader, invest_judge, risk_manager)
    # Clears internal state (curr_state, ticker, log_states_dict)
    # Handles failures gracefully with complete reinitialization
```

### 3. Streamlit UI Enhancement (`streamlit_app.py`)

**New features:**
- **🔄 Reset Button**: Added to the main UI for easy access
- **System Status Display**: Shows current system state (agents ready, analysis complete, etc.)
- **Session State Management**: Properly manages TradingAgentsGraph instances across sessions
- **Persistent ChromaDB Cleanup**: Removes any leftover ChromaDB files

**UI improvements:**
```python
# Reset button with helpful tooltip
reset_button = st.button(
    "🔄 Reset",
    type="secondary",
    help="Reset ChromaDB and clear system state for analyzing new stocks"
)

# Informative status messages
if st.session_state.trading_graph is not None:
    st.info("🤖 Agents initialized and ready for analysis")
```

### 4. Testing Infrastructure (`test_reset_functionality.py`)

**Comprehensive testing:**
- Tests individual memory reset functionality
- Tests complete TradingAgentsGraph reset
- Includes cleanup verification
- Provides clear pass/fail feedback

## How to Use ChromaDB Reset

### Method 1: Using the Reset Button (Recommended)
1. Run an analysis on any stock
2. If you want to analyze another stock, click the **🔄 Reset** button
3. The system will clean up ChromaDB and reinitialize everything
4. You can now analyze any other stock without issues

### Method 2: Programmatic Reset
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

# Create and use trading graph
ta = TradingAgentsGraph()
final_state, decision = ta.propagate("AAPL", "2024-01-15")

# Reset for next analysis
ta.reset()
final_state, decision = ta.propagate("TSLA", "2024-01-15")
```

### Method 3: Manual Cleanup
```python
from tradingagents.agents.utils.memory import cleanup_persistent_chromadb

# Clean up any persistent ChromaDB files
cleanup_persistent_chromadb()
```

## Technical Benefits

1. **No More Application Restarts**: Users can analyze multiple stocks in a single session
2. **Faster Performance**: In-memory ChromaDB is significantly faster than persistent storage
3. **Robust Error Handling**: Graceful degradation and recovery from ChromaDB issues
4. **Windows Compatible**: Handles Windows file locking issues properly
5. **Memory Efficient**: Proper cleanup prevents memory leaks
6. **User Friendly**: Clear UI feedback and simple reset functionality

## Error Resolution

**If you still experience ChromaDB issues:**

1. Click the **🔄 Reset** button in the Streamlit UI
2. If problems persist, restart the Streamlit application
3. For development, run the test script: `python test_reset_functionality.py`
4. Check for any remaining ChromaDB files and delete them manually if needed

## Files Modified for ChromaDB Reset

- `tradingagents/agents/utils/memory.py` - Enhanced memory management
- `tradingagents/graph/trading_graph.py` - Added reset functionality
- `streamlit_app.py` - Added reset button and UI improvements
- `test_reset_functionality.py` - Added comprehensive testing

---

# Changelog

All notable changes to TradingAgents will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Version 0.2.3] - Multi-LLM Provider Support

### Added
- 🤖 **Multiple LLM Provider Selection**: Complete provider flexibility for both GUI and CLI
  - Support for 5 major providers: OpenAI, Anthropic, Google, Ollama, OpenRouter  
  - Dynamic model lists that update based on selected provider
  - Provider-specific configuration with backend URLs and requirements
  - Custom backend URL support for enterprise endpoints
  
- 🖥️ **Enhanced GUI Configuration**: Advanced provider management interface
  - Provider dropdown with descriptions and requirements
  - Real-time configuration display showing active provider and models
  - Provider-specific warnings and setup instructions
  - Smart agent reinitialization when provider changes
  
- ⚡ **Enhanced CLI Provider Selection**: Interactive provider configuration
  - Step-by-step provider and model selection workflow
  - Provider-specific model recommendations with descriptions
  - Custom backend URL configuration option
  - Comprehensive provider information display

### Changed
- 🔧 **Configuration Management**: Improved provider handling
  - Extended configuration system to include provider and backend URL
  - Enhanced analysis results to include provider information
  - Updated historical analysis parsing to handle provider data
  
- 💾 **Analysis Storage**: Enhanced result tracking
  - Analysis files now include LLM provider and backend URL information
  - Historical analysis viewer displays provider details
  - Backward compatibility with existing analysis files

### Technical Details
- Updated `streamlit_app.py` with comprehensive provider selection interface
- Enhanced `cli/utils.py` with provider configuration functions  
- Extended analysis result storage format to include provider metadata
- Added provider-specific model validation and descriptions
- Implemented smart reinitialization for provider changes

### Documentation
- 📖 **LLM_PROVIDER_GUIDE.md**: Comprehensive guide for provider selection and setup
- Updated configuration examples and best practices
- Provider-specific setup instructions and troubleshooting

## [Version 0.2.2] - Market Analyst Upgrade

### Added
- 🔍 **Market Analyst Enhancements**
  - Added new technical indicators: Bollinger Band Width (`bb_width`), Money Flow Index (`mfi`), Average Directional Index (`adx`).
  - Integrated **Volume Profile** analysis via new tool `get_volume_profile_report`, providing POC/VAH/VAL and top volume clusters.
  - Prompt now generates ≥600-word narrative, actionable insights section, indicator summary table, and volume profile summary.
- 🛠 **Toolkit & Dataflows**
  - Implemented `get_volume_profile` data-flow helper that calculates volume profile from Yahoo Finance data (online/offline).
  - Added `get_volume_profile_report` ToolNode in `Toolkit`, auto-detecting online mode.
  - Extended `best_ind_params` with `bb_width` & `mfi` descriptions.

### Changed
- ⚙️ **Trading Graph**
  - Registered `get_volume_profile_report` inside Market ToolNode so Market Analyst can access the new data source.
- 📝 **Market Analyst Prompt**
  - Expanded indicator whitelist, added ADX category, volume profile instructions, multi-time-frame guidance, and length requirement.

## [Version 0.2.1] - Analyst Prompt Enhancements

### Added
- 📰 **News Analyst Upgrade**
  - Rewritten system prompt to a structured, ≥600-word report with a single-line News Verdict and quantified `News Impact Score (NIS)`.
  - Added macro, sector, and company-specific subsections, Risk Radar, Actionable Insights, and a "Key News Summary" markdown table.

- 💼 **Fundamentals Analyst Upgrade**
  - Introduced `Fundamentals Score (FS)` (0-100) and one-line Fundamentals Verdict.
  - Prompt now covers valuation, growth, profitability, efficiency, liquidity/solvency, and insider/institutional activity in 8 numbered sections.
  - Generates ≥600-word narrative plus "Key Fundamentals Summary" markdown table and Actionable Insights.

### Changed
- 📝 **Documentation**
  - Updated analyst prompts to provide more consistent, research-grade outputs aligned with Market & Social analysts.

## [Version 0.2.0] - UI Release

### Added
- 📚 **Analysis History Feature**: Complete history management system in Streamlit GUI
  - Summary table showing all past analyses with sortable columns
  - Detailed viewer for any historical analysis with organized tabs
  - Download capability for individual analysis files
  - Automatic parsing and organization of saved analysis files
  
- 🖥️ **Enhanced GUI Interface**: Major improvements to Streamlit web interface
  - Two-tab main interface: "New Analysis" and "History"
  - Professional styling with color-coded indicators
  - Real-time progress tracking and agent status displays
  - Session state management for better user experience
  
- 🔄 **System Reset Functionality**: Comprehensive ChromaDB reset capabilities
  - Built-in reset button in GUI interface
  - Programmatic reset methods for development use
  - Automatic cleanup of persistent ChromaDB files
  - Windows-friendly file handling and cleanup
  
- 📊 **Rich Analysis Display**: Enhanced result presentation
  - Color-coded trading decisions (🟢 BUY, 🔴 SELL, 🟡 HOLD)
  - Organized tab structure for different analysis sections
  - Executive summary with key metrics
  - Bull vs Bear argument visualization
  
- 🎛️ **Advanced Configuration Options**: Expanded customization capabilities
  - Model selection for deep thinking and quick thinking LLMs
  - Adjustable debate rounds and risk analysis parameters
  - Flexible analyst team selection
  - Online/offline data source toggle

### Changed
- 🔧 **Memory Management**: Improved ChromaDB handling
  - Default to in-memory ChromaDB for better performance
  - Robust cleanup mechanisms for persistent storage
  - Enhanced error handling and recovery
  
- 📁 **File Organization**: Better structure for saved analyses
  - Automatic timestamping with consistent filename format
  - Organized storage in `analyses/` directory
  - Comprehensive analysis reports with all sections included
  
- 🎨 **UI/UX Improvements**: Enhanced user interface design
  - Modern, clean design with professional styling
  - Consistent color schemes and branding
  - Improved navigation and user flow
  - Better feedback and status indicators

### Fixed
- 🐛 **ChromaDB Connection Issues**: Resolved persistent connection problems
  - Fixed tenant connection errors between analyses
  - Eliminated need to restart application for new analyses
  - Proper cleanup of ChromaDB instances and file handles
  
- 💾 **Memory Leaks**: Improved resource management
  - Proper garbage collection of ChromaDB resources
  - Cleanup of temporary files and directories
  - Session state management in Streamlit
  
- 🔧 **Windows Compatibility**: Enhanced Windows support
  - Fixed file locking issues on Windows systems
  - Proper handling of file paths and permissions
  - Delayed cleanup for Windows file system constraints

### Technical Details
- Added `pandas` dependency for data table display
- Added `re` (regex) for analysis file parsing
- Enhanced error handling throughout the application
- Improved session state management in Streamlit
- Added comprehensive testing for reset functionality

### Documentation
- 📖 **Updated README.md**: Added GUI section with comprehensive feature overview
- 📝 **Enhanced GUI_Setup_Guide.md**: Updated with new History features and usage instructions
- 🔧 **CHROMADB_RESET_SOLUTION.md**: Complete documentation of reset functionality
- 📋 **CHANGELOG.md**: New changelog file for tracking updates

## [Version 0.1.0] - Initial Release

### Initial Release Features
- Multi-agent LLM trading framework
- CLI interface for running analyses
- Basic Streamlit GUI
- ChromaDB integration for memory management
- Comprehensive analysis pipeline with 5 agent teams
- Support for multiple LLM models
- Financial data integration with various APIs

**Happy Trading! 📈**

> **Disclaimer**: The GUI and system architecture is from TradingAgents.
