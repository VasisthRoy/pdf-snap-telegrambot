"""
Compress PDF handler for PDF Telegram Bot.
Handles PDF compression to reduce file size.
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils import file_manager, pdf_ops
import config


async def compress_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /compress command - Compress PDF to reduce file size.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    
    # Check if user has uploaded PDF file
    pdf_files = context.user_data.get('pdf_files', [])
    
    if not pdf_files:
        await update.message.reply_text(
            "⚠️ **No PDF found!**\n\n"
            "Please send a PDF file first, then use /compress.\n\n"
            "**Example:**\n"
            "1. Send your PDF file\n"
            "2. Type /compress (default quality)\n\n"
            "**Quality options:**\n"
            "• /compress → Balanced (recommended)\n"
            "• /compress low → Maximum compression\n"
            "• /compress high → Better quality\n\n"
            "💡 Default quality works best for most files!",
            parse_mode='Markdown'
        )
        return
    
    # Check if multiple PDFs uploaded
    if len(pdf_files) > 1:
        await update.message.reply_text(
            "⚠️ **Multiple PDFs detected!**\n\n"
            f"You've uploaded {len(pdf_files)} PDFs.\n"
            f"Compress works with **one PDF at a time**.\n\n"
            f"Please use /cancel and send only one PDF file.",
            parse_mode='Markdown'
        )
        return
    
    # Get quality level from command (default if not specified)
    command_parts = update.message.text.split(maxsplit=1)
    quality = "default"
    
    if len(command_parts) > 1:
        quality_input = command_parts[1].strip().lower()
        
        if quality_input in config.COMPRESSION_LEVELS:
            quality = quality_input
        else:
            await update.message.reply_text(
                "⚠️ **Invalid quality level!**\n\n"
                "**Available options:**\n"
                "• /compress → Default (balanced)\n"
                "• /compress low → Maximum compression\n"
                "• /compress high → Better quality\n\n"
                "💡 Using default quality...",
                parse_mode='Markdown'
            )
            quality = "default"
    
    pdf_path = pdf_files[0]
    
    # Get original PDF info
    original_size = file_manager.get_file_size_mb(pdf_path)
    pdf_info = pdf_ops.get_pdf_info(pdf_path)
    
    # Show processing message
    processing_msg = await update.message.reply_text(
        f"🗜️ **Compressing PDF...**\n\n"
        f"📄 Original size: {original_size:.2f} MB\n"
        f"📚 Pages: {pdf_info['pages']}\n"
        f"⚙️ Quality: {quality}\n\n"
        f"⏳ Please wait, this may take a moment...",
        parse_mode='Markdown'
    )
    
    # Send typing action
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    
    try:
        # Get user directory
        user_dir = file_manager.get_user_dir(user_id)
        output_path = user_dir / "compressed.pdf"
        
        # Compress PDF
        success, original_size_mb, compressed_size_mb = pdf_ops.compress_pdf(
            pdf_path,
            output_path,
            quality
        )
        
        # Calculate compression ratio
        compression_ratio = ((original_size_mb - compressed_size_mb) / original_size_mb) * 100
        
        # Determine if compression was effective
        if compressed_size_mb >= original_size_mb:
            # Compression didn't reduce size
            await processing_msg.edit_text(
                "ℹ️ **Compression completed, but...**\n\n"
                f"📄 Original: {original_size_mb:.2f} MB\n"
                f"📄 Compressed: {compressed_size_mb:.2f} MB\n\n"
                "The compressed file is not smaller than the original.\n"
                "This PDF is already well-optimized! ✨\n\n"
                "I'll send you the original file back.",
                parse_mode='Markdown'
            )
            
            # Send original file
            with open(pdf_path, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename="original.pdf",
                    caption=f"📄 Your PDF is already optimized!\n\n"
                           f"Size: {original_size_mb:.2f} MB\n"
                           f"Pages: {pdf_info['pages']}",
                    parse_mode='Markdown'
                )
        else:
            # Compression successful
            await processing_msg.edit_text(
                f"✅ **Compression completed!**\n\n"
                f"📄 Original: {original_size_mb:.2f} MB\n"
                f"📄 Compressed: {compressed_size_mb:.2f} MB\n"
                f"📉 Reduced by: {compression_ratio:.1f}%\n\n"
                f"📤 Sending your compressed file...",
                parse_mode='Markdown'
            )
            
            # Send compressed PDF
            with open(output_path, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename="compressed.pdf",
                    caption=f"✨ Here's your compressed PDF!\n\n"
                           f"📉 Size reduced by {compression_ratio:.1f}%\n"
                           f"📊 Before: {original_size_mb:.2f} MB\n"
                           f"📊 After: {compressed_size_mb:.2f} MB\n"
                           f"📚 Pages: {pdf_info['pages']}",
                    parse_mode='Markdown'
                )
        
        # Delete processing message
        await processing_msg.delete()
        
        # Clean up user files
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()
        
        # Send completion message
        await update.message.reply_text(
            "🎉 **All done!**\n\n"
            "**Tips for better compression:**\n"
            "• Try different quality levels\n"
            "• /compress low for maximum compression\n"
            "• /compress high for better quality\n\n"
            "Want to compress more PDFs? Just send a new file! 🚀",
            parse_mode='Markdown'
        )
    
    except Exception as e:
        # Handle errors
        error_message = str(e)
        
        await processing_msg.edit_text(
            "❌ **Compression failed!**\n\n"
            f"**Error:** {error_message}\n\n"
            "**Possible reasons:**\n"
            "• PDF is corrupted\n"
            "• PDF is password-protected\n"
            "• PDF has special features that can't be compressed\n\n"
            "💡 Try:\n"
            "• Use /cancel and upload file again\n"
            "• Check if PDF opens normally\n"
            "• Try a different quality level",
            parse_mode='Markdown'
        )
        
        # Clean up on error
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()
