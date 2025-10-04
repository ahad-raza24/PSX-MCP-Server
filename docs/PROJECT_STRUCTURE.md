# PSX MCP Server - Project Structure

## Overview

This document describes the organized project structure for the PSX MCP Server, a comprehensive Model Context Protocol server for Pakistan Stock Exchange data access.

## Directory Structure

```
psx-mcp-server/
├── 📁 src/psx_mcp/          # Main source code
├── 📁 tests/                # Test suite
├── 📁 examples/             # Usage examples and demos
├── 📁 docs/                 # Documentation
├── 📁 config/               # Configuration files
├── 📁 scripts/              # Utility scripts
├── 📄 setup.py              # Package setup
├── 📄 pyproject.toml        # Modern Python project config
├── 📄 Makefile              # Development commands
└── 📄 README.md             # Project documentation
```

## Source Code (`src/psx_mcp/`)

### Core Modules

- **`__init__.py`** - Package initialization and exports
- **`server.py`** - Main MCP server with FastMCP integration
- **`client.py`** - PSX API client for data fetching
- **`models.py`** - Pydantic data models (StockData, TimeSeriesData, etc.)
- **`tools.py`** - All 12 MCP tools implementation

### Key Features

- **12 MCP Tools** with simple, intuitive names
- **Modular Architecture** - separated concerns
- **Type Safety** - Pydantic models with validation
- **Error Handling** - comprehensive error management
- **Async Support** - full async/await implementation

## Test Suite (`tests/`)

### Test Files

- **`test_psx_mcp_server.py`** - Comprehensive test suite (23 tests)
- **`simple_test.py`** - Quick functionality verification
- **`test_psx_endpoints.py`** - PSX API endpoint testing

### Test Coverage

- ✅ PSXClient functionality
- ✅ Data model validation
- ✅ MCP tool integration
- ✅ Real API endpoint testing
- ✅ Error handling scenarios

## Examples (`examples/`)

### Demo Scripts

- **`demo_mcp_server.py`** - Basic server functionality demo
- **`demo_new_tools.py`** - Advanced tools demonstration
- **`demo_simple_names.py`** - Simplified naming showcase

### Usage Patterns

- Natural language query examples
- Tool name mapping demonstrations
- Real-time data fetching examples

## Documentation (`docs/`)

### Documentation Files

- **`API.md`** - Complete API documentation
- **`PROJECT_STRUCTURE.md`** - This file

### Documentation Features

- Detailed tool descriptions
- Parameter specifications
- Usage examples
- Data model schemas
- Error handling guide

## Configuration (`config/`)

### Configuration Files

- **`settings.py`** - Centralized configuration management

### Configuration Options

- PSX API settings
- Server configuration
- Rate limiting settings
- Logging configuration
- Data format settings

## Scripts (`scripts/`)

### Utility Scripts

- **`start_server.py`** - Production server startup script

### Script Features

- Environment setup
- Path management
- Error handling
- User-friendly output

## Development Tools

### Build System

- **`setup.py`** - Traditional Python package setup
- **`pyproject.toml`** - Modern Python project configuration
- **`Makefile`** - Development commands and automation

### Development Commands

```bash
make install-dev    # Install development dependencies
make test          # Run test suite
make lint          # Code linting
make format        # Code formatting
make run-server    # Start MCP server
make run-demo      # Run demonstrations
```

## Package Structure

### Installation

```bash
# Development installation
pip install -e .

# With development tools
pip install -e ".[dev,test]"
```

### Entry Points

- **`psx-mcp-server`** - Command-line server startup

## Key Benefits

### 1. **Modular Architecture**
- Clear separation of concerns
- Easy to maintain and extend
- Reusable components

### 2. **Professional Structure**
- Industry-standard Python project layout
- Comprehensive testing
- Full documentation

### 3. **Developer Experience**
- Simple Makefile commands
- Automated testing
- Code formatting and linting

### 4. **Production Ready**
- Proper error handling
- Configuration management
- Logging support

### 5. **Extensible Design**
- Easy to add new tools
- Configurable settings
- Plugin-ready architecture

## File Organization Principles

### 1. **Separation of Concerns**
- **Client**: API communication
- **Models**: Data structures
- **Tools**: MCP tool implementations
- **Server**: MCP server setup

### 2. **Testability**
- Isolated test files
- Mock-friendly design
- Comprehensive coverage

### 3. **Documentation**
- Inline documentation
- API documentation
- Usage examples
- Project structure docs

### 4. **Configuration**
- Centralized settings
- Environment variables
- Development vs production configs

## Development Workflow

### 1. **Setup**
```bash
make setup
```

### 2. **Development**
```bash
make run-server    # Start server
make test          # Run tests
make lint          # Check code quality
```

### 3. **Testing**
```bash
make test-cov      # Run with coverage
python tests/simple_test.py  # Quick test
```

### 4. **Documentation**
```bash
# Update docs/API.md
# Update README.md
# Add examples to examples/
```

## Deployment

### Production Deployment

```bash
# Build package
make build

# Install production dependencies
pip install -r requirements.txt

# Start server
python scripts/start_server.py
```

### MCP Client Integration

```bash
# With Gemini CLI
gemini-cli --mcp-server scripts/start_server.py
```

## Conclusion

This project structure provides a professional, maintainable, and extensible foundation for the PSX MCP Server. The modular design makes it easy to add new features, maintain code quality, and deploy in production environments.
