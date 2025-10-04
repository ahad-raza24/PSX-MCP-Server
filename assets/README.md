# Assets

This folder contains media assets for the PSX MCP Server project.

## Contents

- **`demo.mp4`** - Main demo video showing the PSX MCP Server in action
- **`demo.gif`** - Animated GIF version of the demo (optional)
- **`screenshots/`** - Screenshots of the application in use
- **`logos/`** - Project logos and branding materials

## Video Guidelines

### Demo Video Content (2-3 minutes):
1. **Introduction** (15 seconds) - Project overview
2. **Setup** (30 seconds) - Installation and configuration
3. **Live Demo** (90 seconds) - Real PSX data queries
4. **Results** (30 seconds) - Show real market data

### Recommended Format:
- **Resolution**: 1920x1080 (Full HD)
- **Format**: MP4 (H.264 codec)
- **Duration**: 2-3 minutes maximum
- **File Size**: Under 25MB (GitHub limit)

### Sample Demo Script:
```
1. "This is the PSX MCP Server for Pakistan Stock Exchange data"
2. Show installation: pip install -r requirements.txt
3. Show configuration: cp gemini_config.template.json gemini_config.json
4. Start server: python scripts/start_server.py
5. Connect Gemini CLI: gemini --config gemini_config.json
6. Demo queries:
   - "Show me current market data for HBL"
   - "Get top 5 gaining stocks"
   - "Show me banking sector stocks"
7. Show results: 485+ stocks, live prices, OHLCV data
```

## Usage in README

Once you add your video to this folder, update the README.md with:

```markdown
## 🎥 Demo Video

![PSX MCP Server Demo](assets/demo.mp4)

*Watch this demo to see the PSX MCP Server in action with real-time market data!*
```

## File Naming Convention

- `demo.mp4` - Main demo video
- `demo.gif` - Animated GIF version
- `screenshot-01.png` - Setup screenshots
- `screenshot-02.png` - Usage screenshots
- `logo.png` - Project logo
