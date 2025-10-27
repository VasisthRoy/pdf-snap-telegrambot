"""
Merge PDF handler for PDF Telegram Bot.
Handles merging multiple PDF files into one document.
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils import file_manager, pdf_ops, analytics
import config


async def merge_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /merge command - Merge multiple PDFs into one.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    
    # Track user activity
    analytics.track_user(update.effective_user, 'merge')
    
    # Check if user has uploaded PDF files
    pdf_files = context.user_data.get('pdf_files', [])
    
    if len(pdf_files) < 2:
        await update.message.reply_text(
            "⚠️ **Not enough PDFs to merge!**\n\n"
            "Please send at least **2 PDF files** first, then use /merge.\n\n"
            "**Example:**\n"
            "1. Send file1.pdf\n"
            "2. Send file2.pdf\n"
            "3. Type /merge\n\n"
            "💡 You can send up to 20 PDFs to merge!",
            parse_mode='Markdown'
        )
        return
    
    if len(pdf_files) > config.MAX_MERGE_FILES:
        await update.message.reply_text(
            f"⚠️ **Too many files!**\n\n"
            f"Maximum {config.MAX_MERGE_FILES} PDFs can be merged at once.\n"
            f"You sent {len(pdf_files)} files.\n\n"
            f"Please use /cancel and send fewer files.",
            parse_mode='Markdown'
        )
        return
    
    # Show processing message
    processing_msg = await update.message.reply_text(
        f"🔄 **Merging {len(pdf_files)} PDFs...**\n\n"
        "⏳ Please wait, this may take a moment...",
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
        output_path = user_dir / "merged.pdf"
        
        # Merge PDFs
        pdf_ops.merge_pdfs(pdf_files, output_path)
        
        # Get file size
        file_size = file_manager.get_file_size_mb(output_path)
        
        # Update processing message
        await processing_msg.edit_text(
            f"✅ **Merge completed!**\n\n"
            f"📄 Merged {len(pdf_files)} PDFs\n"
            f"📊 Size: {file_size:.2f} MB\n\n"
            f"📤 Sending your file...",
            parse_mode='Markdown'
        )
        
        # Send merged PDF
        with open(output_path, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="merged.pdf",
                caption=f"✨ Here's your merged PDF!\n\n"
                       f"📄 {len(pdf_files)} files combined\n"
                       f"📊 Total size: {file_size:.2f} MB",
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
            "Want to merge more PDFs?\n"
            "Just send new files and use /merge again! 🚀",
            parse_mode='Markdown'
        )
    
    except Exception as e:
        # Handle errors
        error_message = str(e)
        
        await processing_msg.edit_text(
            "❌ **Merge failed!**\n\n"
            f"**Error:** {error_message}\n\n"
            "**Possible reasons:**\n"
            "• One or more PDFs are corrupted\n"
            "• Files are password-protected\n"
            "• Insufficient system resources\n\n"
            "💡 Try:\n"
            "• Use /cancel and upload files again\n"
            "• Check if PDFs are valid\n"
            "• Merge fewer files at once",
            parse_mode='Markdown'
        )
        
        # Clean up on error
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()


async def handle_pdf_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle uploaded PDF files - Store them for later processing.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    document = update.message.document
    
    # Check if it's a PDF file
    if not document.file_name.lower().endswith('.pdf'):
        await update.message.reply_text(
            "⚠️ This doesn't appear to be a PDF file.\n\n"
            "Please send PDF files only.\n"
            "File extension should be **.pdf**",
            parse_mode='Markdown'
        )
        return
    
    # Check file size
    if document.file_size > config.MAX_FILE_SIZE:
        file_size_mb = document.file_size / (1024 * 1024)
        max_size_mb = config.MAX_FILE_SIZE / (1024 * 1024)
        
        await update.message.reply_text(
            f"⚠️ **File too large!**\n\n"
            f"Your file: {file_size_mb:.1f} MB\n"
            f"Maximum: {max_size_mb:.1f} MB\n\n"
            f"💡 Try:\n"
            f"• Compress the PDF first\n"
            f"• Split into smaller files\n"
            f"• Use online compression tools",
            parse_mode='Markdown'
        )
        return
    
    # Show download message
    download_msg = await update.message.reply_text(
        f"📥 **Downloading PDF...**\n\n"
        f"📄 File: {document.file_name}\n"
        f"📊 Size: {document.file_size / (1024 * 1024):.2f} MB",
        parse_mode='Markdown'
    )
    
    try:
        # Download file
        telegram_file = await document.get_file()
        sanitized_filename = file_manager.sanitize_filename(document.file_name)
        file_path = await file_manager.download_file(
            telegram_file,
            user_id,
            sanitized_filename
        )
        
        # Validate PDF
        if not file_manager.validate_pdf(file_path):
            await download_msg.edit_text(
                "❌ **Invalid PDF file!**\n\n"
                "The file appears to be corrupted or not a valid PDF.\n\n"
                "Please try:\n"
                "• Opening the file on your device to check it works\n"
                "• Converting it using another tool\n"
                "• Sending a different file",
                parse_mode='Markdown'
            )
            file_path.unlink()  # Delete invalid file
            return
        
        # Store file path in user data
        if 'pdf_files' not in context.user_data:
            context.user_data['pdf_files'] = []
        
        context.user_data['pdf_files'].append(file_path)
        
        file_count = len(context.user_data['pdf_files'])
        
        # Update message
        await download_msg.edit_text(
            f"✅ **PDF received!**\n\n"
            f"📄 File: {document.file_name}\n"
            f"📊 Size: {document.file_size / (1024 * 1024):.2f} MB\n"
            f"📚 Total PDFs: {file_count}\n\n"
            f"**What's next?**\n"
            f"• Send more PDFs to merge (min 2)\n"
            f"• Use /merge to combine all PDFs\n"
            f"• Use /split <pages> to extract pages\n"
            f"• Use /compress to reduce size\n"
            f"• Use /toimage to convert to images\n"
            f"• Use /cancel to start over",
            parse_mode='Markdown'
        )
    
    except ValueError as e:
        await download_msg.edit_text(
            f"❌ **Download failed!**\n\n"
            f"{str(e)}",
            parse_mode='Markdown'
        )
    
    except Exception as e:
        await download_msg.edit_text(
            "❌ **Something went wrong!**\n\n"
            f"Error: {str(e)}\n\n"
            "Please try again or use /cancel to reset.",
            parse_mode='Markdown'
        )