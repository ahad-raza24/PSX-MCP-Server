#!/usr/bin/env python3
"""
Demo script showing the simplified and user-friendly MCP tool names
"""


def show_simplified_tools():
    """Show the new simplified tool names"""
    print("🎯 Simplified PSX MCP Server Tools")
    print("=" * 50)

    basic_tools = [
        ("market_data()", "Get all stocks data"),
        ("intraday(symbol)", "Get intraday data for a stock"),
        ("history(symbol)", "Get historical EOD data"),
        ("sector(sector)", "Find stocks by sector"),
        ("gainers(limit)", "Get top gaining stocks"),
        ("losers(limit)", "Get top losing stocks"),
    ]

    advanced_tools = [
        ("date_range(symbol, start, end)", "Get EOD data for date range"),
        ("time_range(symbol, start, end)", "Get intraday data for time range"),
        ("ohlcv(symbol)", "Get OHLCV data for a stock"),
        ("multi_ohlcv(symbols)", "Get OHLCV for multiple stocks"),
        ("price_at_time(symbol, timestamp)", "Get price at specific time"),
        ("volume_analysis(symbol, days)", "Analyze volume patterns"),
    ]

    print("\n📊 Basic Tools (Super Simple Names):")
    for i, (name, desc) in enumerate(basic_tools, 1):
        print(f"  {i}. {name:<30} - {desc}")

    print("\n🎯 Advanced Tools (Clean & Intuitive):")
    for i, (name, desc) in enumerate(advanced_tools, 1):
        print(f"  {i}. {name:<30} - {desc}")

    print(
        f"\n✨ Total: {len(basic_tools) + len(advanced_tools)} tools with simple names!"
    )


def show_natural_language_examples():
    """Show how natural language maps to simple tool names"""
    print("\n💬 Natural Language → Simple Tool Mapping")
    print("-" * 50)

    examples = [
        ("Show me market data", "market_data()"),
        ("Get HBL intraday data", "intraday('HBL')"),
        ("Show HBL history", "history('HBL')"),
        ("Find banking stocks", "sector('Banking')"),
        ("Top 5 gainers", "gainers(5)"),
        ("Worst 10 stocks", "losers(10)"),
        ("HBL data from Jan to Feb", "date_range('HBL', '2024-01-01', '2024-02-01')"),
        (
            "HBL intraday 9AM to 3PM",
            "time_range('HBL', '2024-10-04 09:00:00', '2024-10-04 15:00:00')",
        ),
        ("HBL OHLCV data", "ohlcv('HBL')"),
        ("OHLCV for HBL,OGDC", "multi_ohlcv('HBL,OGDC')"),
        ("HBL price at timestamp", "price_at_time('HBL', 1759491298)"),
        ("HBL volume analysis", "volume_analysis('HBL', 30)"),
    ]

    for query, tool in examples:
        print(f"  '{query}' → {tool}")


def show_benefits():
    """Show the benefits of simplified naming"""
    print("\n🚀 Benefits of Simplified Names")
    print("-" * 40)

    benefits = [
        "✅ Easy to remember and type",
        "✅ Intuitive and self-explanatory",
        "✅ Shorter and cleaner",
        "✅ Natural language friendly",
        "✅ No complex prefixes or suffixes",
        "✅ Consistent naming pattern",
        "✅ Perfect for voice commands",
        "✅ Great for quick queries",
    ]

    for benefit in benefits:
        print(f"  {benefit}")


def main():
    """Run the demo"""
    show_simplified_tools()
    show_natural_language_examples()
    show_benefits()

    print("\n🎉 PSX MCP Server now has super simple and intuitive tool names!")
    print("   Perfect for natural language interactions with Gemini CLI!")


if __name__ == "__main__":
    main()
