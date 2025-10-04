#!/usr/bin/env python3
"""
Start script for PSX MCP Server
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from psx_mcp.server import mcp  # noqa: E402


def main():
    """Start the MCP server"""
    print("🚀 Starting PSX MCP Server...")
    print(f"📍 Server: {mcp.name}")
    print("🔧 Available tools: 12")
    print("📊 Data source: Pakistan Stock Exchange")
    print("-" * 50)

    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
