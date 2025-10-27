"""
File management utilities for PDF Telegram Bot.
Handles file downloads, validation, cleanup, and temporary storage.
"""

import os
import time
import uuid
import asyncio
from pathlib import Path
from typing import Optional, List
from telegram import File as TelegramFile

import config


class FileManager:
    """Manages temporary file storage and cleanup for bot operations."""
    
    def __init__(self):
        """Initialize file manager with temp directory."""
        self.temp_dir = config.TEMP_DIR
        self.user_dirs = {}  # Track user-specific temp directories
    
    def get_user_dir(self, user_id: int) -> Path:
        """
        Get or create a temporary directory for a specific user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Path: User's temporary directory path
        """
        if user_id not in self.user_dirs:
            user_dir = self.temp_dir / f"user_{user_id}_{uuid.uuid4().hex[:8]}"
            user_dir.mkdir(parents=True, exist_ok=True)
            self.user_dirs[user_id] = user_dir
        
        return self.user_dirs[user_id]
    
    async def download_file(
        self,
        telegram_file: TelegramFile,
        user_id: int,
        filename: Optional[str] = None
    ) -> Path:
        """
        Download a file from Telegram to user's temp directory.
        
        Args:
            telegram_file: Telegram file object to download
            user_id: User's Telegram ID
            filename: Optional custom filename
            
        Returns:
            Path: Path to downloaded file
            
        Raises:
            ValueError: If file is too large or invalid
        """
        # Validate file size
        if telegram_file.file_size > config.MAX_FILE_SIZE:
            raise ValueError(
                f"File too large! Maximum size is {config.MAX_FILE_SIZE / 1024 / 1024:.1f}MB"
            )
        
        # Generate unique filename if not provided
        if filename is None:
            filename = f"{uuid.uuid4().hex}.tmp"
        
        # Get user directory and create file path
        user_dir = self.get_user_dir(user_id)
        file_path = user_dir / filename
        
        # Download file
        await telegram_file.download_to_drive(str(file_path))
        
        return file_path
    
    def validate_pdf(self, file_path: Path) -> bool:
        """
        Validate that a file is a valid PDF.
        
        Args:
            file_path: Path to file to validate
            
        Returns:
            bool: True if valid PDF, False otherwise
        """
        if not file_path.exists():
            return False
        
        # Check file extension
        if file_path.suffix.lower() != config.SUPPORTED_PDF_FORMAT:
            return False
        
        # Check PDF magic bytes (basic validation)
        try:
            with open(file_path, 'rb') as f:
                header = f.read(5)
                return header == b'%PDF-'
        except Exception:
            return False
    
    def validate_image(self, file_path: Path) -> bool:
        """
        Validate that a file is a supported image format.
        
        Args:
            file_path: Path to file to validate
            
        Returns:
            bool: True if valid image, False otherwise
        """
        if not file_path.exists():
            return False
        
        # Check file extension
        return file_path.suffix.lower() in config.SUPPORTED_IMAGE_FORMATS
    
    def cleanup_user_files(self, user_id: int) -> None:
        """
        Clean up all temporary files for a specific user.
        
        Args:
            user_id: User's Telegram ID
        """
        if user_id in self.user_dirs:
            user_dir = self.user_dirs[user_id]
            
            try:
                # Remove all files in user directory
                if user_dir.exists():
                    for file in user_dir.iterdir():
                        try:
                            if file.is_file():
                                file.unlink()
                            elif file.is_dir():
                                import shutil
                                shutil.rmtree(file)
                        except Exception as e:
                            print(f"Error deleting {file}: {e}")
                    
                    # Remove user directory
                    user_dir.rmdir()
                
                # Remove from tracking
                del self.user_dirs[user_id]
            
            except Exception as e:
                print(f"Error cleaning up user {user_id} files: {e}")
    
    def cleanup_old_files(self, max_age_hours: int = 1) -> None:
        """
        Clean up old temporary files across all users.
        
        Args:
            max_age_hours: Maximum age of files in hours before deletion
        """
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        try:
            for user_dir in self.temp_dir.iterdir():
                if not user_dir.is_dir():
                    continue
                
                # Check directory age
                dir_age = current_time - user_dir.stat().st_mtime
                
                if dir_age > max_age_seconds:
                    try:
                        import shutil
                        shutil.rmtree(user_dir)
                        print(f"Cleaned up old directory: {user_dir.name}")
                    except Exception as e:
                        print(f"Error cleaning up {user_dir}: {e}")
        
        except Exception as e:
            print(f"Error in cleanup_old_files: {e}")
    
    def get_file_size_mb(self, file_path: Path) -> float:
        """
        Get file size in megabytes.
        
        Args:
            file_path: Path to file
            
        Returns:
            float: File size in MB
        """
        if not file_path.exists():
            return 0.0
        
        return file_path.stat().st_size / (1024 * 1024)
    
    def sanitize_filename(self, filename: str) -> str:
        """
        Sanitize a filename to remove potentially dangerous characters.
        
        Args:
            filename: Original filename
            
        Returns:
            str: Sanitized filename
        """
        # Remove or replace dangerous characters
        dangerous_chars = ['/', '\\', '..', '\x00', '\n', '\r']
        sanitized = filename
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Limit filename length
        if len(sanitized) > 200:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:200 - len(ext)] + ext
        
        return sanitized


# Global file manager instance
file_manager = FileManager()


async def cleanup_scheduler():
    """
    Background task to periodically clean up old temporary files.
    Runs every hour to remove files older than 1 hour.
    """
    while True:
        await asyncio.sleep(config.CLEANUP_INTERVAL)
        print("🧹 Running scheduled cleanup...")
        file_manager.cleanup_old_files(max_age_hours=1)
        print("✅ Cleanup completed")
