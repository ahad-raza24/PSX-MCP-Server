"""
PSX API Client for fetching market data
"""

import httpx
from typing import List, Dict, Any
from .models import StockData, TimeSeriesData


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
