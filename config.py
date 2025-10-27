"""
Configuration management for PDF Telegram Bot.
Handles environment variables and bot settings.
"""

import os
from pathlib import Path
from typing import Final

# Bot Configuration
BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN", "")

# File Size Limits (in bytes)
MAX_FILE_SIZE: Final[int] = 50 * 1024 * 1024  # 50MB (Telegram limit)
MAX_MERGE_FILES: Final[int] = 20  # Maximum files to merge at once
MAX_IMAGE_FILES: Final[int] = 50  # Maximum images to convert at once

# Compression Quality Settings
COMPRESSION_LEVELS: Final[dict] = {
    "low": "/screen",      # Maximum compression (72 dpi)
    "default": "/ebook",   # Balanced (150 dpi)
    "high": "/printer"     # Minimal compression (300 dpi)
}

# Temporary Storage
TEMP_DIR: Final[Path] = Path("/tmp/pdf_bot_temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Operation Timeouts (in seconds)
OPERATION_TIMEOUT: Final[int] = 300  # 5 minutes max per operation
CLEANUP_INTERVAL: Final[int] = 3600  # Clean temp files every hour

# Rate Limiting (basic)
MAX_OPERATIONS_PER_MINUTE: Final[int] = 10

# Supported File Formats
SUPPORTED_IMAGE_FORMATS: Final[tuple] = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
SUPPORTED_PDF_FORMAT: Final[str] = '.pdf'

# Bot Information
BOT_NAME: Final[str] = "PDF Tools Bot"
BOT_VERSION: Final[str] = "1.0.0"
BOT_DESCRIPTION: Final[str] = "Free PDF manipulation tools in Telegram"
DEVELOPER: Final[str] = "Your Name"
GITHUB_REPO: Final[str] = "https://github.com/yourusername/pdf-telegram-bot"

# Feature Flags
ENABLE_ANALYTICS: Final[bool] = False  # For future implementation
ENABLE_RATE_LIMITING: Final[bool] = True
ENABLE_ADMIN_PANEL: Final[bool] = False  # For future implementation

def validate_config() -> bool:
    """
    Validate that all required configuration is present.
    
    Returns:
        bool: True if config is valid, False otherwise
    """
    if not BOT_TOKEN:
        print("❌ ERROR: BOT_TOKEN not found in environment variables!")
        print("Please set BOT_TOKEN in your .env file or environment.")
        return False
    
    if not TEMP_DIR.exists():
        try:
            TEMP_DIR.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"❌ ERROR: Cannot create temp directory: {e}")
            return False
    
    return True

def get_bot_info() -> dict:
    """
    Get bot information for /about command.
    
    Returns:
        dict: Bot information
    """
    return {
        "name": BOT_NAME,
        "version": BOT_VERSION,
        "description": BOT_DESCRIPTION,
        "developer": DEVELOPER,
        "repo": GITHUB_REPO
    }
