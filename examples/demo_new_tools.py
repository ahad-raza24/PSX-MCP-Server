#!/usr/bin/env python3
"""
Demo script to test all the new advanced PSX MCP Server tools
"""

import asyncio
import json
import sys
import os
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from psx_mcp.client import PSXClient

async def demo_new_tools():
    """Demonstrate all the new advanced tools"""
    print("🚀 Advanced PSX MCP Server Tools Demo")
    print("=" * 60)
    
    client = PSXClient()
    
    try:
        # Demo 1: OHLCV Data for specific stock
        print("\n📊 1. OHLCV Data for HBL")
        print("-" * 40)
        all_stocks = await client.get_market_watch_data()
        hbl_stock = next((s for s in all_stocks if s['symbol'] == 'HBL'), None)
        if hbl_stock:
            print(f"  Symbol: {hbl_stock['symbol']}")
            print(f"  Open: {hbl_stock['open_price']}")
            print(f"  High: {hbl_stock['high_price']}")
            print(f"  Low: {hbl_stock['low_price']}")
            print(f"  Close: {hbl_stock['current_price']}")
            print(f"  Volume: {hbl_stock['volume']}")
            print(f"  Change: {hbl_stock['change_percent']}%")
        
        # Demo 2: Date Range EOD Data
        print("\n📅 2. EOD Data for Date Range (Last 30 days)")
        print("-" * 40)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        eod_data = await client.get_eod_data("HBL")
        filtered_data = [
            point for point in eod_data 
            if start_date.timestamp() <= point['timestamp'] <= end_date.timestamp()
        ]
        
        print(f"  Found {len(filtered_data)} data points in last 30 days")
        if filtered_data:
            print(f"  Latest: {datetime.fromtimestamp(filtered_data[0]['timestamp']).strftime('%Y-%m-%d')} - Price: {filtered_data[0]['price']}")
            print(f"  Oldest: {datetime.fromtimestamp(filtered_data[-1]['timestamp']).strftime('%Y-%m-%d')} - Price: {filtered_data[-1]['price']}")
        
        # Demo 3: Intraday Time Range
        print("\n⏰ 3. Intraday Data for Time Range")
        print("-" * 40)
        intraday_data = await client.get_intraday_data("HBL")
        if intraday_data:
            # Get last 2 hours of data
            latest_time = intraday_data[0]['timestamp']
            two_hours_ago = latest_time - (2 * 60 * 60)  # 2 hours in seconds
            
            recent_data = [
                point for point in intraday_data 
                if point['timestamp'] >= two_hours_ago
            ]
            
            print(f"  Found {len(recent_data)} data points in last 2 hours")
            if recent_data:
                print(f"  Latest: {datetime.fromtimestamp(recent_data[0]['timestamp']).strftime('%H:%M:%S')} - Price: {recent_data[0]['price']}")
                print(f"  Volume range: {min(p['volume'] for p in recent_data)} - {max(p['volume'] for p in recent_data)}")
        
        # Demo 4: Multiple Stocks OHLCV
        print("\n📈 4. Multiple Stocks OHLCV Data")
        print("-" * 40)
        symbols_to_check = ['HBL', 'OGDC']
        for symbol in symbols_to_check:
            stock = next((s for s in all_stocks if s['symbol'] == symbol), None)
            if stock:
                print(f"  {symbol}: O:{stock['open_price']} H:{stock['high_price']} L:{stock['low_price']} C:{stock['current_price']} V:{stock['volume']}")
        
        # Demo 5: Price at Specific Time
        print("\n🎯 5. Price at Specific Time")
        print("-" * 40)
        if intraday_data:
            # Get a timestamp from 1 hour ago
            one_hour_ago = intraday_data[0]['timestamp'] - (60 * 60)
            closest_point = min(
                intraday_data, 
                key=lambda x: abs(x['timestamp'] - one_hour_ago)
            )
            print(f"  Closest price to 1 hour ago: {closest_point['price']}")
            print(f"  Time: {datetime.fromtimestamp(closest_point['timestamp']).strftime('%H:%M:%S')}")
        
        # Demo 6: Volume Analysis
        print("\n📊 6. Volume Analysis (Last 30 days)")
        print("-" * 40)
        if filtered_data:
            volumes = [point['volume'] for point in filtered_data]
            prices = [point['price'] for point in filtered_data]
            
            print(f"  Average Volume: {sum(volumes) / len(volumes):,.0f}")
            print(f"  Max Volume: {max(volumes):,}")
            print(f"  Min Volume: {min(volumes):,}")
            print(f"  Average Price: {sum(prices) / len(prices):.2f}")
            print(f"  Price Range: {min(prices):.2f} - {max(prices):.2f}")
        
        print("\n✅ All advanced demos completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    
    finally:
        await client.close()

def show_all_tools():
    """Show all available MCP tools"""
    print("\n🔧 Complete List of Available MCP Tools")
    print("-" * 50)
    
    basic_tools = [
        "get_market_watch() - Get all stocks data",
        "get_stock_intraday_data(symbol) - Get intraday data",
        "get_stock_eod_data(symbol) - Get historical EOD data",
        "search_stocks_by_sector(sector) - Filter by sector",
        "get_top_gainers(limit) - Top performing stocks",
        "get_top_losers(limit) - Worst performing stocks"
    ]
    
    advanced_tools = [
        "get_eod_data_by_date_range(symbol, start_date, end_date) - EOD data for date range",
        "get_intraday_data_by_time_range(symbol, start_time, end_time) - Intraday for time range",
        "get_ohlcv_data(symbol) - OHLCV data for specific stock",
        "get_multiple_stocks_ohlcv(symbols) - OHLCV for multiple stocks",
        "get_stock_price_at_time(symbol, timestamp) - Price at specific timestamp",
        "get_volume_analysis(symbol, days) - Volume analysis over time period"
    ]
    
    print("📊 Basic Tools:")
    for i, tool in enumerate(basic_tools, 1):
        print(f"  {i}. {tool}")
    
    print("\n🎯 Advanced Tools:")
    for i, tool in enumerate(advanced_tools, 1):
        print(f"  {i}. {tool}")
    
    print(f"\n📈 Total Tools Available: {len(basic_tools) + len(advanced_tools)}")

def show_usage_examples():
    """Show usage examples for the new tools"""
    print("\n📖 Usage Examples")
    print("-" * 30)
    print("Date Range EOD:")
    print("  'Get HBL data from 2024-01-01 to 2024-01-31'")
    print()
    print("Time Range Intraday:")
    print("  'Get HBL intraday data from 2024-10-04 09:00:00 to 2024-10-04 15:00:00'")
    print()
    print("OHLCV Data:")
    print("  'Get OHLCV data for HBL'")
    print("  'Get OHLCV for HBL,OGDC,PTC'")
    print()
    print("Volume Analysis:")
    print("  'Analyze volume for HBL over last 60 days'")
    print()
    print("Price at Time:")
    print("  'Get HBL price at timestamp 1759491298'")

async def main():
    """Run the complete demo"""
    show_all_tools()
    show_usage_examples()
    await demo_new_tools()
    
    print("\n🎉 Advanced PSX MCP Server is ready with 12 powerful tools!")

if __name__ == "__main__":
    asyncio.run(main())
