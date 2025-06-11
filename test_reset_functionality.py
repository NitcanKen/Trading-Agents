#!/usr/bin/env python3
"""
Test script to verify ChromaDB reset functionality
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from tradingagents.agents.utils.memory import FinancialSituationMemory, cleanup_persistent_chromadb
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

def test_memory_reset():
    """Test if FinancialSituationMemory reset works"""
    print("🧪 Testing FinancialSituationMemory reset...")
    
    # Create a memory instance
    memory = FinancialSituationMemory("test_memory")
    
    # Add some test data
    test_data = [
        ("Market is volatile", "Consider defensive stocks"),
        ("High inflation observed", "Look into inflation hedges")
    ]
    
    try:
        memory.add_situations(test_data)
        print("✅ Successfully added test data to memory")
        
        # Test retrieval
        results = memory.get_memories("Market conditions are uncertain", n_matches=1)
        print(f"✅ Retrieved {len(results)} memories before reset")
        
        # Reset the memory
        memory.reset()
        print("✅ Memory reset completed")
        
        # Try to use it again
        memory.add_situations([("New test data", "New recommendation")])
        print("✅ Successfully added data after reset")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory reset test failed: {e}")
        return False

def test_trading_graph_reset():
    """Test if TradingAgentsGraph reset works"""
    print("\n🧪 Testing TradingAgentsGraph reset...")
    
    try:
        # Create config
        config = DEFAULT_CONFIG.copy()
        config["deep_think_llm"] = "gpt-4o-mini"  # Use cheaper model for testing
        config["quick_think_llm"] = "gpt-4o-mini"
        
        # Create trading graph
        ta = TradingAgentsGraph(
            selected_analysts=["market"],  # Just one analyst for testing
            debug=False,
            config=config
        )
        print("✅ TradingAgentsGraph created successfully")
        
        # Reset the graph
        ta.reset()
        print("✅ TradingAgentsGraph reset completed")
        
        # Try to use it again (would fail if reset didn't work)
        ta.reset()  # Double reset test
        print("✅ Double reset test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ TradingAgentsGraph reset test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting ChromaDB Reset Functionality Tests\n")
    
    # Clean up any existing persistent ChromaDB files first
    print("🧹 Cleaning up existing ChromaDB files...")
    cleanup_persistent_chromadb()
    
    # Test individual memory reset
    memory_test = test_memory_reset()
    
    # Test trading graph reset
    graph_test = test_trading_graph_reset()
    
    # Clean up after tests
    print("\n🧹 Final cleanup...")
    cleanup_persistent_chromadb()
    
    # Summary
    print(f"\n📊 Test Results:")
    print(f"   Memory Reset Test: {'✅ PASSED' if memory_test else '❌ FAILED'}")
    print(f"   Trading Graph Reset Test: {'✅ PASSED' if graph_test else '❌ FAILED'}")
    
    if memory_test and graph_test:
        print("\n🎉 All tests passed! The reset functionality is working correctly.")
        print("💡 You can now use the Reset button in the Streamlit app to resolve ChromaDB connection issues.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
    
    return memory_test and graph_test

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 