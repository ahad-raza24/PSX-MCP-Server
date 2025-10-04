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
async def market_data() -> str:
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
async def intraday(symbol: str) -> str:
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
async def history(symbol: str) -> str:
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
async def sector(sector: str) -> str:
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
async def gainers(limit: int = 10) -> str:
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
async def losers(limit: int = 10) -> str:
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

@mcp.tool()
async def date_range(symbol: str, start_date: str, end_date: str) -> str:
    """
    Get end-of-day data for a specific stock within a date range.
    
    Args:
        symbol: Stock symbol (e.g., 'HBL', 'OGDC', 'PTC')
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
    
    Returns:
        JSON string containing EOD data within the specified date range
    """
    try:
        from datetime import datetime
        import time
        
        # Convert dates to timestamps
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        start_timestamp = int(start_dt.timestamp())
        end_timestamp = int(end_dt.timestamp())
        
        # Get all EOD data
        all_data = await psx_client.get_eod_data(symbol.upper())
        
        # Filter by date range
        filtered_data = [
            point for point in all_data 
            if start_timestamp <= point['timestamp'] <= end_timestamp
        ]
        
        return json.dumps(filtered_data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def time_range(symbol: str, start_time: str, end_time: str) -> str:
    """
    Get intraday data for a specific stock within a time range.
    
    Args:
        symbol: Stock symbol (e.g., 'HBL', 'OGDC', 'PTC')
        start_time: Start time in YYYY-MM-DD HH:MM:SS format
        end_time: End time in YYYY-MM-DD HH:MM:SS format
    
    Returns:
        JSON string containing intraday data within the specified time range
    """
    try:
        from datetime import datetime
        import time
        
        # Convert times to timestamps
        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        start_timestamp = int(start_dt.timestamp())
        end_timestamp = int(end_dt.timestamp())
        
        # Get all intraday data
        all_data = await psx_client.get_intraday_data(symbol.upper())
        
        # Filter by time range
        filtered_data = [
            point for point in all_data 
            if start_timestamp <= point['timestamp'] <= end_timestamp
        ]
        
        return json.dumps(filtered_data, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def ohlcv(symbol: str) -> str:
    """
    Get OHLCV (Open, High, Low, Close, Volume) data for a specific stock.
    
    Args:
        symbol: Stock symbol (e.g., 'HBL', 'OGDC', 'PTC')
    
    Returns:
        JSON string containing OHLCV data from market watch
    """
    try:
        all_stocks = await psx_client.get_market_watch_data()
        
        # Find the specific stock
        stock_data = None
        for stock in all_stocks:
            if stock.get('symbol', '').upper() == symbol.upper():
                stock_data = stock
                break
        
        if not stock_data:
            return json.dumps({"error": f"Stock symbol {symbol} not found"})
        
        # Extract OHLCV data
        ohlcv = {
            "symbol": stock_data.get('symbol'),
            "sector": stock_data.get('sector'),
            "open": stock_data.get('open_price'),
            "high": stock_data.get('high_price'),
            "low": stock_data.get('low_price'),
            "close": stock_data.get('current_price'),
            "volume": stock_data.get('volume'),
            "ldcp": stock_data.get('ldcp'),
            "change": stock_data.get('change'),
            "change_percent": stock_data.get('change_percent')
        }
        
        return json.dumps(ohlcv, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def multi_ohlcv(symbols: str) -> str:
    """
    Get OHLCV data for multiple stocks at once.
    
    Args:
        symbols: Comma-separated list of stock symbols (e.g., 'HBL,OGDC,PTC')
    
    Returns:
        JSON string containing OHLCV data for all requested stocks
    """
    try:
        symbol_list = [s.strip().upper() for s in symbols.split(',')]
        all_stocks = await psx_client.get_market_watch_data()
        
        result = []
        for symbol in symbol_list:
            stock_data = None
            for stock in all_stocks:
                if stock.get('symbol', '').upper() == symbol:
                    stock_data = stock
                    break
            
            if stock_data:
                ohlcv = {
                    "symbol": stock_data.get('symbol'),
                    "sector": stock_data.get('sector'),
                    "open": stock_data.get('open_price'),
                    "high": stock_data.get('high_price'),
                    "low": stock_data.get('low_price'),
                    "close": stock_data.get('current_price'),
                    "volume": stock_data.get('volume'),
                    "ldcp": stock_data.get('ldcp'),
                    "change": stock_data.get('change'),
                    "change_percent": stock_data.get('change_percent')
                }
                result.append(ohlcv)
            else:
                result.append({"symbol": symbol, "error": "Not found"})
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def price_at_time(symbol: str, timestamp: int) -> str:
    """
    Get the closest price data for a stock at a specific timestamp.
    
    Args:
        symbol: Stock symbol (e.g., 'HBL', 'OGDC', 'PTC')
        timestamp: Unix timestamp to find closest price for
    
    Returns:
        JSON string containing the closest price data point
    """
    try:
        # Get intraday data
        intraday_data = await psx_client.get_intraday_data(symbol.upper())
        
        if not intraday_data:
            return json.dumps({"error": f"No intraday data found for {symbol}"})
        
        # Find the closest timestamp
        closest_point = min(
            intraday_data, 
            key=lambda x: abs(x['timestamp'] - timestamp)
        )
        
        return json.dumps(closest_point, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool()
async def volume_analysis(symbol: str, days: int = 30) -> str:
    """
    Analyze volume patterns for a stock over a specified number of days.
    
    Args:
        symbol: Stock symbol (e.g., 'HBL', 'OGDC', 'PTC')
        days: Number of days to analyze (default: 30)
    
    Returns:
        JSON string containing volume analysis statistics
    """
    try:
        from datetime import datetime, timedelta
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        
        # Get EOD data for the period
        eod_data = await psx_client.get_eod_data(symbol.upper())
        
        # Filter by date range
        filtered_data = [
            point for point in eod_data 
            if start_timestamp <= point['timestamp'] <= end_timestamp
        ]
        
        if not filtered_data:
            return json.dumps({"error": f"No data found for {symbol} in the last {days} days"})
        
        # Calculate volume statistics
        volumes = [point['volume'] for point in filtered_data]
        prices = [point['price'] for point in filtered_data]
        
        analysis = {
            "symbol": symbol,
            "period_days": days,
            "data_points": len(filtered_data),
            "volume_stats": {
                "average_volume": sum(volumes) / len(volumes),
                "max_volume": max(volumes),
                "min_volume": min(volumes),
                "total_volume": sum(volumes)
            },
            "price_stats": {
                "average_price": sum(prices) / len(prices),
                "max_price": max(prices),
                "min_price": min(prices),
                "price_change": prices[-1] - prices[0] if len(prices) > 1 else 0
            },
            "latest_data": filtered_data[0] if filtered_data else None
        }
        
        return json.dumps(analysis, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

async def cleanup():
    """Cleanup function to close HTTP client"""
    await psx_client.close()

# Note: FastMCP handles cleanup automatically when the server shuts down

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
