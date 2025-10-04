# PSX MCP Server API Documentation

## Overview

The PSX MCP Server provides 12 powerful tools for accessing Pakistan Stock Exchange data through the Model Context Protocol (MCP).

## Basic Tools

### 1. market_data()
Get current market data for all stocks listed on PSX.

**Returns:** JSON string containing market data for all stocks

**Example:**
```python
result = await market_data()
```

### 2. intraday(symbol)
Get intraday time series data for a specific stock.

**Parameters:**
- `symbol` (str): Stock symbol (e.g., 'HBL', 'OGDC', 'PTC')

**Returns:** JSON string containing intraday data points

**Example:**
```python
result = await intraday('HBL')
```

### 3. history(symbol)
Get end-of-day historical data for a specific stock (past 5 years).

**Parameters:**
- `symbol` (str): Stock symbol

**Returns:** JSON string containing EOD data points

**Example:**
```python
result = await history('HBL')
```

### 4. sector(sector)
Search for stocks by sector.

**Parameters:**
- `sector` (str): Sector name (e.g., 'Banking', 'Technology', 'Energy')

**Returns:** JSON string containing stocks in the specified sector

**Example:**
```python
result = await sector('Banking')
```

### 5. gainers(limit)
Get top gaining stocks.

**Parameters:**
- `limit` (int): Number of top gainers to return (default: 10)

**Returns:** JSON string containing top gaining stocks

**Example:**
```python
result = await gainers(5)
```

### 6. losers(limit)
Get top losing stocks.

**Parameters:**
- `limit` (int): Number of top losers to return (default: 10)

**Returns:** JSON string containing top losing stocks

**Example:**
```python
result = await losers(5)
```

## Advanced Tools

### 7. date_range(symbol, start_date, end_date)
Get EOD data for a specific date range.

**Parameters:**
- `symbol` (str): Stock symbol
- `start_date` (str): Start date in YYYY-MM-DD format
- `end_date` (str): End date in YYYY-MM-DD format

**Returns:** JSON string containing filtered EOD data

**Example:**
```python
result = await date_range('HBL', '2024-01-01', '2024-01-31')
```

### 8. time_range(symbol, start_time, end_time)
Get intraday data for a specific time range.

**Parameters:**
- `symbol` (str): Stock symbol
- `start_time` (str): Start time in YYYY-MM-DD HH:MM:SS format
- `end_time` (str): End time in YYYY-MM-DD HH:MM:SS format

**Returns:** JSON string containing filtered intraday data

**Example:**
```python
result = await time_range('HBL', '2024-10-04 09:00:00', '2024-10-04 15:00:00')
```

### 9. ohlcv(symbol)
Get OHLCV data for a specific stock.

**Parameters:**
- `symbol` (str): Stock symbol

**Returns:** JSON string containing OHLCV data

**Example:**
```python
result = await ohlcv('HBL')
```

### 10. multi_ohlcv(symbols)
Get OHLCV data for multiple stocks.

**Parameters:**
- `symbols` (str): Comma-separated list of stock symbols

**Returns:** JSON string containing OHLCV data for all stocks

**Example:**
```python
result = await multi_ohlcv('HBL,OGDC,PTC')
```

### 11. price_at_time(symbol, timestamp)
Get closest price data at a specific timestamp.

**Parameters:**
- `symbol` (str): Stock symbol
- `timestamp` (int): Unix timestamp

**Returns:** JSON string containing closest price data point

**Example:**
```python
result = await price_at_time('HBL', 1759491298)
```

### 12. volume_analysis(symbol, days)
Analyze volume patterns over a specified period.

**Parameters:**
- `symbol` (str): Stock symbol
- `days` (int): Number of days to analyze (default: 30)

**Returns:** JSON string containing volume analysis statistics

**Example:**
```python
result = await volume_analysis('HBL', 60)
```

## Data Models

### StockData
```python
{
    "symbol": str,
    "sector": str,
    "listed_in": str,
    "ldcp": float,
    "open_price": float,
    "high_price": float,
    "low_price": float,
    "current_price": float,
    "change": float,
    "change_percent": float,
    "volume": int
}
```

### TimeSeriesData
```python
{
    "timestamp": int,
    "price": float,
    "volume": int,
    "open_price": float  # Optional, for EOD data
}
```

## Error Handling

All tools return JSON with either:
- **Success:** Requested data
- **Error:** `{"error": "error_message"}`

## Rate Limiting

The server implements rate limiting to prevent API abuse:
- Maximum 100 requests per minute
- 60-second sliding window

## Usage with Gemini CLI

```bash
# Start the server
python scripts/start_server.py

# Connect with Gemini CLI
gemini-cli --mcp-server scripts/start_server.py
```
