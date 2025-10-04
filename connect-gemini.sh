#!/bin/bash

echo "🚀 Connecting Gemini CLI to PSX MCP Server"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "scripts/start_server.py" ]; then
    echo "❌ Please run this script from the MCP project root directory"
    exit 1
fi

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "✅ Activating virtual environment..."
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found. Please run 'make setup' first"
    exit 1
fi

echo ""
echo "🔧 Starting PSX MCP Server in background..."
echo "Server will be available at: $(pwd)/scripts/start_server.py"
echo ""

# Start the MCP server in background
python scripts/start_server.py &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

echo "✅ MCP Server started with PID: $SERVER_PID"
echo ""
echo "📋 Now you can connect Gemini CLI using:"
echo "gemini --mcp-server $(pwd)/scripts/start_server.py"
echo ""
echo "🧪 Test queries you can try:"
echo "- 'Show me market data for HBL'"
echo "- 'Get top 5 gaining stocks'"
echo "- 'Find all banking sector stocks'"
echo "- 'Get HBL intraday data'"
echo ""
echo "⏹️  To stop the server later, run: kill $SERVER_PID"
