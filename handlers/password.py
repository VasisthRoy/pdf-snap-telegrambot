"""
Password handler for PDF Telegram Bot.
Handles adding and removing password protection from PDF files.
"""

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils import file_manager, pdf_ops, analytics
import config


async def protect_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /protect command - Add password protection to PDF.
    
    Usage: /protect <password>
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    
    # Track user activity
    analytics.track_user(update.effective_user, 'protect')
    
    # Check if user has uploaded PDF file
    pdf_files = context.user_data.get('pdf_files', [])
    
    if not pdf_files:
        await update.message.reply_text(
            "⚠️ **No PDF found!**\n\n"
            "Please send a PDF file first, then use /protect.\n\n"
            "**Example:**\n"
            "1. Send your PDF file\n"
            "2. Type /protect MyPassword123\n\n"
            "**Password tips:**\n"
            "• Use strong passwords (8+ characters)\n"
            "• Mix letters, numbers, and symbols\n"
            "• Avoid common words\n\n"
            "💡 Remember your password - you'll need it to open the PDF!",
            parse_mode='Markdown'
        )
        return
    
    # Check if multiple PDFs uploaded
    if len(pdf_files) > 1:
        await update.message.reply_text(
            "⚠️ **Multiple PDFs detected!**\n\n"
            f"You've uploaded {len(pdf_files)} PDFs.\n"
            f"Protection works with **one PDF at a time**.\n\n"
            f"Please use /cancel and send only one PDF file.",
            parse_mode='Markdown'
        )
        return
    
    # Get password from command
    command_parts = update.message.text.split(maxsplit=1)
    
    if len(command_parts) < 2:
        await update.message.reply_text(
            "⚠️ **Missing password!**\n\n"
            "**How to use:**\n"
            "/protect <password>\n\n"
            "**Examples:**\n"
            "• /protect MySecretPass123\n"
            "• /protect Company@2024\n"
            "• /protect MyP@ssw0rd!\n\n"
            "**Password requirements:**\n"
            "• Minimum 4 characters\n"
            "• Can include letters, numbers, symbols\n"
            "• No spaces recommended\n\n"
            "💡 **Important:** Remember this password!\n"
            "You'll need it to open the PDF.",
            parse_mode='Markdown'
        )
        return
    
    password = command_parts[1].strip()
    
    # Validate password
    if len(password) < 4:
        await update.message.reply_text(
            "⚠️ **Password too short!**\n\n"
            "Password must be at least **4 characters** long.\n\n"
            "Please use a stronger password for better security.",
            parse_mode='Markdown'
        )
        return
    
    if len(password) > 128:
        await update.message.reply_text(
            "⚠️ **Password too long!**\n\n"
            "Password must be less than **128 characters**.\n\n"
            "Please use a shorter password.",
            parse_mode='Markdown'
        )
        return
    
    pdf_path = pdf_files[0]
    
    # Get original PDF info
    pdf_info = pdf_ops.get_pdf_info(pdf_path)
    original_size = file_manager.get_file_size_mb(pdf_path)
    
    # Check if PDF is already encrypted
    if pdf_info['encrypted']:
        await update.message.reply_text(
            "⚠️ **PDF is already password-protected!**\n\n"
            "This PDF already has password protection.\n\n"
            "**To change the password:**\n"
            "1. Use /unlock to remove current password\n"
            "2. Then use /protect with new password\n\n"
            "💡 You'll need the current password to unlock it.",
            parse_mode='Markdown'
        )
        return
    
    # Show processing message
    processing_msg = await update.message.reply_text(
        f"🔐 **Adding password protection...**\n\n"
        f"📄 **PDF Info:**\n"
        f"   Pages: {pdf_info['pages']}\n"
        f"   Size: {original_size:.2f} MB\n\n"
        f"🔒 Encrypting with your password...\n"
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
        output_path = user_dir / "protected.pdf"
        
        # Add password protection
        pdf_ops.protect_pdf(pdf_path, output_path, password)
        
        # Get file size
        protected_size = file_manager.get_file_size_mb(output_path)
        
        # Update processing message
        await processing_msg.edit_text(
            f"✅ **Password protection added!**\n\n"
            f"📄 Pages: {pdf_info['pages']}\n"
            f"📊 Size: {protected_size:.2f} MB\n"
            f"🔒 Password: {'*' * len(password)}\n\n"
            f"📤 Sending your protected file...",
            parse_mode='Markdown'
        )
        
        # Send protected PDF
        with open(output_path, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="protected.pdf",
                caption=f"🔒 **Your PDF is now password-protected!**\n\n"
                       f"📄 Pages: {pdf_info['pages']}\n"
                       f"📊 Size: {protected_size:.2f} MB\n\n"
                       f"⚠️ **IMPORTANT:**\n"
                       f"• Save your password in a secure place\n"
                       f"• You'll need it to open this PDF\n"
                       f"• Cannot be recovered if forgotten\n\n"
                       f"💡 Password length: {len(password)} characters",
                parse_mode='Markdown'
            )
        
        # Delete the message containing the password for security
        try:
            await update.message.delete()
        except:
            pass  # User might have disabled message deletion
        
        # Delete processing message
        await processing_msg.delete()
        
        # Clean up user files
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()
        
        # Send completion message
        await update.message.reply_text(
            "🎉 **All done!**\n\n"
            "Your PDF is now securely protected.\n\n"
            "**Security Tips:**\n"
            "• Store your password safely\n"
            "• Use different passwords for different files\n"
            "• Share password separately from the file\n\n"
            "Want to protect more PDFs? Send a new file! 🚀",
            parse_mode='Markdown'
        )
    
    except Exception as e:
        # Handle errors
        error_message = str(e)
        
        await processing_msg.edit_text(
            "❌ **Protection failed!**\n\n"
            f"**Error:** {error_message}\n\n"
            "**Possible reasons:**\n"
            "• PDF is corrupted\n"
            "• PDF has restrictions that prevent encryption\n"
            "• Insufficient system resources\n\n"
            "💡 **Try:**\n"
            "• Use /cancel and upload file again\n"
            "• Check if PDF opens normally\n"
            "• Try a different PDF file",
            parse_mode='Markdown'
        )
        
        # Clean up on error
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()


async def unlock_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /unlock command - Remove password protection from PDF.
    
    Usage: /unlock <password>
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    
    # Track user activity
    analytics.track_user(update.effective_user, 'unlock')
    
    # Check if user has uploaded PDF file
    pdf_files = context.user_data.get('pdf_files', [])
    
    if not pdf_files:
        await update.message.reply_text(
            "⚠️ **No PDF found!**\n\n"
            "Please send a password-protected PDF file first, then use /unlock.\n\n"
            "**Example:**\n"
            "1. Send your protected PDF file\n"
            "2. Type /unlock YourPassword123\n\n"
            "💡 You need the correct password to unlock the PDF!",
            parse_mode='Markdown'
        )
        return
    
    # Check if multiple PDFs uploaded
    if len(pdf_files) > 1:
        await update.message.reply_text(
            "⚠️ **Multiple PDFs detected!**\n\n"
            f"You've uploaded {len(pdf_files)} PDFs.\n"
            f"Unlock works with **one PDF at a time**.\n\n"
            f"Please use /cancel and send only one PDF file.",
            parse_mode='Markdown'
        )
        return
    
    # Get password from command
    command_parts = update.message.text.split(maxsplit=1)
    
    if len(command_parts) < 2:
        await update.message.reply_text(
            "⚠️ **Missing password!**\n\n"
            "**How to use:**\n"
            "/unlock <password>\n\n"
            "**Examples:**\n"
            "• /unlock MySecretPass123\n"
            "• /unlock Company@2024\n\n"
            "💡 You must provide the correct password\n"
            "that was used to protect this PDF.",
            parse_mode='Markdown'
        )
        return
    
    password = command_parts[1].strip()
    pdf_path = pdf_files[0]
    
    # Get original PDF info (will fail if password is wrong)
    original_size = file_manager.get_file_size_mb(pdf_path)
    
    # Show processing message
    processing_msg = await update.message.reply_text(
        f"🔓 **Removing password protection...**\n\n"
        f"📊 Size: {original_size:.2f} MB\n\n"
        f"🔐 Verifying password...\n"
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
        output_path = user_dir / "unlocked.pdf"
        
        # Remove password protection
        pdf_ops.unlock_pdf(pdf_path, output_path, password)
        
        # Get PDF info after unlocking
        pdf_info = pdf_ops.get_pdf_info(output_path)
        unlocked_size = file_manager.get_file_size_mb(output_path)
        
        # Update processing message
        await processing_msg.edit_text(
            f"✅ **Password removed successfully!**\n\n"
            f"📄 Pages: {pdf_info['pages']}\n"
            f"📊 Size: {unlocked_size:.2f} MB\n\n"
            f"📤 Sending your unlocked file...",
            parse_mode='Markdown'
        )
        
        # Send unlocked PDF
        with open(output_path, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="unlocked.pdf",
                caption=f"🔓 **Your PDF is now unlocked!**\n\n"
                       f"📄 Pages: {pdf_info['pages']}\n"
                       f"📊 Size: {unlocked_size:.2f} MB\n\n"
                       f"✅ Password protection removed\n"
                       f"📖 PDF can now be opened without password\n\n"
                       f"💡 Want to protect it again? Use /protect",
                parse_mode='Markdown'
            )
        
        # Delete the message containing the password for security
        try:
            await update.message.delete()
        except:
            pass  # User might have disabled message deletion
        
        # Delete processing message
        await processing_msg.delete()
        
        # Clean up user files
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()
        
        # Send completion message
        await update.message.reply_text(
            "🎉 **All done!**\n\n"
            "Your PDF is now accessible without a password.\n\n"
            "Want to unlock more PDFs? Send a new file! 🚀",
            parse_mode='Markdown'
        )
    
    except ValueError as e:
        # Wrong password error
        await processing_msg.edit_text(
            "❌ **Incorrect password!**\n\n"
            "The password you provided is incorrect.\n\n"
            "**Please try again:**\n"
            "1. Check your password (case-sensitive)\n"
            "2. Make sure there are no extra spaces\n"
            "3. Use /unlock <correct_password>\n\n"
            "💡 If you forgot the password, you cannot unlock this PDF.",
            parse_mode='Markdown'
        )
        
        # Don't clean up files - let user try again
    
    except Exception as e:
        # Handle other errors
        error_message = str(e)
        
        await processing_msg.edit_text(
            "❌ **Unlock failed!**\n\n"
            f"**Error:** {error_message}\n\n"
            "**Possible reasons:**\n"
            "• Incorrect password\n"
            "• PDF is corrupted\n"
            "• PDF is not password-protected\n"
            "• PDF uses unsupported encryption\n\n"
            "💡 **Try:**\n"
            "• Verify the password is correct\n"
            "• Check if PDF is actually protected\n"
            "• Try opening PDF in a PDF reader first",
            parse_mode='Markdown'
        )
        
        # Clean up on error
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()