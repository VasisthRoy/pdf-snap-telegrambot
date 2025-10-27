"""
Convert handler for PDF Telegram Bot.
Handles PDF to images and images to PDF conversions.
"""

import zipfile
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils import file_manager, pdf_ops
import config


async def pdf_to_images_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /toimage, /topng, /tojpg commands - Convert PDF to images.
    
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
            "Please send a PDF file first, then use /toimage.\n\n"
            "**Example:**\n"
            "1. Send your PDF file\n"
            "2. Type /toimage or /topng\n\n"
            "Each page will be converted to a separate image! 🖼️",
            parse_mode='Markdown'
        )
        return
    
    # Check if multiple PDFs uploaded
    if len(pdf_files) > 1:
        await update.message.reply_text(
            "⚠️ **Multiple PDFs detected!**\n\n"
            f"You've uploaded {len(pdf_files)} PDFs.\n"
            f"Conversion works with **one PDF at a time**.\n\n"
            f"Please use /cancel and send only one PDF file.",
            parse_mode='Markdown'
        )
        return
    
    pdf_path = pdf_files[0]
    
    # Get PDF info
    pdf_info = pdf_ops.get_pdf_info(pdf_path)
    page_count = pdf_info['pages']
    
    # Warn if too many pages
    if page_count > 20:
        warning_msg = await update.message.reply_text(
            f"⚠️ **Large PDF detected!**\n\n"
            f"📚 Your PDF has {page_count} pages.\n\n"
            f"Converting many pages may take time and produce many files.\n\n"
            f"**Options:**\n"
            f"• Proceed with conversion (images will be sent as zip)\n"
            f"• Use /split to extract fewer pages first\n"
            f"• Use /cancel to abort\n\n"
            f"⏳ Processing will start in a moment...",
            parse_mode='Markdown'
        )
    
    # Determine image format from command
    command = update.message.text.lower()
    image_format = "PNG"  # Default
    
    if "jpg" in command or "jpeg" in command:
        image_format = "JPEG"
    
    # Show processing message
    processing_msg = await update.message.reply_text(
        f"🔄 **Converting PDF to images...**\n\n"
        f"📄 Pages: {page_count}\n"
        f"🖼️ Format: {image_format}\n\n"
        f"⏳ This may take a moment for large files...",
        parse_mode='Markdown'
    )
    
    # Send typing action
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.UPLOAD_PHOTO
    )
    
    try:
        # Get user directory and create images subdirectory
        user_dir = file_manager.get_user_dir(user_id)
        images_dir = user_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        # Convert PDF to images
        image_paths = pdf_ops.pdf_to_images(pdf_path, images_dir, image_format)
        
        # Update processing message
        await processing_msg.edit_text(
            f"✅ **Conversion completed!**\n\n"
            f"🖼️ Generated {len(image_paths)} images\n\n"
            f"📤 Sending images...",
            parse_mode='Markdown'
        )
        
        # If few pages, send as individual images
        if len(image_paths) <= 10:
            for i, img_path in enumerate(image_paths, 1):
                with open(img_path, 'rb') as img_file:
                    await update.message.reply_photo(
                        photo=img_file,
                        caption=f"📄 Page {i} of {len(image_paths)}"
                    )
        else:
            # Many pages - create zip file
            zip_path = user_dir / "pdf_images.zip"
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for img_path in image_paths:
                    zipf.write(img_path, img_path.name)
            
            zip_size = file_manager.get_file_size_mb(zip_path)
            
            # Send zip file
            with open(zip_path, 'rb') as zip_file:
                await update.message.reply_document(
                    document=zip_file,
                    filename="pdf_images.zip",
                    caption=f"📦 **All images in one ZIP file!**\n\n"
                           f"🖼️ Total images: {len(image_paths)}\n"
                           f"📊 Size: {zip_size:.2f} MB\n"
                           f"📄 Format: {image_format}",
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
            "Want to convert more PDFs to images?\n"
            "Just send a new PDF and use /toimage again! 🚀",
            parse_mode='Markdown'
        )
    
    except Exception as e:
        # Handle errors
        error_message = str(e)
        
        await processing_msg.edit_text(
            "❌ **Conversion failed!**\n\n"
            f"**Error:** {error_message}\n\n"
            "**Possible reasons:**\n"
            "• PDF is corrupted\n"
            "• PDF is password-protected\n"
            "• PDF contains special elements\n"
            "• System resources insufficient\n\n"
            "💡 Try:\n"
            "• Use /cancel and upload file again\n"
            "• Check if PDF opens normally\n"
            "• Try a smaller PDF",
            parse_mode='Markdown'
        )
        
        # Clean up on error
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()


async def images_to_pdf_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /topdf command - Convert images to PDF.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    
    # Check if user has uploaded image files
    image_files = context.user_data.get('image_files', [])
    
    if not image_files:
        await update.message.reply_text(
            "⚠️ **No images found!**\n\n"
            "Please send image files first, then use /topdf.\n\n"
            "**Example:**\n"
            "1. Send image1.jpg\n"
            "2. Send image2.png\n"
            "3. Type /topdf\n\n"
            "**Supported formats:**\n"
            "JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP\n\n"
            "💡 Send at least 1 image to create a PDF!",
            parse_mode='Markdown'
        )
        return
    
    if len(image_files) > config.MAX_IMAGE_FILES:
        await update.message.reply_text(
            f"⚠️ **Too many images!**\n\n"
            f"Maximum {config.MAX_IMAGE_FILES} images can be converted at once.\n"
            f"You sent {len(image_files)} images.\n\n"
            f"Please use /cancel and send fewer images.",
            parse_mode='Markdown'
        )
        return
    
    # Show processing message
    processing_msg = await update.message.reply_text(
        f"🔄 **Converting images to PDF...**\n\n"
        f"🖼️ Total images: {len(image_files)}\n\n"
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
        output_path = user_dir / "images_combined.pdf"
        
        # Convert images to PDF
        pdf_ops.images_to_pdf(image_files, output_path)
        
        # Get file size
        file_size = file_manager.get_file_size_mb(output_path)
        
        # Update processing message
        await processing_msg.edit_text(
            f"✅ **Conversion completed!**\n\n"
            f"📄 PDF created with {len(image_files)} pages\n"
            f"📊 Size: {file_size:.2f} MB\n\n"
            f"📤 Sending your PDF...",
            parse_mode='Markdown'
        )
        
        # Send PDF
        with open(output_path, 'rb') as pdf_file:
            await update.message.reply_document(
                document=pdf_file,
                filename="images_combined.pdf",
                caption=f"✨ Here's your PDF from images!\n\n"
                       f"📄 Pages: {len(image_files)}\n"
                       f"📊 Size: {file_size:.2f} MB\n"
                       f"🖼️ Images converted successfully!",
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
            "Want to create more PDFs from images?\n"
            "Just send new images and use /topdf again! 🚀",
            parse_mode='Markdown'
        )
    
    except Exception as e:
        # Handle errors
        error_message = str(e)
        
        await processing_msg.edit_text(
            "❌ **Conversion failed!**\n\n"
            f"**Error:** {error_message}\n\n"
            "**Possible reasons:**\n"
            "• One or more images are corrupted\n"
            "• Unsupported image format\n"
            "• Insufficient system resources\n\n"
            "💡 Try:\n"
            "• Use /cancel and upload images again\n"
            "• Check if images open normally\n"
            "• Use common formats (JPG, PNG)\n"
            "• Upload fewer images at once",
            parse_mode='Markdown'
        )
        
        # Clean up on error
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()


async def handle_image_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle uploaded image files - Store them for PDF conversion.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    
    # Handle both photo and document uploads
    if update.message.photo:
        # Photo sent as image (compressed by Telegram)
        photo = update.message.photo[-1]  # Get largest size
        telegram_file = await photo.get_file()
        file_name = f"photo_{photo.file_unique_id}.jpg"
        file_size = photo.file_size
    elif update.message.document:
        # Document upload
        document = update.message.document
        
        # Check if it's an image format
        if not any(document.file_name.lower().endswith(ext) for ext in config.SUPPORTED_IMAGE_FORMATS):
            return  # Not an image, ignore
        
        telegram_file = await document.get_file()
        file_name = document.file_name
        file_size = document.file_size
    else:
        return
    
    # Check file size
    if file_size > config.MAX_FILE_SIZE:
        file_size_mb = file_size / (1024 * 1024)
        max_size_mb = config.MAX_FILE_SIZE / (1024 * 1024)
        
        await update.message.reply_text(
            f"⚠️ **Image too large!**\n\n"
            f"Your image: {file_size_mb:.1f} MB\n"
            f"Maximum: {max_size_mb:.1f} MB\n\n"
            f"💡 Try compressing the image first.",
            parse_mode='Markdown'
        )
        return
    
    try:
        # Download image
        sanitized_filename = file_manager.sanitize_filename(file_name)
        file_path = await file_manager.download_file(
            telegram_file,
            user_id,
            sanitized_filename
        )
        
        # Validate image
        if not file_manager.validate_image(file_path):
            await update.message.reply_text(
                "❌ **Invalid image file!**\n\n"
                "The file appears to be corrupted or unsupported.\n\n"
                "**Supported formats:**\n"
                "JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP",
                parse_mode='Markdown'
            )
            file_path.unlink()  # Delete invalid file
            return
        
        # Store file path in user data
        if 'image_files' not in context.user_data:
            context.user_data['image_files'] = []
        
        context.user_data['image_files'].append(file_path)
        
        file_count = len(context.user_data['image_files'])
        
        # Send confirmation
        await update.message.reply_text(
            f"✅ **Image received!**\n\n"
            f"🖼️ File: {file_name}\n"
            f"📊 Size: {file_size / (1024 * 1024):.2f} MB\n"
            f"📚 Total images: {file_count}\n\n"
            f"**What's next?**\n"
            f"• Send more images (up to {config.MAX_IMAGE_FILES})\n"
            f"• Use /topdf to create PDF\n"
            f"• Use /cancel to start over",
            parse_mode='Markdown'
        )
    
    except Exception as e:
        await update.message.reply_text(
            "❌ **Something went wrong!**\n\n"
            f"Error: {str(e)}\n\n"
            "Please try again or use /cancel to reset.",
            parse_mode='Markdown'
        )
