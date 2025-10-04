#!/usr/bin/env python3
"""
Simple test to verify PSX MCP Server functionality
"""

import asyncio
import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from psx_mcp.client import PSXClient

async def test_psx_client():
    """Test PSXClient functionality"""
    print("Testing PSX Client...")
    
    client = PSXClient()
    
    try:
        # Test market watch data
        print("Testing market watch data...")
        market_data = await client.get_market_watch_data()
        print(f"✅ Market watch data retrieved: {len(market_data)} stocks")
        
        if market_data:
            print(f"Sample stock: {market_data[0]}")
        
        # Test intraday data for HBL
        print("\nTesting intraday data for HBL...")
        intraday_data = await client.get_intraday_data("HBL")
        print(f"✅ Intraday data retrieved: {len(intraday_data)} data points")
        
        if intraday_data:
            print(f"Sample intraday point: {intraday_data[0]}")
        
        # Test EOD data for HBL
        print("\nTesting EOD data for HBL...")
        eod_data = await client.get_eod_data("HBL")
        print(f"✅ EOD data retrieved: {len(eod_data)} data points")
        
        if eod_data:
            print(f"Sample EOD point: {eod_data[0]}")
        
        print("\n🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    finally:
        await client.close()

def test_data_models():
    """Test Pydantic data models"""
    print("\nTesting data models...")
    
    from psx_mcp.models import StockData, TimeSeriesData
    
    # Test StockData
    stock = StockData(
        symbol="HBL",
        sector="Banking",
        listed_in="Main Board",
        ldcp=100.0,
        open_price=101.0,
        high_price=102.0,
        low_price=99.0,
        current_price=101.5,
        change=1.5,
        change_percent=1.5,
        volume=1000000
    )
    
    print(f"✅ StockData model: {stock.symbol} - {stock.current_price}")
    
    # Test TimeSeriesData
    time_point = TimeSeriesData(
        timestamp=1759491298,
        price=300.87,
        volume=1000
    )
    
    print(f"✅ TimeSeriesData model: {time_point.timestamp} - {time_point.price}")
    
    print("🎉 Data model tests passed!")

def test_mcp_server_import():
    """Test that MCP server can be imported"""
    print("\nTesting MCP server import...")
    
    try:
        from psx_mcp.server import mcp
        print(f"✅ MCP server imported: {mcp.name}")
        print("🎉 MCP server import test passed!")
    except Exception as e:
        print(f"❌ MCP server import failed: {e}")

async def main():
    """Run all tests"""
    print("🚀 Starting PSX MCP Server Tests\n")
    
    test_data_models()
    test_mcp_server_import()
    await test_psx_client()
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
