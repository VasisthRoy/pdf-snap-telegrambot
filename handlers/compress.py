"""
Compress PDF handler for PDF Telegram Bot.
Handles PDF compression to reduce file size with flexible compression targets.
"""

import re
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction

from utils import file_manager, pdf_ops, analytics
import config


def parse_compression_target(text: str) -> dict:
    """
    Parse user's compression target from command text.
    
    Args:
        text: Command text (e.g., "/compress 50%", "/compress 2mb", "/compress low")
        
    Returns:
        dict: {
            'type': 'percentage'|'size'|'quality',
            'value': float or str,
            'unit': 'percent'|'mb'|'kb'|None
        }
    """
    # Remove command and clean up
    parts = text.lower().strip().split(maxsplit=1)
    
    if len(parts) < 2:
        # No parameter, use default quality
        return {'type': 'quality', 'value': 'default', 'unit': None}
    
    target = parts[1].strip()
    
    # Check for percentage (e.g., "50%", "50 %", "50 percent")
    percent_match = re.match(r'(\d+(?:\.\d+)?)\s*(?:%|percent)', target)
    if percent_match:
        percent = float(percent_match.group(1))
        if 10 <= percent <= 90:  # Reasonable range
            return {'type': 'percentage', 'value': percent, 'unit': 'percent'}
        else:
            return {'type': 'error', 'value': f'Percentage must be between 10% and 90%, got {percent}%'}
    
    # Check for file size (e.g., "2mb", "500kb", "1.5 MB")
    size_match = re.match(r'(\d+(?:\.\d+)?)\s*(mb|kb|m|k)', target)
    if size_match:
        size_value = float(size_match.group(1))
        unit = size_match.group(2)
        
        # Convert to MB for consistency
        if unit in ['kb', 'k']:
            size_mb = size_value / 1024
        else:
            size_mb = size_value
        
        if 0.1 <= size_mb <= 50:  # Reasonable range
            return {'type': 'size', 'value': size_mb, 'unit': 'mb'}
        else:
            return {'type': 'error', 'value': f'Target size must be between 0.1MB and 50MB'}
    
    # Check for quality level (low, default, high)
    if target in config.COMPRESSION_LEVELS:
        return {'type': 'quality', 'value': target, 'unit': None}
    
    # Invalid format
    return {'type': 'error', 'value': f'Invalid format: {target}'}


async def compress_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /compress command - Compress PDF to reduce file size.
    
    Supports multiple compression targets:
    - Quality levels: /compress low, /compress default, /compress high
    - Percentage: /compress 50% (compress to 50% of original size)
    - Target size: /compress 2mb, /compress 500kb
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    
    # Track user activity
    analytics.track_user(update.effective_user, 'compress')
    
    # Check if user has uploaded PDF file
    pdf_files = context.user_data.get('pdf_files', [])
    
    if not pdf_files:
        await update.message.reply_text(
            "⚠️ **No PDF found!**\n\n"
            "Please send a PDF file first, then use /compress.\n\n"
            "**Examples:**\n"
            "• /compress → Default compression\n"
            "• /compress low → Maximum compression\n"
            "• /compress high → Better quality\n"
            "• /compress 50% → Reduce to 50% of size\n"
            "• /compress 2mb → Compress to 2MB\n"
            "• /compress 500kb → Compress to 500KB\n\n"
            "💡 Try different options to find the best balance!",
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
    
    # Parse compression target
    target = parse_compression_target(update.message.text)
    
    if target['type'] == 'error':
        await update.message.reply_text(
            f"⚠️ **{target['value']}**\n\n"
            "**Valid compression options:**\n\n"
            "**Quality levels:**\n"
            "• /compress low → Maximum compression\n"
            "• /compress default → Balanced\n"
            "• /compress high → Better quality\n\n"
            "**Percentage:**\n"
            "• /compress 50% → Reduce to 50% of original\n"
            "• /compress 30% → Reduce to 30% of original\n"
            "• Range: 10% to 90%\n\n"
            "**Target size:**\n"
            "• /compress 2mb → Compress to 2MB\n"
            "• /compress 500kb → Compress to 500KB\n"
            "• Range: 0.1MB to 50MB\n\n"
            "💡 Smaller targets = more compression = lower quality",
            parse_mode='Markdown'
        )
        return
    
    pdf_path = pdf_files[0]
    
    # Get original PDF info
    original_size = file_manager.get_file_size_mb(pdf_path)
    pdf_info = pdf_ops.get_pdf_info(pdf_path)
    
    # Validate target size vs original size
    if target['type'] == 'size' and target['value'] >= original_size:
        await update.message.reply_text(
            f"⚠️ **Target size too large!**\n\n"
            f"📄 Your PDF: {original_size:.2f} MB\n"
            f"🎯 Target: {target['value']:.2f} MB\n\n"
            f"Target size must be smaller than original!\n\n"
            f"**Try:**\n"
            f"• /compress 50% → Half the size\n"
            f"• /compress {(original_size * 0.5):.1f}mb → Half size\n"
            f"• /compress low → Maximum compression",
            parse_mode='Markdown'
        )
        return
    
    # Format target description for user
    if target['type'] == 'quality':
        target_desc = f"Quality: {target['value']}"
    elif target['type'] == 'percentage':
        target_size = original_size * (target['value'] / 100)
        target_desc = f"{target['value']}% (target: ~{target_size:.2f} MB)"
    else:  # size
        target_desc = f"Target size: {target['value']:.2f} MB"
    
    # Show processing message
    processing_msg = await update.message.reply_text(
        f"🗜️ **Compressing PDF...**\n\n"
        f"📄 **Before compression:**\n"
        f"   Size: {original_size:.2f} MB\n"
        f"   Pages: {pdf_info['pages']}\n\n"
        f"🎯 **Target:** {target_desc}\n\n"
        f"⏳ Processing... This may take a moment...",
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
        
        # Compress PDF based on target type
        success, original_size_mb, compressed_size_mb = pdf_ops.compress_pdf_advanced(
            pdf_path,
            output_path,
            target
        )
        
        # Calculate compression ratio
        if compressed_size_mb > 0:
            compression_ratio = ((original_size_mb - compressed_size_mb) / original_size_mb) * 100
            size_saved = original_size_mb - compressed_size_mb
        else:
            compression_ratio = 0
            size_saved = 0
        
        # Determine if compression was effective
        if compressed_size_mb >= original_size_mb * 0.98:  # Less than 2% reduction
            # Compression didn't reduce size significantly
            await processing_msg.edit_text(
                "ℹ️ **Compression completed, but minimal reduction**\n\n"
                f"📊 **Before:** {original_size_mb:.2f} MB\n"
                f"📊 **After:** {compressed_size_mb:.2f} MB\n"
                f"📉 **Reduced by:** {compression_ratio:.1f}% ({size_saved:.2f} MB saved)\n\n"
                "Your PDF is already well-optimized! ✨\n\n"
                "**Why minimal compression:**\n"
                "• PDF already compressed efficiently\n"
                "• Mostly text content (compresses less)\n"
                "• Already using optimal settings\n\n"
                "Sending you the best version available...",
                parse_mode='Markdown'
            )
            
            # Send the better version (or original if no improvement)
            if compressed_size_mb < original_size_mb:
                result_path = output_path
                result_msg = f"Slightly compressed: {compressed_size_mb:.2f} MB"
            else:
                result_path = pdf_path
                result_msg = f"Original (already optimized): {original_size_mb:.2f} MB"
            
            with open(result_path, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename="optimized.pdf",
                    caption=f"📄 {result_msg}\n"
                           f"📚 Pages: {pdf_info['pages']}",
                    parse_mode='Markdown'
                )
        else:
            # Successful compression
            # Check if target was met
            target_met_emoji = "✅"
            target_met_text = "Target met!"
            
            if target['type'] == 'percentage':
                expected_size = original_size_mb * (target['value'] / 100)
                diff_percent = abs(compressed_size_mb - expected_size) / expected_size * 100
                if diff_percent > 15:  # More than 15% off target
                    target_met_emoji = "~"
                    target_met_text = "Close to target"
            elif target['type'] == 'size':
                diff_percent = abs(compressed_size_mb - target['value']) / target['value'] * 100
                if diff_percent > 15:
                    target_met_emoji = "~"
                    target_met_text = "Close to target"
            
            await processing_msg.edit_text(
                f"{target_met_emoji} **Compression completed successfully!**\n\n"
                f"📊 **Before compression:** {original_size_mb:.2f} MB\n"
                f"📊 **After compression:** {compressed_size_mb:.2f} MB\n"
                f"📉 **Reduced by:** {compression_ratio:.1f}%\n"
                f"💾 **Space saved:** {size_saved:.2f} MB\n"
                f"📚 **Pages:** {pdf_info['pages']}\n\n"
                f"🎯 {target_met_text}\n\n"
                f"📤 Sending your compressed file...",
                parse_mode='Markdown'
            )
            
            # Send compressed PDF
            with open(output_path, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename="compressed.pdf",
                    caption=f"✨ **Compressed PDF Ready!**\n\n"
                           f"📉 Reduced by {compression_ratio:.1f}%\n"
                           f"📊 Before: {original_size_mb:.2f} MB\n"
                           f"📊 After: {compressed_size_mb:.2f} MB\n"
                           f"💾 Saved: {size_saved:.2f} MB\n"
                           f"📚 Pages: {pdf_info['pages']}",
                    parse_mode='Markdown'
                )
        
        # Delete processing message
        await processing_msg.delete()
        
        # Clean up user files
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()
        
        # Send completion message with tips
        await update.message.reply_text(
            "🎉 **All done!**\n\n"
            "**Compression tips:**\n"
            "• Lower % = more compression\n"
            "• Try /compress 50% for half size\n"
            "• Try /compress 1mb for specific size\n"
            "• Try /compress low for maximum compression\n\n"
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
            "• Target size too small to achieve\n"
            "• PDF has special features that resist compression\n"
            "• Ghostscript not installed on server\n\n"
            "💡 **Try:**\n"
            "• Use /cancel and upload file again\n"
            "• Check if PDF opens normally\n"
            "• Try a less aggressive target (higher %)\n"
            "• Try /compress low (quality mode)",
            parse_mode='Markdown'
        )
        
        # Clean up on error
        file_manager.cleanup_user_files(user_id)
        context.user_data.clear()