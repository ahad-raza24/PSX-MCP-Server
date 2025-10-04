# PSX MCP Server

A Model Context Protocol (MCP) server that provides tools to scrape and access Pakistan Stock Exchange (PSX) market data.

## Features

This MCP server provides **12 powerful tools** for comprehensive PSX data access:

### 📊 Basic Tools (Simple & Intuitive)
1. **market_data()** - Get current market data for all 460+ stocks listed on PSX
2. **intraday(symbol)** - Get intraday time series data for a specific stock
3. **history(symbol)** - Get end-of-day historical data for a specific stock (past 5 years)
4. **sector(sector)** - Search stocks by sector
5. **gainers(limit)** - Get top gaining stocks
6. **losers(limit)** - Get top losing stocks

### 🎯 Advanced Tools (Clean & Powerful)
7. **date_range(symbol, start, end)** - Get EOD data for specific date range (YYYY-MM-DD format)
8. **time_range(symbol, start, end)** - Get intraday data for specific time range (YYYY-MM-DD HH:MM:SS format)
9. **ohlcv(symbol)** - Get OHLCV (Open, High, Low, Close, Volume) data for specific stock
10. **multi_ohlcv(symbols)** - Get OHLCV data for multiple stocks (comma-separated symbols)
11. **price_at_time(symbol, timestamp)** - Get closest price data at specific Unix timestamp
12. **volume_analysis(symbol, days)** - Analyze volume patterns over specified number of days

## Installation

### Option 1: Direct Installation
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Gemini CLI (copy and customize the template):
```bash
cp gemini_config.template.json gemini_config.json
# Edit gemini_config.json with your project path
```

3. Run the MCP server:
```bash
python scripts/start_server.py
```

### Option 2: Development Installation
1. Install with development tools:
```bash
make setup
# or
pip install -e ".[dev]"
```

2. Run with Makefile:
```bash
make run-server
```

### Option 3: Docker
1. Build the Docker image:
```bash
docker build -t psx-mcp-server .
```

2. Run the container:
```bash
docker run -it psx-mcp-server
```

## Configuration

### Template Files
The project includes template configuration files for easy setup:

- **`gemini_config.template.json`** - Simple Gemini CLI configuration template
- **`mcp_config.template.json`** - Advanced MCP configuration template with additional settings

### Quick Setup
1. Copy the template file:
```bash
cp gemini_config.template.json gemini_config.json
```

2. Edit the configuration with your project path:
```json
{
  "mcpServers": {
    "psx-scraper": {
      "command": "python",
      "args": ["/your/actual/path/scripts/start_server.py"],
      "env": {
        "PYTHONPATH": "/your/actual/path/src"
      }
    }
  }
}
```

3. Connect Gemini CLI:
```bash
gemini --config gemini_config.json
```

## Development

### Available Commands
```bash
make help          # Show all available commands
make test          # Run test suite
make lint          # Run linting checks
make format        # Format code with black
make run-demo      # Run demonstrations
make clean         # Clean build artifacts
```

## Data Sources

The server scrapes data from the following PSX endpoints:

- `https://dps.psx.com.pk/market-watch` - Market watch data
- `https://dps.psx.com.pk/timeseries/int/{SYMBOL}` - Intraday data
- `https://dps.psx.com.pk/timeseries/eod/{SYMBOL}` - End-of-day data

## Usage

The server can be used with any MCP client, such as Gemini CLI. The tools return JSON data that can be processed by the client.

### Example Queries

**Basic Data (Super Simple):**
- "Show me market data" → `market_data()`
- "Get HBL intraday data" → `intraday('HBL')`
- "Show HBL history" → `history('HBL')`
- "Find banking stocks" → `sector('Banking')`
- "Top 5 gainers" → `gainers(5)`

**Advanced Filtering (Clean & Intuitive):**
- "HBL data from Jan to Feb" → `date_range('HBL', '2024-01-01', '2024-02-01')`
- "HBL intraday 9AM to 3PM" → `time_range('HBL', '2024-10-04 09:00:00', '2024-10-04 15:00:00')`
- "HBL OHLCV data" → `ohlcv('HBL')`
- "OHLCV for HBL,OGDC" → `multi_ohlcv('HBL,OGDC')`
- "HBL volume analysis" → `volume_analysis('HBL', 30)`

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
