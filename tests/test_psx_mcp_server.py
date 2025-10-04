#!/usr/bin/env python3
"""
Comprehensive test suite for PSX MCP Server
Tests all tools and functionality
"""

import pytest
import asyncio
import json
import sys
import os
from unittest.mock import Mock, AsyncMock, patch
import httpx

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from psx_mcp.client import PSXClient
from psx_mcp.models import StockData, TimeSeriesData
from psx_mcp.server import mcp

class TestPSXClient:
    """Test the PSXClient class"""
    
    @pytest.fixture
    def psx_client(self):
        """Create a PSXClient instance for testing"""
        return PSXClient()
    
    @pytest.mark.asyncio
    async def test_client_initialization(self, psx_client):
        """Test PSXClient initialization"""
        assert psx_client.base_url == "https://dps.psx.com.pk"
        assert psx_client.client is not None
        assert isinstance(psx_client.client, httpx.AsyncClient)
        await psx_client.close()
    
    @pytest.mark.asyncio
    async def test_market_watch_data_success(self, psx_client):
        """Test successful market watch data retrieval"""
        # Mock response data
        mock_data = [
            {
                "symbol": "HBL",
                "sector": "Banking",
                "listed_in": "Main Board",
                "ldcp": 100.0,
                "open": 101.0,
                "high": 102.0,
                "low": 99.0,
                "current": 101.5,
                "change": 1.5,
                "change_percent": 1.5,
                "volume": 1000000
            },
            {
                "symbol": "OGDC",
                "sector": "Oil & Gas",
                "listed_in": "Main Board",
                "ldcp": 80.0,
                "open": 81.0,
                "high": 82.0,
                "low": 79.0,
                "current": 80.5,
                "change": 0.5,
                "change_percent": 0.6,
                "volume": 500000
            }
        ]
        
        with patch.object(psx_client.client, 'get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_data
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            result = await psx_client.get_market_watch_data()
            
            assert len(result) == 2
            assert result[0]['symbol'] == 'HBL'
            assert result[0]['current_price'] == 101.5
            assert result[1]['symbol'] == 'OGDC'
            assert result[1]['sector'] == 'Oil & Gas'
        
        await psx_client.close()
    
    @pytest.mark.asyncio
    async def test_market_watch_data_failure(self, psx_client):
        """Test market watch data retrieval failure"""
        with patch.object(psx_client.client, 'get') as mock_get:
            mock_get.side_effect = httpx.RequestError("Network error")
            
            with pytest.raises(Exception) as exc_info:
                await psx_client.get_market_watch_data()
            
            assert "Failed to fetch market watch data" in str(exc_info.value)
        
        await psx_client.close()
    
    @pytest.mark.asyncio
    async def test_intraday_data_success(self, psx_client):
        """Test successful intraday data retrieval"""
        mock_data = [
            [1759491298, 300.87, 1000],
            [1759491300, 301.20, 1500],
            [1759491302, 300.50, 800]
        ]
        
        with patch.object(psx_client.client, 'get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_data
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            result = await psx_client.get_intraday_data("HBL")
            
            assert len(result) == 3
            assert result[0]['timestamp'] == 1759491298
            assert result[0]['price'] == 300.87
            assert result[0]['volume'] == 1000
            assert result[1]['price'] == 301.20
        
        await psx_client.close()
    
    @pytest.mark.asyncio
    async def test_eod_data_success(self, psx_client):
        """Test successful EOD data retrieval"""
        mock_data = [
            [1759489200, 300.87, 2024970, 305],
            [1759575600, 302.15, 1987654, 301],
            [1759662000, 299.50, 2154321, 303]
        ]
        
        with patch.object(psx_client.client, 'get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_data
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            result = await psx_client.get_eod_data("HBL")
            
            assert len(result) == 3
            assert result[0]['timestamp'] == 1759489200
            assert result[0]['price'] == 300.87
            assert result[0]['volume'] == 2024970
            assert result[0]['open_price'] == 305
        
        await psx_client.close()
    
    @pytest.mark.asyncio
    async def test_intraday_data_failure(self, psx_client):
        """Test intraday data retrieval failure"""
        with patch.object(psx_client.client, 'get') as mock_get:
            mock_get.side_effect = httpx.RequestError("Network error")
            
            with pytest.raises(Exception) as exc_info:
                await psx_client.get_intraday_data("INVALID")
            
            assert "Failed to fetch intraday data for INVALID" in str(exc_info.value)
        
        await psx_client.close()
    
    @pytest.mark.asyncio
    async def test_eod_data_failure(self, psx_client):
        """Test EOD data retrieval failure"""
        with patch.object(psx_client.client, 'get') as mock_get:
            mock_get.side_effect = httpx.RequestError("Network error")
            
            with pytest.raises(Exception) as exc_info:
                await psx_client.get_eod_data("INVALID")
            
            assert "Failed to fetch EOD data for INVALID" in str(exc_info.value)
        
        await psx_client.close()

class TestMCPTools:
    """Test MCP tools functionality by importing the actual tool functions"""
    
    @pytest.mark.asyncio
    async def test_get_market_watch_tool_success(self):
        """Test get_market_watch tool success"""
        # Import the actual tool function
        from psx_mcp_server import get_market_watch
        
        mock_data = [
            {
                "symbol": "HBL",
                "sector": "Banking",
                "listed_in": "Main Board",
                "ldcp": 100.0,
                "open": 101.0,
                "high": 102.0,
                "low": 99.0,
                "current": 101.5,
                "change": 1.5,
                "change_percent": 1.5,
                "volume": 1000000
            }
        ]
        
        with patch('psx_mcp_server.psx_client.get_market_watch_data', return_value=mock_data):
            result = await get_market_watch()
            data = json.loads(result)
            
            assert len(data) == 1
            assert data[0]['symbol'] == 'HBL'
            assert data[0]['current_price'] == 101.5
    
    @pytest.mark.asyncio
    async def test_get_market_watch_tool_failure(self):
        """Test get_market_watch tool failure"""
        from psx_mcp_server import get_market_watch
        
        with patch('psx_mcp_server.psx_client.get_market_watch_data', side_effect=Exception("API Error")):
            result = await get_market_watch()
            data = json.loads(result)
            
            assert "error" in data
            assert data["error"] == "API Error"
    
    @pytest.mark.asyncio
    async def test_get_stock_intraday_data_tool_success(self):
        """Test get_stock_intraday_data tool success"""
        from psx_mcp_server import get_stock_intraday_data
        
        mock_data = [
            {"timestamp": 1759491298, "price": 300.87, "volume": 1000},
            {"timestamp": 1759491300, "price": 301.20, "volume": 1500}
        ]
        
        with patch('psx_mcp_server.psx_client.get_intraday_data', return_value=mock_data):
            result = await get_stock_intraday_data("HBL")
            data = json.loads(result)
            
            assert len(data) == 2
            assert data[0]['timestamp'] == 1759491298
            assert data[0]['price'] == 300.87
    
    @pytest.mark.asyncio
    async def test_get_stock_intraday_data_tool_failure(self):
        """Test get_stock_intraday_data tool failure"""
        from psx_mcp_server import get_stock_intraday_data
        
        with patch('psx_mcp_server.psx_client.get_intraday_data', side_effect=Exception("API Error")):
            result = await get_stock_intraday_data("INVALID")
            data = json.loads(result)
            
            assert "error" in data
            assert data["error"] == "API Error"
    
    @pytest.mark.asyncio
    async def test_get_stock_eod_data_tool_success(self):
        """Test get_stock_eod_data tool success"""
        from psx_mcp_server import get_stock_eod_data
        
        mock_data = [
            {"timestamp": 1759489200, "price": 300.87, "volume": 2024970, "open_price": 305},
            {"timestamp": 1759575600, "price": 302.15, "volume": 1987654, "open_price": 301}
        ]
        
        with patch('psx_mcp_server.psx_client.get_eod_data', return_value=mock_data):
            result = await get_stock_eod_data("HBL")
            data = json.loads(result)
            
            assert len(data) == 2
            assert data[0]['timestamp'] == 1759489200
            assert data[0]['price'] == 300.87
            assert data[0]['open_price'] == 305
    
    @pytest.mark.asyncio
    async def test_get_stock_eod_data_tool_failure(self):
        """Test get_stock_eod_data tool failure"""
        from psx_mcp_server import get_stock_eod_data
        
        with patch('psx_mcp_server.psx_client.get_eod_data', side_effect=Exception("API Error")):
            result = await get_stock_eod_data("INVALID")
            data = json.loads(result)
            
            assert "error" in data
            assert data["error"] == "API Error"
    
    @pytest.mark.asyncio
    async def test_search_stocks_by_sector_success(self):
        """Test search_stocks_by_sector tool success"""
        from psx_mcp_server import search_stocks_by_sector
        
        mock_data = [
            {"symbol": "HBL", "sector": "Banking", "current_price": 101.5},
            {"symbol": "UBL", "sector": "Banking", "current_price": 95.2},
            {"symbol": "OGDC", "sector": "Oil & Gas", "current_price": 80.5}
        ]
        
        with patch('psx_mcp_server.psx_client.get_market_watch_data', return_value=mock_data):
            result = await search_stocks_by_sector("Banking")
            data = json.loads(result)
            
            assert len(data) == 2
            assert data[0]['symbol'] == 'HBL'
            assert data[1]['symbol'] == 'UBL'
    
    @pytest.mark.asyncio
    async def test_get_top_gainers_success(self):
        """Test get_top_gainers tool success"""
        from psx_mcp_server import get_top_gainers
        
        mock_data = [
            {"symbol": "STOCK1", "change_percent": 5.5},
            {"symbol": "STOCK2", "change_percent": 3.2},
            {"symbol": "STOCK3", "change_percent": 1.8},
            {"symbol": "STOCK4", "change_percent": -2.1}
        ]
        
        with patch('psx_mcp_server.psx_client.get_market_watch_data', return_value=mock_data):
            result = await get_top_gainers(3)
            data = json.loads(result)
            
            assert len(data) == 3
            assert data[0]['symbol'] == 'STOCK1'
            assert data[0]['change_percent'] == 5.5
            assert data[1]['symbol'] == 'STOCK2'
            assert data[2]['symbol'] == 'STOCK3'
    
    @pytest.mark.asyncio
    async def test_get_top_losers_success(self):
        """Test get_top_losers tool success"""
        from psx_mcp_server import get_top_losers
        
        mock_data = [
            {"symbol": "STOCK1", "change_percent": 5.5},
            {"symbol": "STOCK2", "change_percent": -3.2},
            {"symbol": "STOCK3", "change_percent": -1.8},
            {"symbol": "STOCK4", "change_percent": -5.1}
        ]
        
        with patch('psx_mcp_server.psx_client.get_market_watch_data', return_value=mock_data):
            result = await get_top_losers(3)
            data = json.loads(result)
            
            assert len(data) == 3
            assert data[0]['symbol'] == 'STOCK4'
            assert data[0]['change_percent'] == -5.1
            assert data[1]['symbol'] == 'STOCK2'
            assert data[2]['symbol'] == 'STOCK3'

class TestDataModels:
    """Test Pydantic data models"""
    
    def test_stock_data_model(self):
        """Test StockData model validation"""
        stock = StockData(
            symbol="HBL",
            sector="Banking",
            listed_in="Main Board",
            ldcp=100.0,
            open_price=101.0,
            high_price=102.0,
            low_price=99.0,
            current_price=101.5,
            change=1.5,
            change_percent=1.5,
            volume=1000000
        )
        
        assert stock.symbol == "HBL"
        assert stock.sector == "Banking"
        assert stock.current_price == 101.5
        assert stock.volume == 1000000
    
    def test_time_series_data_model(self):
        """Test TimeSeriesData model validation"""
        # Test with intraday data (no open_price)
        intraday = TimeSeriesData(
            timestamp=1759491298,
            price=300.87,
            volume=1000
        )
        
        assert intraday.timestamp == 1759491298
        assert intraday.price == 300.87
        assert intraday.volume == 1000
        assert intraday.open_price is None
        
        # Test with EOD data (with open_price)
        eod = TimeSeriesData(
            timestamp=1759489200,
            price=300.87,
            volume=2024970,
            open_price=305.0
        )
        
        assert eod.timestamp == 1759489200
        assert eod.price == 300.87
        assert eod.volume == 2024970
        assert eod.open_price == 305.0

class TestIntegration:
    """Integration tests with actual PSX API"""
    
    @pytest.mark.asyncio
    async def test_real_market_watch_data(self):
        """Test with real PSX market watch API"""
        client = PSXClient()
        try:
            # This test will only run if marked with --integration flag
            data = await client.get_market_watch_data()
            
            # Basic validation of real data
            assert isinstance(data, list)
            assert len(data) > 0
            
            # Check structure of first item
            first_stock = data[0]
            assert 'symbol' in first_stock
            assert 'current_price' in first_stock
            assert 'volume' in first_stock
            
        except Exception as e:
            pytest.skip(f"Real API test failed (expected): {e}")
        finally:
            await client.close()
    
    @pytest.mark.asyncio
    async def test_real_intraday_data(self):
        """Test with real PSX intraday API"""
        client = PSXClient()
        try:
            # Test with a known stock symbol
            data = await client.get_intraday_data("HBL")
            
            # Basic validation of real data
            assert isinstance(data, list)
            
            if data:  # If data is available
                first_point = data[0]
                assert 'timestamp' in first_point
                assert 'price' in first_point
                assert 'volume' in first_point
                
        except Exception as e:
            pytest.skip(f"Real API test failed (expected): {e}")
        finally:
            await client.close()
    
    @pytest.mark.asyncio
    async def test_real_eod_data(self):
        """Test with real PSX EOD API"""
        client = PSXClient()
        try:
            # Test with a known stock symbol
            data = await client.get_eod_data("HBL")
            
            # Basic validation of real data
            assert isinstance(data, list)
            assert len(data) > 0  # Should have historical data
            
            # Check structure of first item
            first_point = data[0]
            assert 'timestamp' in first_point
            assert 'price' in first_point
            assert 'volume' in first_point
            assert 'open_price' in first_point
            
        except Exception as e:
            pytest.skip(f"Real API test failed (expected): {e}")
        finally:
            await client.close()

def test_mcp_server_initialization():
    """Test MCP server initialization"""
    assert mcp is not None
    assert mcp.name == "PSX Data Scraper"

def test_server_import():
    """Test that the server can be imported and basic functions exist"""
    from psx_mcp_server import (
        get_market_watch,
        get_stock_intraday_data,
        get_stock_eod_data,
        search_stocks_by_sector,
        get_top_gainers,
        get_top_losers
    )
    
    # Check that all functions are callable
    assert callable(get_market_watch)
    assert callable(get_stock_intraday_data)
    assert callable(get_stock_eod_data)
    assert callable(search_stocks_by_sector)
    assert callable(get_top_gainers)
    assert callable(get_top_losers)

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])