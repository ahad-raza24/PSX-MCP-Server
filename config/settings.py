"""
Configuration settings for PSX MCP Server
"""

import os
from typing import Optional


class Settings:
    """Configuration settings"""
    
    # PSX API Configuration
    PSX_BASE_URL: str = "https://dps.psx.com.pk"
    REQUEST_TIMEOUT: int = 30
    
    # Server Configuration
    SERVER_NAME: str = "PSX Data Scraper"
    SERVER_VERSION: str = "1.0.0"
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 100
    RATE_LIMIT_WINDOW: int = 60
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Data Configuration
    DEFAULT_DATE_FORMAT: str = "%Y-%m-%d"
    DEFAULT_DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    MAX_HISTORICAL_DAYS: int = 1825  # 5 years
    
    @classmethod
    def get_env_var(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        """Get environment variable with optional default"""
        return os.getenv(key, default)


# Global settings instance
settings = Settings()
