# Changelog

All notable changes to TradingAgents will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-06-25

### Added
- 🏃 **Real-Time Agent Status Tracking**: GUI now shows `running`, `pending`, and `completed` states per agent with animated pulse badges.
- 🎨 **Card-Style Status Grid**: Replaced legacy table with responsive two-column card layout; dark-theme friendly.
- 🏷️ **Active Agent Banner**: Banner under progress bar dynamically displays the agent currently executing.

### Changed
- 🔄 **Streamlit `run_analysis()`**: Switched to LangGraph `stream()` execution loop enabling frame-by-frame UI updates and more accurate progress bar.
- 📊 **Progress Calculation**: Progress bar now maps completion ratio linearly (30-90 %) and finalizes at 100 % after save.

### Fixed
- 🪟 **ChromaDB Temp Cleanup (Windows)**: Added robust `onerror` handler, retry with permission change, micro-delay, and downgraded noisy warnings to debug logs.

## [Unreleased]

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

- 📝 **Analyst Reports Rendering**: Fixed incomplete content display in the "Analyst Reports" tab of the History view
  - Refined regex patterns in `parse_analysis_file` to capture entire section text
  - Analyst reports now render fully with Markdown elements preserved

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

## [Previous Versions]

### Initial Release
- Multi-agent LLM trading framework
- CLI interface for running analyses
- Basic Streamlit GUI
- ChromaDB integration for memory management
- Comprehensive analysis pipeline with 5 agent teams
- Support for multiple LLM models
- Financial data integration with various APIs 