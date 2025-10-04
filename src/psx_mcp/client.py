"""
PSX API Client for fetching market data
"""

import httpx
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import re
from .models import TimeSeriesData


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

            # Parse HTML response
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the market data table
            table = soup.find('table', {'id': 'marketWatchTable'}) or soup.find('table')
            if not table:
                raise Exception("Market data table not found in HTML response")

            stocks = []
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 9:  # Ensure we have enough columns
                    try:
                        stock_data = {
                            "symbol": cells[0].get_text(strip=True),
                            "sector": cells[1].get_text(strip=True),
                            "listed_in": cells[2].get_text(strip=True),
                            "ldcp": self._parse_float(cells[3].get_text(strip=True)),
                            "open_price": self._parse_float(cells[4].get_text(strip=True)),
                            "high_price": self._parse_float(cells[5].get_text(strip=True)),
                            "low_price": self._parse_float(cells[6].get_text(strip=True)),
                            "current_price": self._parse_float(cells[7].get_text(strip=True)),
                            "change": self._parse_float(cells[8].get_text(strip=True)),
                            "change_percent": self._parse_float(cells[9].get_text(strip=True)) if len(cells) > 9 else 0.0,
                            "volume": self._parse_int(cells[10].get_text(strip=True)) if len(cells) > 10 else 0,
                        }
                        stocks.append(stock_data)
                    except (ValueError, IndexError) as e:
                        # Skip rows with invalid data
                        continue

            return stocks

        except Exception as e:
            raise Exception(f"Failed to fetch market watch data: {str(e)}")

    def _parse_float(self, text: str) -> float:
        """Parse float value from text, handling commas and other formatting"""
        if not text or text == '-':
            return 0.0
        # Remove commas and other formatting
        cleaned = re.sub(r'[^\d.-]', '', text)
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    def _parse_int(self, text: str) -> int:
        """Parse integer value from text, handling commas and other formatting"""
        if not text or text == '-':
            return 0
        # Remove commas and other formatting
        cleaned = re.sub(r'[^\d]', '', text)
        try:
            return int(cleaned)
        except ValueError:
            return 0

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
                        timestamp=item[0], price=float(item[1]), volume=int(item[2])
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
                        open_price=float(item[3]),
                    )
                    eod_data.append(time_point.model_dump())

            return eod_data

        except Exception as e:
            raise Exception(f"Failed to fetch EOD data for {symbol}: {str(e)}")

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
