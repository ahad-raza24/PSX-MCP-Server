#!/usr/bin/env python3
"""
Demo script to show PSX MCP Server functionality
"""

import asyncio
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from psx_mcp.client import PSXClient

async def demo_psx_data():
    """Demonstrate PSX data fetching capabilities"""
    print("🚀 PSX MCP Server Demo")
    print("=" * 50)
    
    client = PSXClient()
    
    try:
        # Demo 1: Market Watch Data
        print("\n📊 Market Watch Data")
        print("-" * 30)
        market_data = await client.get_market_watch_data()
        print(f"Retrieved {len(market_data)} stocks")
        
        for stock in market_data[:3]:  # Show first 3 stocks
            print(f"  {stock['symbol']}: {stock['current_price']} ({stock['sector']})")
        
        # Demo 2: Intraday Data
        print("\n📈 Intraday Data (HBL)")
        print("-" * 30)
        intraday_data = await client.get_intraday_data("HBL")
        print(f"Retrieved {len(intraday_data)} intraday data points")
        
        if intraday_data:
            latest = intraday_data[0]
            print(f"  Latest: Price {latest['price']} at {latest['timestamp']}")
        
        # Demo 3: EOD Data
        print("\n📉 End-of-Day Data (HBL)")
        print("-" * 30)
        eod_data = await client.get_eod_data("HBL")
        print(f"Retrieved {len(eod_data)} EOD data points")
        
        if eod_data:
            latest = eod_data[0]
            print(f"  Latest: Close {latest['price']}, Open {latest['open_price']}, Volume {latest['volume']}")
        
        print("\n✅ All demos completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    
    finally:
        await client.close()

def show_mcp_tools():
    """Show available MCP tools"""
    print("\n🔧 Available MCP Tools")
    print("-" * 30)
    
    tools = [
        "get_market_watch() - Get all stocks data",
        "get_stock_intraday_data(symbol) - Get intraday data",
        "get_stock_eod_data(symbol) - Get historical EOD data",
        "search_stocks_by_sector(sector) - Filter by sector",
        "get_top_gainers(limit) - Top performing stocks",
        "get_top_losers(limit) - Worst performing stocks"
    ]
    
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool}")

def show_usage_instructions():
    """Show how to use the MCP server"""
    print("\n📖 Usage Instructions")
    print("-" * 30)
    print("1. Start the MCP server:")
    print("   python psx_mcp_server.py")
    print()
    print("2. Connect with Gemini CLI:")
    print("   gemini-cli --mcp-server psx_mcp_server.py")
    print()
    print("3. Example queries:")
    print("   - 'Get market data for HBL'")
    print("   - 'Show me top 10 gaining stocks'")
    print("   - 'Find all banking sector stocks'")
    print("   - 'Get intraday data for OGDC'")

async def main():
    """Run the demo"""
    show_mcp_tools()
    show_usage_instructions()
    await demo_psx_data()
    
    print("\n🎉 PSX MCP Server is ready for use!")

if __name__ == "__main__":
    asyncio.run(main())
