

# PSX MCP Server

Un servidor de Protocolo de Contexto de Modelos (MCP) que proporciona herramientas para extraer y acceder a datos del mercado de la Bolsa de Pakistán (PSX).

## 🎥 Video de demostración

![PSX MCP Server Demo](assets/PSX_MCPServer%20Demo%20-%20Ahad.mov)

*¡Mira esta demostración para ver el servidor PSX MCP en acción con datos del mercado en tiempo real!*

## Características

Este servidor MCP proporciona **12 herramientas poderosas** para un acceso exhaustivo a los datos de PSX:

### 📊 Herramientas básicas (Sencillas e intuitivas)
1. **market_data()** - Obtener datos actuales del mercado para todas las más de 460 acciones listadas en PSX
2. **intraday(symbol)** - Obtener datos de series temporales intradía para una acción específica
3. **history(symbol)** - Obtener datos históricos de cierre para una acción específica (últimos 5 años)
4. **sector(sector)** - Buscar acciones por sector
5. **gainers(limit)** - Obtener las acciones con mayor alza
6. **losers(limit)** - Obtener las acciones con mayor baja

### 🎯 Herramientas avanzadas (Limpias y potentes)
7. **date_range(symbol, start, end)** - Obtener datos de cierre para un rango de fechas específico (formato AAAA-MM-DD)
8. **time_range(symbol, start, end)** - Obtener datos intradía para un rango horario específico (formato AAAA-MM-DD HH:MM:SS)
9. **ohlcv(symbol)** - Obtener datos OHLCV (Apertura, Máxima, Mínima, Cierre, Volumen) para una acción específica
10. **multi_ohlcv(symbols)** - Obtener datos OHLCV para múltiples acciones (símbolos separados por comas)
11. **price_at_time(symbol, timestamp)** - Obtener el dato de precio más cercano en una marca de tiempo Unix específica
12. **volume_analysis(symbol, days)** - Analizar patrones de volumen durante un número específico de días

## Instalación

### Opción 1: Instalación directa
1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar Gemini CLI (copiar y personalizar la plantilla):
```bash
cp gemini_config.template.json gemini_config.json
# Edit gemini_config.json with your project path
```

3. Ejecutar el servidor MCP:
```bash
python scripts/start_server.py
```

### Opción 2: Instalación para desarrollo
1. Instalar con herramientas de desarrollo:
```bash
make setup
# or
pip install -e ".[dev]"
```

2. Ejecutar con Makefile:
```bash
make run-server
```

### Opción 3: Docker
1. Construir la imagen de Docker:
```bash
docker build -t psx-mcp-server .
```

2. Ejecutar el contenedor:
```bash
docker run -it psx-mcp-server
```

## Configuración

### Archivos de plantilla
El proyecto incluye archivos de configuración tipo plantilla para una configuración sencilla:

- **`gemini_config.template.json`** - Plantilla simple de configuración para Gemini CLI
- **`mcp_config.template.json`** - Plantilla avanzada de configuración MCP con ajustes adicionales

### Configuración rápida
1. Copiar el archivo de plantilla:
```bash
cp gemini_config.template.json gemini_config.json
```

2. Editar la configuración con la ruta de tu proyecto:
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

3. Conectar Gemini CLI:
```bash
gemini --config gemini_config.json
```

## Desarrollo

### Comandos disponibles
```bash
make help          # Show all available commands
make test          # Run test suite
make lint          # Run linting checks
make format        # Format code with black
make run-demo      # Run demonstrations
make clean         # Clean build artifacts
```

## Fuentes de datos

El servidor extrae datos de los siguientes puntos finales de PSX:

- `https://dps.psx.com.pk/market-watch` - Datos de vigilancia de mercado
- `https://dps.psx.com.pk/timeseries/int/{SYMBOL}` - Datos intradía
- `https://dps.psx.com.pk/timeseries/eod/{SYMBOL}` - Datos de cierre

## Uso

El servidor se puede utilizar con cualquier cliente MCP, como Gemini CLI. Las herramientas devuelven datos en formato JSON que pueden ser procesados por el cliente.

### Ejemplos de consultas

**Datos básicos (Súper sencillo):**
- "Muéstrame los datos del mercado" → `market_data()`
- "Obtener datos intradía de HBL" → `intraday('HBL')`
- "Mostrar historial de HBL" → `history('HBL')`
- "Encontrar acciones bancarias" → `sector('Banking')`
- "Top 5 con mayor alza" → `gainers(5)`

**Filtrado avanzado (Limpio e intuitivo):**
- "Datos de HBL de enero a febrero" → `date_range('HBL', '2024-01-01', '2024-02-01')`
- "Intradía de HBL de 9AM a 3PM" → `time_range('HBL', '2024-10-04 09:00:00', '2024-10-04 15:00:00')`
- "Datos OHLCV de HBL" → `ohlcv('HBL')`
- "OHLCV para HBL,OGDC" → `multi_ohlcv('HBL,OGDC')`
- "Análisis de volumen de HBL" → `volume_analysis('HBL', 30)`

### Ejemplos de símbolos de acciones

- HBL - Habib Bank Limited
- OGDC - Oil and Gas Development Company
- PTC - Pakistan Telecommunication Company
- LUCK - Lucky Cement
- ENGRO - Engro Corporation

## Modelos de datos

### Datos de acciones
- Símbolo, Sector, Listado en
- LDCP, Apertura, Máxima, Mínima, Precios actuales
- Monto y porcentaje de cambio
- Volumen operado

### Datos de series temporales
- Marca de tiempo Unix
- Precio/Precio de cierre
- Volumen
- Precio de apertura (para datos de cierre)

## Manejo de errores

Todas las herramientas incluyen un manejo adecuado de errores y devuelven mensajes de error en formato JSON si las solicitudes fallan.
