"""
PDF Tools Telegram Bot - Main Application
A comprehensive PDF manipulation bot for Telegram.

Features:
- Merge multiple PDFs
- Split PDFs by page range
- Compress PDFs
- Convert PDF to images
- Convert images to PDF

Author: Your Name
Version: 1.0.0
"""

import asyncio
import logging
import sys
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

import config
from handlers import (
    start_command,
    help_command,
    about_command,
    cancel_command,
    merge_command,
    split_command,
    compress_command,
    pdf_to_images_command,
    images_to_pdf_command,
    handle_pdf_file,
    handle_image_file
)
from utils import cleanup_scheduler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle errors in the bot.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Try to inform user about the error
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ **An unexpected error occurred!**\n\n"
                "The bot encountered an issue while processing your request.\n\n"
                "**What you can do:**\n"
                "• Use /cancel and try again\n"
                "• Restart with /start\n"
                "• Check if your files are valid\n\n"
                "If the problem persists, please report it on GitHub.",
                parse_mode='Markdown'
            )
        except Exception:
            pass


async def post_init(application: Application) -> None:
    """
    Post-initialization function to set bot commands.
    
    Args:
        application: Telegram application object
    """
    # Set bot commands for better UX in Telegram
    commands = [
        ("start", "Start the bot and see welcome message"),
        ("help", "Show detailed help and usage guide"),
        ("merge", "Merge multiple PDFs into one"),
        ("split", "Extract specific pages from PDF"),
        ("compress", "Reduce PDF file size"),
        ("toimage", "Convert PDF pages to images"),
        ("topdf", "Convert images to PDF"),
        ("cancel", "Cancel current operation"),
        ("about", "Bot information and credits")
    ]
    
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands set successfully")


def main() -> None:
    """
    Main function to start the bot.
    """
    # Validate configuration
    if not config.validate_config():
        logger.error("Configuration validation failed!")
        sys.exit(1)
    
    logger.info(f"Starting {config.BOT_NAME} v{config.BOT_VERSION}...")
    
    # Create the Application
    application = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    
    # PDF operation handlers
    application.add_handler(CommandHandler("merge", merge_command))
    application.add_handler(CommandHandler("split", split_command))
    application.add_handler(CommandHandler("compress", compress_command))
    
    # Conversion handlers (multiple command aliases)
    application.add_handler(CommandHandler("toimage", pdf_to_images_command))
    application.add_handler(CommandHandler("topng", pdf_to_images_command))
    application.add_handler(CommandHandler("tojpg", pdf_to_images_command))
    application.add_handler(CommandHandler("topdf", images_to_pdf_command))
    
    # File handlers
    application.add_handler(
        MessageHandler(
            filters.Document.PDF,
            handle_pdf_file
        )
    )
    
    application.add_handler(
        MessageHandler(
            filters.PHOTO | filters.Document.IMAGE,
            handle_image_file
        )
    )
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Create cleanup task
    async def startup_cleanup():
        """Start the cleanup scheduler on bot startup."""
        asyncio.create_task(cleanup_scheduler())
        logger.info("Cleanup scheduler started")
    
    # Schedule cleanup task
    application.post_init = startup_cleanup
    
    # Start the bot
    logger.info("Bot is starting... Press Ctrl+C to stop.")
    logger.info(f"Bot name: {config.BOT_NAME}")
    logger.info(f"Version: {config.BOT_VERSION}")
    
    # Run the bot until Ctrl+C
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True  # Ignore old updates on restart
    )
    
    logger.info("Bot stopped.")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
