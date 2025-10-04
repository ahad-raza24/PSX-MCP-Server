"""
Data models for PSX MCP Server
"""

from typing import Optional
from pydantic import BaseModel, Field


class StockData(BaseModel):
    """Model for stock market data"""
    symbol: str = Field(..., description="Stock symbol")
    sector: str = Field(..., description="Sector name")
    listed_in: str = Field(..., description="Board listing")
    ldcp: float = Field(..., description="Last day closing price")
    open_price: float = Field(..., description="Opening price")
    high_price: float = Field(..., description="Highest price")
    low_price: float = Field(..., description="Lowest price")
    current_price: float = Field(..., description="Current price")
    change: float = Field(..., description="Price change")
    change_percent: float = Field(..., description="Price change percentage")
    volume: int = Field(..., description="Volume traded")


class TimeSeriesData(BaseModel):
    """Model for time series data points"""
    timestamp: int = Field(..., description="Unix timestamp")
    price: float = Field(..., description="Price at timestamp")
    volume: int = Field(..., description="Volume at timestamp")
    open_price: Optional[float] = Field(None, description="Opening price (for EOD data)")


class VolumeAnalysis(BaseModel):
    """Model for volume analysis results"""
    symbol: str = Field(..., description="Stock symbol")
    period_days: int = Field(..., description="Analysis period in days")
    data_points: int = Field(..., description="Number of data points")
    volume_stats: dict = Field(..., description="Volume statistics")
    price_stats: dict = Field(..., description="Price statistics")
    latest_data: Optional[dict] = Field(None, description="Latest data point")
