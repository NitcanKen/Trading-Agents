import streamlit as st
import os
import datetime
import json
from pathlib import Path
import time
from datetime import date, timedelta
import pandas as pd
import re

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.agents.utils.memory import cleanup_persistent_chromadb

# Page configuration
st.set_page_config(
    page_title="TradingAgents - Multi-Agent Financial Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5em;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #666;
        margin-bottom: 2em;
    }
    
    .agent-status {
        padding: 0.5em;
        border-radius: 5px;
        margin: 0.2em 0;
        font-weight: bold;
    }
    
    .status-completed {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .status-running {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .status-pending {
        background-color: #f8f9fa;
        color: #6c757d;
        border: 1px solid #dee2e6;
    }
    
    .team-section {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1em;
        margin: 0.5em 0;
        background-color: #f8f9fa;
    }
    
    .analysis-output {
        background-color: #f8f9fa;
        border-left: 4px solid #007bff;
        padding: 1em;
        margin: 1em 0;
        border-radius: 4px;
        color: #333333 !important;
    }
    
    .analysis-output p, .analysis-output div, .analysis-output span {
        color: #333333 !important;
    }
    
    .stExpander > div:first-child {
        background-color: #e9ecef;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'trading_graph' not in st.session_state:
    st.session_state.trading_graph = None

def reset_system():
    """Reset ChromaDB and clear all system state"""
    try:
        # Reset the trading graph if it exists
        if st.session_state.trading_graph is not None:
            st.session_state.trading_graph.reset()
        
        # Clear the trading graph instance
        st.session_state.trading_graph = None
        
        # Clean up persistent ChromaDB files
        cleanup_persistent_chromadb()
        
        # Clear analysis results
        st.session_state.analysis_complete = False
        st.session_state.analysis_results = None
        
        if hasattr(st.session_state, 'saved_file'):
            delattr(st.session_state, 'saved_file')
        
        return True, "System reset successfully! ChromaDB cleaned up. You can now analyze a new stock."
    except Exception as e:
        # Even if reset fails, try to clean up everything
        st.session_state.trading_graph = None
        st.session_state.analysis_complete = False
        st.session_state.analysis_results = None
        
        try:
            cleanup_persistent_chromadb()
        except:
            pass
            
        return True, f"System reset completed with cleanup. Any ChromaDB issues should now be resolved."

def display_header():
    """Display the main header and branding"""
    st.markdown('<div class="main-header">🚀 TradingAgents</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Multi-Agent LLM Financial Trading Framework</div>', unsafe_allow_html=True)
    
    # Workflow description
    st.markdown("""
    **Workflow Steps:**
    1. **Analyst Team** → II. **Research Team** → III. **Trader** → IV. **Risk Management** → V. **Portfolio Management**
    """)

def create_config_sidebar():
    """Create the configuration sidebar"""
    st.sidebar.title("⚙️ Configuration")
    
    # Model selection
    available_models = [
        "o4-mini", "o3", "o3-mini", "gpt-4.1", "gpt-4.1-mini", 
        "gpt-4.1-nano", "gpt-4o", "gpt-4o-mini"
    ]
    
    deep_think_model = st.sidebar.selectbox(
        "Deep Thinking Model:",
        available_models,
        index=available_models.index("gpt-4.1"),
        help="Model used for complex analysis and decision making"
    )
    
    quick_think_model = st.sidebar.selectbox(
        "Quick Thinking Model:",
        available_models,
        index=available_models.index("gpt-4o-mini"),
        help="Model used for rapid analysis and tool calls"
    )
    
    # Analysis parameters
    max_debate_rounds = st.sidebar.slider(
        "Max Debate Rounds:",
        min_value=1,
        max_value=5,
        value=1,
        help="Number of debate rounds between bull and bear researchers"
    )
    
    max_risk_rounds = st.sidebar.slider(
        "Max Risk Discussion Rounds:",
        min_value=1,
        max_value=5,
        value=1,
        help="Number of discussion rounds between risk analysts"
    )
    
    online_tools = st.sidebar.checkbox(
        "Enable Online Tools",
        value=True,
        help="Use real-time data sources for analysis"
    )
    
    # Analyst selection
    st.sidebar.subheader("📊 Select Analysts")
    analyst_options = {
        "market": st.sidebar.checkbox("Market Analyst", value=True),
        "social": st.sidebar.checkbox("Social Media Analyst", value=True),
        "news": st.sidebar.checkbox("News Analyst", value=True),
        "fundamentals": st.sidebar.checkbox("Fundamentals Analyst", value=True)
    }
    
    selected_analysts = [k for k, v in analyst_options.items() if v]
    
    return {
        "deep_think_llm": deep_think_model,
        "quick_think_llm": quick_think_model,
        "max_debate_rounds": max_debate_rounds,
        "max_risk_discuss_rounds": max_risk_rounds,
        "online_tools": online_tools,
        "selected_analysts": selected_analysts
    }

def display_agent_status():
    """Display the status of all agents"""
    st.subheader("🔄 Agent Status")
    
    # Define agent teams and their members
    teams = {
        "Analyst Team": [
            "Market Analyst",
            "Social Analyst", 
            "News Analyst",
            "Fundamentals Analyst"
        ],
        "Research Team": [
            "Bull Researcher",
            "Bear Researcher",
            "Research Manager"
        ],
        "Trading Team": [
            "Trader"
        ],
        "Risk Management": [
            "Risky Analyst",
            "Neutral Analyst",
            "Safe Analyst"
        ],
        "Portfolio Management": [
            "Portfolio Manager"
        ]
    }
    
    # Create columns for teams
    cols = st.columns(len(teams))
    
    for idx, (team_name, agents) in enumerate(teams.items()):
        with cols[idx]:
            st.markdown(f"**{team_name}**")
            for agent in agents:
                status = st.session_state.agent_status.get(agent, "pending")
                status_class = f"status-{status}"
                status_text = status.replace("_", " ").title()
                
                if status == "completed":
                    emoji = "✅"
                elif status == "running":
                    emoji = "🔄"
                else:
                    emoji = "⏳"
                
                st.markdown(
                    f'<div class="agent-status {status_class}">{emoji} {agent}: {status_text}</div>',
                    unsafe_allow_html=True
                )

def save_analysis_results(ticker, results, config):
    """Save analysis results to the analyses folder"""
    analyses_dir = Path("analyses")
    analyses_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ticker}_{timestamp}_analysis.txt"
    filepath = analyses_dir / filename
    
    # Format the results for saving
    content = f"""
=== TradingAgents Analysis Report ===
Company: {ticker}
Analysis Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Models Used: Deep={config['deep_think_llm']}, Quick={config['quick_think_llm']}
Debate Rounds: {config['max_debate_rounds']}, Risk Rounds: {config['max_risk_discuss_rounds']}
Online Tools: {config['online_tools']}

=== ANALYST TEAM REPORTS ===

--- Market Analysis ---
{results.get('market_report', 'N/A')}

--- Social Sentiment ---
{results.get('sentiment_report', 'N/A')}

--- News Analysis ---
{results.get('news_report', 'N/A')}

--- Fundamentals Analysis ---
{results.get('fundamentals_report', 'N/A')}

=== RESEARCH TEAM DECISION ===
{results.get('investment_plan', 'N/A')}

=== TRADING TEAM PLAN ===
{results.get('trader_investment_plan', 'N/A')}

=== PORTFOLIO MANAGEMENT DECISION ===
{results.get('final_trade_decision', 'N/A')}

=== INVESTMENT DEBATE DETAILS ===
Bull Arguments:
{results.get('investment_debate_state', {}).get('bull_history', 'N/A')}

Bear Arguments:
{results.get('investment_debate_state', {}).get('bear_history', 'N/A')}

Research Manager Decision:
{results.get('investment_debate_state', {}).get('judge_decision', 'N/A')}

=== RISK ANALYSIS DETAILS ===
Risky Analysis:
{results.get('risk_debate_state', {}).get('risky_history', 'N/A')}

Safe Analysis:
{results.get('risk_debate_state', {}).get('safe_history', 'N/A')}

Neutral Analysis:
{results.get('risk_debate_state', {}).get('neutral_history', 'N/A')}

Risk Manager Decision:
{results.get('risk_debate_state', {}).get('judge_decision', 'N/A')}
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(filepath)

def run_analysis(ticker, trade_date, config):
    """Run the analysis synchronously with progress updates"""
    try:
        # Create config for TradingAgentsGraph
        ta_config = DEFAULT_CONFIG.copy()
        ta_config.update({
            "deep_think_llm": config["deep_think_llm"],
            "quick_think_llm": config["quick_think_llm"],
            "max_debate_rounds": config["max_debate_rounds"],
            "max_risk_discuss_rounds": config["max_risk_discuss_rounds"],
            "online_tools": config["online_tools"]
        })
        
        # Create progress components
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize or reuse TradingAgentsGraph
        if st.session_state.trading_graph is None:
            status_text.text("🔧 Initializing agents...")
            progress_bar.progress(10)
            
            st.session_state.trading_graph = TradingAgentsGraph(
                selected_analysts=config["selected_analysts"],
                debug=False,
                config=ta_config
            )
        else:
            status_text.text("🔧 Using existing agents...")
            progress_bar.progress(10)
        
        ta = st.session_state.trading_graph
        
        # Run analysis
        status_text.text("🚀 Running multi-agent analysis...")
        progress_bar.progress(30)
        
        final_state, decision = ta.propagate(ticker, trade_date)
        
        progress_bar.progress(90)
        status_text.text("💾 Saving results...")
        
        # Save results to file
        saved_file = save_analysis_results(ticker, final_state, config)
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis Complete!")
        
        # Store results in session state
        st.session_state.analysis_results = final_state
        st.session_state.analysis_complete = True
        st.session_state.saved_file = saved_file
        
        return True, None
        
    except Exception as e:
        return False, str(e)

def display_analysis_results():
    """Display the analysis results"""
    if not st.session_state.analysis_complete or not st.session_state.analysis_results:
        return
    
    results = st.session_state.analysis_results
    
    st.success("🎉 Analysis Complete!")
    
    if hasattr(st.session_state, 'saved_file'):
        st.info(f"📁 Results saved to: `{st.session_state.saved_file}`")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Summary", "🔍 Analyst Reports", "💭 Research Debate", 
        "📈 Trading Plan", "⚖️ Risk Analysis"
    ])
    
    with tab1:
        st.subheader("Executive Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Company:**")
            st.write(results.get('company_of_interest', 'N/A'))
            
            st.markdown("**Analysis Date:**")
            st.write(results.get('trade_date', 'N/A'))
        
        with col2:
            st.markdown("**Final Decision:**")
            decision_text = results.get('final_trade_decision', 'N/A')
            if 'BUY' in decision_text.upper():
                st.success("🟢 BUY")
            elif 'SELL' in decision_text.upper():
                st.error("🔴 SELL")
            elif 'HOLD' in decision_text.upper():
                st.warning("🟡 HOLD")
            else:
                st.info("📋 See Full Decision")
        
        st.markdown("**Portfolio Management Decision:**")
        st.markdown(f'<div class="analysis-output" style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 1em; margin: 1em 0; border-radius: 4px; color: #333333;">{results.get("final_trade_decision", "N/A")}</div>', 
                   unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Analyst Team Reports")
        
        if results.get('market_report'):
            with st.expander("📈 Market Analysis", expanded=True):
                st.markdown(results['market_report'])
        
        if results.get('sentiment_report'):
            with st.expander("💬 Social Sentiment Analysis"):
                st.markdown(results['sentiment_report'])
        
        if results.get('news_report'):
            with st.expander("📰 News Analysis"):
                st.markdown(results['news_report'])
        
        if results.get('fundamentals_report'):
            with st.expander("📊 Fundamentals Analysis"):
                st.markdown(results['fundamentals_report'])
    
    with tab3:
        st.subheader("Research Team Debate")
        
        debate_state = results.get('investment_debate_state', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🐂 Bull Arguments:**")
            bull_history = debate_state.get('bull_history', 'No bull arguments recorded')
            st.markdown(f'<div class="analysis-output" style="background-color: #f8f9fa; border-left: 4px solid #28a745; padding: 1em; margin: 1em 0; border-radius: 4px; color: #333333;">{bull_history}</div>', 
                       unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🐻 Bear Arguments:**")
            bear_history = debate_state.get('bear_history', 'No bear arguments recorded')
            st.markdown(f'<div class="analysis-output" style="background-color: #f8f9fa; border-left: 4px solid #dc3545; padding: 1em; margin: 1em 0; border-radius: 4px; color: #333333;">{bear_history}</div>', 
                       unsafe_allow_html=True)
        
        st.markdown("**🎯 Research Manager Decision:**")
        judge_decision = debate_state.get('judge_decision', results.get('investment_plan', 'N/A'))
        st.markdown(f'<div class="analysis-output" style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 1em; margin: 1em 0; border-radius: 4px; color: #333333;">{judge_decision}</div>', 
                   unsafe_allow_html=True)
    
    with tab4:
        st.subheader("Trading Team Plan")
        trader_plan = results.get('trader_investment_plan', 'N/A')
        st.markdown(f'<div class="analysis-output" style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 1em; margin: 1em 0; border-radius: 4px; color: #333333;">{trader_plan}</div>', 
                   unsafe_allow_html=True)
    
    with tab5:
        st.subheader("Risk Management Analysis")
        
        risk_state = results.get('risk_debate_state', {})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🚨 Risky Analysis:**")
            risky_history = risk_state.get('risky_history', 'No risky analysis recorded')
            st.markdown(f'<div class="analysis-output" style="background-color: #f8f9fa; border-left: 4px solid #dc3545; padding: 1em; margin: 1em 0; border-radius: 4px; color: #333333;">{risky_history}</div>', 
                       unsafe_allow_html=True)
        
        with col2:
            st.markdown("**⚖️ Neutral Analysis:**")
            neutral_history = risk_state.get('neutral_history', 'No neutral analysis recorded')
            st.markdown(f'<div class="analysis-output" style="background-color: #f8f9fa; border-left: 4px solid #6c757d; padding: 1em; margin: 1em 0; border-radius: 4px; color: #333333;">{neutral_history}</div>', 
                       unsafe_allow_html=True)
        
        with col3:
            st.markdown("**🛡️ Safe Analysis:**")
            safe_history = risk_state.get('safe_history', 'No safe analysis recorded')
            st.markdown(f'<div class="analysis-output" style="background-color: #f8f9fa; border-left: 4px solid #28a745; padding: 1em; margin: 1em 0; border-radius: 4px; color: #333333;">{safe_history}</div>', 
                       unsafe_allow_html=True)
        
        st.markdown("**🏛️ Risk Manager Final Decision:**")
        risk_judge_decision = risk_state.get('judge_decision', 'N/A')
        st.markdown(f'<div class="analysis-output" style="background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 1em; margin: 1em 0; border-radius: 4px; color: #333333;">{risk_judge_decision}</div>', 
                   unsafe_allow_html=True)

def load_analysis_history():
    """Load all analysis files from the analyses folder"""
    analyses_dir = Path("analyses")
    if not analyses_dir.exists():
        return []
    
    history = []
    for file_path in analyses_dir.glob("*_analysis.txt"):
        try:
            # Parse filename for ticker and timestamp
            filename = file_path.stem
            # Format: TICKER_YYYYMMDD_HHMMSS_analysis
            parts = filename.split("_")
            if len(parts) >= 3:
                ticker = parts[0]
                date_str = parts[1]
                time_str = parts[2]
                
                # Parse date and time
                analysis_datetime = datetime.datetime.strptime(f"{date_str}_{time_str}", "%Y%m%d_%H%M%S")
                
                # Read file content to extract key information
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract decision from content
                decision = "Unknown"
                if "=== PORTFOLIO MANAGEMENT DECISION ===" in content:
                    lines = content.split("\n")
                    for i, line in enumerate(lines):
                        if "=== PORTFOLIO MANAGEMENT DECISION ===" in line:
                            # Look for the decision in the next few lines
                            for j in range(i+1, min(i+10, len(lines))):
                                if lines[j].strip() and not lines[j].startswith("==="):
                                    decision_text = lines[j].strip()
                                    if 'BUY' in decision_text.upper():
                                        decision = "🟢 BUY"
                                    elif 'SELL' in decision_text.upper():
                                        decision = "🔴 SELL"
                                    elif 'HOLD' in decision_text.upper():
                                        decision = "🟡 HOLD"
                                    else:
                                        decision = "📋 Other"
                                    break
                            break
                
                history.append({
                    'ticker': ticker,
                    'datetime': analysis_datetime,
                    'decision': decision,
                    'filepath': str(file_path),
                    'filename': file_path.name
                })
        except Exception as e:
            # Skip files that can't be parsed
            continue
    
    # Sort by datetime, most recent first
    history.sort(key=lambda x: x['datetime'], reverse=True)
    return history

def parse_analysis_file(filepath):
    """Parse an analysis file and extract structured data"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract sections using regex
        sections = {}
        
        # Extract header information
        header_match = re.search(r'Company: (.+?)\nAnalysis Date: (.+?)\n', content)
        if header_match:
            sections['company'] = header_match.group(1).strip()
            sections['analysis_date'] = header_match.group(2).strip()
        
        # Extract models and config
        models_match = re.search(r'Models Used: (.+?)\n', content)
        if models_match:
            sections['models'] = models_match.group(1).strip()
        
        # Extract main sections
        section_patterns = {
            'market_analysis': r'--- Market Analysis ---\n(.*?)(?=---|===|$)',
            'social_sentiment': r'--- Social Sentiment ---\n(.*?)(?=---|===|$)',
            'news_analysis': r'--- News Analysis ---\n(.*?)(?=---|===|$)',
            'fundamentals_analysis': r'--- Fundamentals Analysis ---\n(.*?)(?=---|===|$)',
            'research_decision': r'=== RESEARCH TEAM DECISION ===\n(.*?)(?====|$)',
            'trading_plan': r'=== TRADING TEAM PLAN ===\n(.*?)(?====|$)',
            'final_decision': r'=== PORTFOLIO MANAGEMENT DECISION ===\n(.*?)(?====|$)',
            'bull_arguments': r'Bull Arguments:\n(.*?)(?=Bear Arguments:|Research Manager|===|$)',
            'bear_arguments': r'Bear Arguments:\n(.*?)(?=Research Manager|===|$)',
            'research_manager_decision': r'Research Manager Decision:\n(.*?)(?====|$)',
            'risk_analysis': r'=== RISK ANALYSIS DETAILS ===\n(.*?)(?=$)'
        }
        
        for key, pattern in section_patterns.items():
            match = re.search(pattern, content, re.DOTALL)
            if match:
                sections[key] = match.group(1).strip()
            else:
                sections[key] = 'N/A'
        
        return sections
    except Exception as e:
        return {'error': f"Failed to parse file: {str(e)}"}

def display_history_section():
    """Display the history section with all past analyses"""
    
    # Load history
    history = load_analysis_history()
    
    if not history:
        st.info("📭 No historical analyses found. Run your first analysis to see it here!")
        return
    
    # Create a summary table
    st.markdown("### 📊 Analysis Summary")
    
    # Convert to DataFrame for display
    df_data = []
    for item in history:
        df_data.append({
            'Ticker': item['ticker'],
            'Date': item['datetime'].strftime('%Y-%m-%d'),
            'Time': item['datetime'].strftime('%H:%M:%S'),
            'Decision': item['decision'],
            'File': item['filename']
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True)
    
    # Detailed view section
    st.markdown("### 🔍 Detailed Analysis View")
    
    # Create a selectbox for choosing analysis
    if history:
        options = [f"{item['ticker']} - {item['datetime'].strftime('%Y-%m-%d %H:%M:%S')} - {item['decision']}" 
                  for item in history]
        
        selected_idx = st.selectbox(
            "Select an analysis to view details:",
            range(len(options)),
            format_func=lambda x: options[x]
        )
        
        if selected_idx is not None:
            selected_analysis = history[selected_idx]
            
            # Parse and display the selected analysis
            parsed_data = parse_analysis_file(selected_analysis['filepath'])
            
            if 'error' in parsed_data:
                st.error(f"❌ {parsed_data['error']}")
                return
            
            # Display header info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Company", parsed_data.get('company', 'N/A'))
            with col2:
                st.metric("Analysis Date", parsed_data.get('analysis_date', 'N/A'))
            with col3:
                st.metric("Models Used", parsed_data.get('models', 'N/A'))
            
            # Create tabs for detailed sections
            detail_tabs = st.tabs([
                "📊 Summary", "🔍 Analyst Reports", "💭 Research Debate", 
                "📈 Trading Plan", "⚖️ Risk Analysis", "📄 Raw Data"
            ])
            
            with detail_tabs[0]:  # Summary
                st.markdown("**Final Decision:**")
                final_decision = parsed_data.get('final_decision', 'N/A')
                st.markdown(f'<div class="analysis-output">{final_decision}</div>', 
                           unsafe_allow_html=True)
            
            with detail_tabs[1]:  # Analyst Reports
                if parsed_data.get('market_analysis', 'N/A') != 'N/A':
                    with st.expander("📈 Market Analysis", expanded=True):
                        st.markdown(parsed_data['market_analysis'])
                
                if parsed_data.get('social_sentiment', 'N/A') != 'N/A':
                    with st.expander("💬 Social Sentiment Analysis"):
                        st.markdown(parsed_data['social_sentiment'])
                
                if parsed_data.get('news_analysis', 'N/A') != 'N/A':
                    with st.expander("📰 News Analysis"):
                        st.markdown(parsed_data['news_analysis'])
                
                if parsed_data.get('fundamentals_analysis', 'N/A') != 'N/A':
                    with st.expander("📊 Fundamentals Analysis"):
                        st.markdown(parsed_data['fundamentals_analysis'])
            
            with detail_tabs[2]:  # Research Debate
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🐂 Bull Arguments:**")
                    bull_args = parsed_data.get('bull_arguments', 'N/A')
                    st.markdown(f'<div class="analysis-output" style="border-left: 4px solid #28a745;">{bull_args}</div>', 
                               unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**🐻 Bear Arguments:**")
                    bear_args = parsed_data.get('bear_arguments', 'N/A')
                    st.markdown(f'<div class="analysis-output" style="border-left: 4px solid #dc3545;">{bear_args}</div>', 
                               unsafe_allow_html=True)
                
                st.markdown("**🎯 Research Manager Decision:**")
                research_decision = parsed_data.get('research_manager_decision', parsed_data.get('research_decision', 'N/A'))
                st.markdown(f'<div class="analysis-output">{research_decision}</div>', 
                           unsafe_allow_html=True)
            
            with detail_tabs[3]:  # Trading Plan
                trading_plan = parsed_data.get('trading_plan', 'N/A')
                st.markdown(f'<div class="analysis-output">{trading_plan}</div>', 
                           unsafe_allow_html=True)
            
            with detail_tabs[4]:  # Risk Analysis
                risk_analysis = parsed_data.get('risk_analysis', 'N/A')
                st.markdown(f'<div class="analysis-output">{risk_analysis}</div>', 
                           unsafe_allow_html=True)
            
            with detail_tabs[5]:  # Raw Data
                st.markdown("**📄 Full Analysis File:**")
                with open(selected_analysis['filepath'], 'r', encoding='utf-8') as f:
                    full_content = f.read()
                st.text_area("Raw analysis data:", value=full_content, height=400)
                
                # Download button
                st.download_button(
                    label="💾 Download Analysis File",
                    data=full_content,
                    file_name=selected_analysis['filename'],
                    mime="text/plain"
                )

def main():
    """Main application function"""
    display_header()
    
    # Configuration sidebar
    config = create_config_sidebar()
    
    # Create main tabs
    main_tab1, main_tab2 = st.tabs(["🚀 New Analysis", "📚 History"])
    
    with main_tab1:
        # Main input section
        st.subheader("📈 Stock Analysis Input")
        
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            ticker = st.text_input(
                "Ticker Symbol:",
                value="SPY",
                placeholder="Enter stock ticker (e.g., AAPL, TSLA, SPY)",
                help="Enter the stock ticker symbol you want to analyze"
            ).upper()
        
        with col2:
            trade_date = st.date_input(
                "Analysis Date:",
                value=date.today(),
                help="Date for the analysis (usually today or a recent trading day)"
            )
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
            run_button = st.button(
                "🚀 Run Analysis",
                type="primary",
                help="Start the multi-agent analysis"
            )
        
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
            reset_button = st.button(
                "🔄 Reset",
                type="secondary",
                help="Reset ChromaDB and clear system state for analyzing new stocks"
            )
        
        # Validation
        if not ticker:
            st.warning("⚠️ Please enter a ticker symbol")
            return
        
        if not config["selected_analysts"]:
            st.warning("⚠️ Please select at least one analyst from the sidebar")
            return
        
        # Reset button logic
        if reset_button:
            with st.spinner("🔄 Resetting system..."):
                success, message = reset_system()
            if success:
                st.success(f"✅ {message}")
                # Force a rerun to refresh the UI
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(f"❌ Reset failed: {message}")
        
        # Run analysis button logic
        if run_button:
            # Clear only analysis results (keep trading graph instance for reuse)
            st.session_state.analysis_complete = False
            st.session_state.analysis_results = None
            
            # Run analysis with progress updates
            with st.spinner("🔄 Starting analysis..."):
                success, error = run_analysis(ticker, str(trade_date), config)
            
            if not success:
                st.error(f"❌ Analysis failed: {error}")
                st.info("💡 Try using the Reset button if you're experiencing ChromaDB connection issues.")
            else:
                st.success("🎉 Analysis completed successfully!")
                # Force a rerun to show results
                time.sleep(0.5)
                st.rerun()
        
        # Display system status
        if st.session_state.analysis_complete:
            st.subheader("🔄 Analysis Status")
            st.success("✅ All agents completed successfully!")
        elif st.session_state.trading_graph is not None:
            st.subheader("🔄 System Status")
            st.info("🤖 Agents initialized and ready for analysis")
        else:
            st.subheader("🔄 System Status")
            st.warning("⚡ System ready - agents will be initialized on first analysis")
        
        # Display results
        if st.session_state.analysis_complete:
            st.markdown("---")
            display_analysis_results()
    
    with main_tab2:
        # History section
        display_history_section()
    

if __name__ == "__main__":
    main() 