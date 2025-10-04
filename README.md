# PSX MCP Server

A Model Context Protocol (MCP) server that provides tools to scrape and access Pakistan Stock Exchange (PSX) market data.

## Features

This MCP server provides **12 powerful tools** for comprehensive PSX data access:

### 📊 Basic Tools
1. **get_market_watch** - Get current market data for all 460+ stocks listed on PSX
2. **get_stock_intraday_data** - Get intraday time series data for a specific stock
3. **get_stock_eod_data** - Get end-of-day historical data for a specific stock (past 5 years)
4. **search_stocks_by_sector** - Search stocks by sector
5. **get_top_gainers** - Get top gaining stocks
6. **get_top_losers** - Get top losing stocks

### 🎯 Advanced Tools
7. **get_eod_data_by_date_range** - Get EOD data for specific date range (YYYY-MM-DD format)
8. **get_intraday_data_by_time_range** - Get intraday data for specific time range (YYYY-MM-DD HH:MM:SS format)
9. **get_ohlcv_data** - Get OHLCV (Open, High, Low, Close, Volume) data for specific stock
10. **get_multiple_stocks_ohlcv** - Get OHLCV data for multiple stocks (comma-separated symbols)
11. **get_stock_price_at_time** - Get closest price data at specific Unix timestamp
12. **get_volume_analysis** - Analyze volume patterns over specified number of days

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the MCP server:
```bash
python psx_mcp_server.py
```

## Data Sources

The server scrapes data from the following PSX endpoints:

- `https://dps.psx.com.pk/market-watch` - Market watch data
- `https://dps.psx.com.pk/timeseries/int/{SYMBOL}` - Intraday data
- `https://dps.psx.com.pk/timeseries/eod/{SYMBOL}` - End-of-day data

## Usage

The server can be used with any MCP client, such as Gemini CLI. The tools return JSON data that can be processed by the client.

### Example Queries

**Basic Data:**
- "Get market data for HBL"
- "Show me top 10 gaining stocks"
- "Find all banking sector stocks"

**Advanced Filtering:**
- "Get HBL data from 2024-01-01 to 2024-01-31"
- "Get HBL intraday data from 2024-10-04 09:00:00 to 2024-10-04 15:00:00"
- "Get OHLCV data for HBL,OGDC,PTC"
- "Analyze volume for HBL over last 60 days"

### Example Stock Symbols

- HBL - Habib Bank Limited
- OGDC - Oil and Gas Development Company
- PTC - Pakistan Telecommunication Company
- LUCK - Lucky Cement
- ENGRO - Engro Corporation

## Data Models

### Stock Data
- Symbol, Sector, Listed In
- LDCP, Open, High, Low, Current prices
- Change amount and percentage
- Volume traded

### Time Series Data
- Unix timestamp
- Price/Close price
- Volume
- Open price (for EOD data)

## Error Handling

All tools include proper error handling and return error messages in JSON format if requests fail.
