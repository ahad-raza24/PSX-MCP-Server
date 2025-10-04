#!/usr/bin/env python3
"""
PSX MCP Server - Pakistan Stock Exchange Data Scraper
Provides tools to fetch market data from PSX website
"""

from fastmcp import FastMCP
from .tools import (
    market_data,
    intraday,
    history,
    sector,
    gainers,
    losers,
    date_range,
    time_range,
    ohlcv,
    multi_ohlcv,
    price_at_time,
    volume_analysis,
)

# Initialize the MCP server
mcp = FastMCP("PSX Data Scraper")

# Register all tools
mcp.tool()(market_data)
mcp.tool()(intraday)
mcp.tool()(history)
mcp.tool()(sector)
mcp.tool()(gainers)
mcp.tool()(losers)
mcp.tool()(date_range)
mcp.tool()(time_range)
mcp.tool()(ohlcv)
mcp.tool()(multi_ohlcv)
mcp.tool()(price_at_time)
mcp.tool()(volume_analysis)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
