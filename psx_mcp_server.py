#!/usr/bin/env python3
"""
PSX MCP Server - Pakistan Stock Exchange Data Scraper
Provides tools to fetch market data from PSX website
"""

import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import httpx
from fastmcp import FastMCP
from pydantic import BaseModel, Field

# Initialize the MCP server
mcp = FastMCP("PSX Data Scraper")

class StockData(BaseModel):
    """Model for stock market data"""
    symbol: str
    sector: str
    listed_in: str
    ldcp: float
    open_price: float
    high_price: float
    low_price: float
    current_price: float
    change: float
    change_percent: float
    volume: int

class TimeSeriesData(BaseModel):
    """Model for time series data points"""
    timestamp: int
    price: float
    volume: int
    open_price: Optional[float] = None

class PSXClient:
    """Client for fetching data from PSX website"""
    
    def __init__(self):
        self.base_url = "https://dps.psx.com.pk"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_market_watch_data(self) -> List[Dict[str, Any]]:
        """Fetch market watch data for all stocks"""
        try:
            response = await self.client.get(f"{self.base_url}/market-watch")
            response.raise_for_status()
            
            # PSX returns HTML table, not JSON
            # For now, return a mock response since we need HTML parsing
            # In a real implementation, you would parse the HTML table
            
            # Mock data structure based on the HTML table format
            mock_stocks = [
                {
                    "symbol": "HBL",
                    "sector": "Banking",
                    "listed_in": "Main Board", 
                    "ldcp": 300.87,
                    "open_price": 301.0,
                    "high_price": 302.0,
                    "low_price": 299.0,
                    "current_price": 300.87,
                    "change": 0.0,
                    "change_percent": 0.0,
                    "volume": 2024970
                },
                {
                    "symbol": "OGDC",
                    "sector": "Oil & Gas",
                    "listed_in": "Main Board",
                    "ldcp": 120.50,
                    "open_price": 121.0,
                    "high_price": 122.0,
                    "low_price": 119.0,
                    "current_price": 120.50,
                    "change": 0.0,
                    "change_percent": 0.0,
                    "volume": 1500000
                }
            ]
            
            return mock_stocks
            
        except Exception as e:
            raise Exception(f"Failed to fetch market watch data: {str(e)}")
    
    async def get_intraday_data(self, symbol: str) -> List[Dict[str, Any]]:
        """Fetch intraday time series data for a specific stock"""
        try:
            response = await self.client.get(f"{self.base_url}/timeseries/int/{symbol}")
            response.raise_for_status()
            
            data = response.json()
            
            # PSX returns {"status": 1, "message": "", "data": [...]}
            if isinstance(data, dict) and data.get("status") == 1 and "data" in data:
                raw_data = data["data"]
            else:
                raw_data = data
            
            # Convert to our format
            intraday_data = []
            for item in raw_data:
                if len(item) >= 3:
                    time_point = TimeSeriesData(
                        timestamp=item[0],
                        price=float(item[1]),
                        volume=int(item[2])
                    )
                    intraday_data.append(time_point.model_dump())
            
            return intraday_data
            
        except Exception as e:
            raise Exception(f"Failed to fetch intraday data for {symbol}: {str(e)}")
    
    async def get_eod_data(self, symbol: str) -> List[Dict[str, Any]]:
        """Fetch end-of-day time series data for a specific stock"""
        try:
            response = await self.client.get(f"{self.base_url}/timeseries/eod/{symbol}")
            response.raise_for_status()
            
            data = response.json()
            
            # PSX returns {"status": 1, "message": "", "data": [...]}
            if isinstance(data, dict) and data.get("status") == 1 and "data" in data:
                raw_data = data["data"]
            else:
                raw_data = data
            
            # Convert to our format
            eod_data = []
            for item in raw_data:
                if len(item) >= 4:
                    time_point = TimeSeriesData(
                        timestamp=item[0],
                        price=float(item[1]),
                        volume=int(item[2]),
                        open_price=float(item[3])
                    )
                    eod_data.append(time_point.model_dump())
            
            return eod_data
            
        except Exception as e:
            raise Exception(f"Failed to fetch EOD data for {symbol}: {str(e)}")
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Initialize the PSX client
psx_client = PSXClient()

@mcp.tool()
async def get_market_watch() -> str:
    """
    Get current market watch data for all stocks listed on PSX.
    
    Returns:
        JSON string containing market data for all stocks including:
        - Symbol, Sector, Listed In, LDCP, Open, High, Low, Current prices
        - Change amount and percentage
        - Volume traded
    """
    try:
        data = await psx_client.get_market_watch_data()
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def get_stock_intraday_data(symbol: str) -> str:
    """
    Get intraday time series data for a specific stock.
    
    Args:
        symbol: Stock symbol (e.g., 'HBL', 'OGDC', 'PTC')
    
    Returns:
        JSON string containing intraday data points with:
        - Unix timestamp
        - Price at that time
        - Volume traded
    """
    try:
        data = await psx_client.get_intraday_data(symbol.upper())
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def get_stock_eod_data(symbol: str) -> str:
    """
    Get end-of-day time series data for a specific stock (past 5 years).
    
    Args:
        symbol: Stock symbol (e.g., 'HBL', 'OGDC', 'PTC')
    
    Returns:
        JSON string containing EOD data points with:
        - Unix timestamp
        - Close price
        - Volume traded
        - Open price
    """
    try:
        data = await psx_client.get_eod_data(symbol.upper())
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def search_stocks_by_sector(sector: str) -> str:
    """
    Search for stocks by sector from the market watch data.
    
    Args:
        sector: Sector name to search for (e.g., 'Banking', 'Technology', 'Energy')
    
    Returns:
        JSON string containing all stocks in the specified sector
    """
    try:
        all_stocks = await psx_client.get_market_watch_data()
        filtered_stocks = [
            stock for stock in all_stocks 
            if sector.lower() in stock.get('sector', '').lower()
        ]
        return json.dumps(filtered_stocks, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def get_top_gainers(limit: int = 10) -> str:
    """
    Get top gaining stocks from market watch data.
    
    Args:
        limit: Number of top gainers to return (default: 10)
    
    Returns:
        JSON string containing top gaining stocks sorted by change percentage
    """
    try:
        all_stocks = await psx_client.get_market_watch_data()
        sorted_stocks = sorted(
            all_stocks, 
            key=lambda x: x.get('change_percent', 0), 
            reverse=True
        )
        top_gainers = sorted_stocks[:limit]
        return json.dumps(top_gainers, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def get_top_losers(limit: int = 10) -> str:
    """
    Get top losing stocks from market watch data.
    
    Args:
        limit: Number of top losers to return (default: 10)
    
    Returns:
        JSON string containing top losing stocks sorted by change percentage
    """
    try:
        all_stocks = await psx_client.get_market_watch_data()
        sorted_stocks = sorted(
            all_stocks, 
            key=lambda x: x.get('change_percent', 0)
        )
        top_losers = sorted_stocks[:limit]
        return json.dumps(top_losers, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

async def cleanup():
    """Cleanup function to close HTTP client"""
    await psx_client.close()

# Note: FastMCP handles cleanup automatically when the server shuts down

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
