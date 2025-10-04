"""
PSX MCP Server - Pakistan Stock Exchange Data Scraper
A Model Context Protocol (MCP) server for accessing PSX market data.
"""

__version__ = "1.0.0"
__author__ = "Ahad Raza"
__description__ = "MCP server for Pakistan Stock Exchange data scraping"

from .server import mcp
from .client import PSXClient

__all__ = ["mcp", "PSXClient"]
