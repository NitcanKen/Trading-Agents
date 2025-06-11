# 🚀 TradingAgents GUI Setup Guide

This guide will help you set up and run the beautiful Streamlit GUI for TradingAgents.

## 📋 Prerequisites

You mentioned you have already:
- ✅ Cloned the repository to `C:\Users\asdzx\Documents\Python Project\TradingAgents`
- ✅ Created a virtual environment
- ✅ Set up all API keys
- ✅ Python 3.13 installed

## 🛠️ Setup Steps

### 1. Activate Your Virtual Environment

Open PowerShell in your project directory and activate your virtual environment:

```powershell
# Navigate to your project directory
cd "C:\Users\asdzx\Documents\Python Project\TradingAgents"

# Activate your virtual environment (adjust path if needed)
.\venv\Scripts\Activate.ps1
```

### 2. Install Streamlit

Install the required Streamlit dependency:

```powershell
pip install streamlit
```

Or install all requirements (which now includes Streamlit):

```powershell
pip install -r requirements.txt
```

### 3. Run the GUI

You have two options:

#### Option A: Use the Batch File (Easiest)
Simply double-click `run_gui.bat` in the project folder.

#### Option B: Run Manually
```powershell
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

## 🔧 Troubleshooting

### Port Already in Use
If port 8501 is busy, run with a different port:
```powershell
streamlit run streamlit_app.py --server.port 8502
```

### Import Errors
Make sure your virtual environment is activated and all dependencies are installed:
```powershell
pip install -r requirements.txt
```

### API Key Issues
Ensure all your API keys are properly set in your environment variables:
- `OPENAI_API_KEY`
- Any other API keys required by your data sources

### Memory Issues
If you encounter memory issues with large analyses:
- Try reducing the number of selected analysts
- Reduce debate/risk discussion rounds
- Use lighter models (like gpt-4o-mini)

## 📁 File Structure

After setup, your project will have these key files:
```
TradingAgents/
├── streamlit_app.py          # Main GUI application
├── run_gui.bat              # Easy launcher for Windows
├── GUI_Setup_Guide.md       # This guide
├── analyses/                # Auto-generated analysis results
├── requirements.txt         # Updated with streamlit
└── ... (existing files)
```

## 🚀 Advanced Usage

### Custom Model Configuration
You can easily switch between your available models:
- **Deep Thinking Models**: For complex analysis (gpt-4.1, o3, o4-mini)
- **Quick Thinking Models**: For rapid tool calls (gpt-4o-mini, gpt-4.1-nano)

### Analysis Customization
- **Minimal Analysis**: Select only Market Analyst, 1 debate round
- **Comprehensive Analysis**: Select all analysts, 3-5 debate rounds
- **Risk-Focused Analysis**: Include all risk analysts, increase risk rounds

### History Management
- **View Trends**: Compare decisions across time periods
- **Export Data**: Download specific analyses for external tools
- **Portfolio Review**: Track your analysis history for portfolio insights
- **Research**: Use historical data for backtesting strategies

### Batch Processing
For multiple analyses, you can:
1. Run one analysis and save results
2. Use the History tab to review
3. Switch back to New Analysis tab
4. Change ticker symbol and run another analysis
5. All results are automatically timestamped and organized

## 📂 File Organization

The GUI automatically organizes your files:
```
TradingAgents/
├── streamlit_app.py          # Main GUI application
├── run_gui.bat              # Easy launcher for Windows
├── GUI_Setup_Guide.md       # This guide
├── analyses/                # Auto-generated analysis results
│   ├── AAPL_20240115_143022_analysis.txt
│   ├── TSLA_20240115_151045_analysis.txt
│   └── SPY_20240116_092314_analysis.txt
├── requirements.txt         # Updated with all dependencies
└── ... (existing files)
```

## 🎉 Enjoy Your New GUI!

You now have a professional, easy-to-use interface for your TradingAgents system! The GUI provides all the functionality of the CLI but with a much more user-friendly experience, plus powerful history management capabilities.

**Pro Tips:**
- Save your favorite configuration settings by noting them down
- Use meaningful ticker symbols and check the analysis dates
- Review all tabs for comprehensive insights
- Use the History tab to track patterns in your trading decisions
- Download analysis files for external tools or sharing
- Use the Reset button if you encounter ChromaDB issues
- Check the `analyses` folder for all saved reports

**New History Features:**
- 📊 **Quick Overview**: See all your analyses at a glance in the summary table
- 🔍 **Deep Dive**: Select any analysis for detailed review with organized tabs
- 📥 **Export**: Download any analysis file for external use
- 📈 **Track Performance**: Monitor your trading decision patterns over time
- 🔄 **Easy Navigation**: Switch seamlessly between new analysis and history review

Happy Trading! 📈 