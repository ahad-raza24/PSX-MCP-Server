# PSX MCP Server

A Model Context Protocol (MCP) server that provides tools to scrape and access Pakistan Stock Exchange (PSX) market data.

## Features

This MCP server provides the following tools:

1. **get_market_watch** - Get current market data for all 460+ stocks listed on PSX
2. **get_stock_intraday_data** - Get intraday time series data for a specific stock
3. **get_stock_eod_data** - Get end-of-day historical data for a specific stock (past 5 years)
4. **search_stocks_by_sector** - Search stocks by sector
5. **get_top_gainers** - Get top gaining stocks
6. **get_top_losers** - Get top losing stocks

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
