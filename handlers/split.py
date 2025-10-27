"""
Split PDF handler for PDF Telegram Bot.
Handles extracting specific pages from PDF files.
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils import file_manager, pdf_ops
import config


async def split_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /split command - Extract specific pages from PDF.
    
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
            "Please send a PDF file first, then use /split.\n\n"
            "**Example:**\n"
            "1. Send your PDF file\n"
            "2. Type /split 1-3 (to extract pages 1, 2, 3)\n\n"
            "**Page formats:**\n"
            "• /split 1-3 → Pages 1, 2, 3\n"
            "• /split 1,3,5 → Pages 1, 3, 5\n"
            "• /split 2-end → From page 2 to last page",
            parse_mode='Markdown'
        )
        return
    
    # Check if multiple PDFs uploaded
    if len(pdf_files) > 1:
        await update.message.reply_text(
            "⚠️ **Multiple PDFs detected!**\n\n"
            f"You've uploaded {len(pdf_files)} PDFs.\n"
            f"Split works with **one PDF at a time**.\n\n"
            f"Please use /cancel and send only one PDF file.",
            parse_mode='Markdown'
        )
        return
    
    # Get page specification from command
    command_parts = update.message.text.split(maxsplit=1)
    
    if len(command_parts) < 2:
        # Get PDF info for help message
        pdf_path = pdf_files[0]
        pdf_info = pdf_ops.get_pdf_info(pdf_path)
        
        await update.message.reply_text(
            "⚠️ **Missing page specification!**\n\n"
            f"📄 Your PDF has **{pdf_info['pages']} pages**\n\n"
            "**How to use:**\n"
            "/split <pages>\n\n"
            "**Examples:**\n"
            "• /split 1-3 → Extract pages 1, 2, 3\n"
            "• /split 1,3,5 → Extract pages 1, 3, 5\n"
            "• /split 5-end → From page 5 to last page\n"
            f"• /split 1-{pdf_info['pages']} → All pages\n\n"
            "💡 Mix formats: /split 1-3,5,7-end",
            parse_mode='Markdown'
        )
        return
    
    pages_spec = command_parts[1].strip()
    pdf_path = pdf_files[0]
    
    # Get PDF info
    pdf_info = pdf_ops.get_pdf_info(pdf_path)
    
    # Show processing message
    processing_msg = await update.message.reply_text(
        f"🔄 **Extracting pages...**\n\n"
        f"📄 Pages to extract: {pages_spec}\n"
        f"📚 Total pages in PDF: {pdf_info['pages']}\n\n"
        f"⏳ Please wait...",
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
        output_path = user_dir / "extracted.pdf"
        
        # Split PDF
        success, pages_extracted = pdf_ops.split_pdf(pdf_path, pages_spec, output_path)
        
        # Get file size
        file_size = file_manager.get_file_size_mb(output_path)
        
        # Update processing message
        await processing_msg.edit_text(
            f"✅ **Extraction completed!**\n\n"
            f"📄 Pages extracted: {pages_extracted}\n"
            f"📊 Size: {file_size:.2f} MB\n\n"
            f"📤 Sending your file...",
            parse_mode='Markdown'
        )
        
        # Send extracted PDF
        with open(output_path, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="extracted_pages.pdf",
                caption=f"✨ Here are your extracted pages!\n\n"
                       f"📄 Pages: {pages_spec}\n"
                       f"📚 Total pages: {pages_extracted}\n"
                       f"📊 Size: {file_size:.2f} MB",
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
            "Want to extract more pages?\n"
            "Just send a new PDF and use /split again! 🚀",
            parse_mode='Markdown'
        )
    
    except ValueError as e:
        # Handle invalid page specification
        error_message = str(e)
        
        await processing_msg.edit_text(
            "❌ **Invalid page specification!**\n\n"
            f"**Error:** {error_message}\n\n"
            f"📚 Your PDF has {pdf_info['pages']} pages.\n\n"
            "**Valid formats:**\n"
            "• /split 1-3 → Pages 1, 2, 3\n"
            "• /split 1,3,5 → Pages 1, 3, 5\n"
            "• /split 2-end → Page 2 to last page\n\n"
            "💡 Make sure page numbers are within range!",
            parse_mode='Markdown'
        )
    
    except Exception as e:
        # Handle other errors
        error_message = str(e)
        
        await processing_msg.edit_text(
            "❌ **Extraction failed!**\n\n"
            f"**Error:** {error_message}\n\n"
            "**Possible reasons:**\n"
            "• PDF is corrupted\n"
            "• PDF is password-protected\n"
            "• Invalid page range\n\n"
            "💡 Try:\n"
            "• Use /cancel and upload file again\n"
            "• Check if PDF opens normally\n"
            "• Verify page numbers",
            parse_mode='Markdown'
        )
        
        # Clean up on error
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()
