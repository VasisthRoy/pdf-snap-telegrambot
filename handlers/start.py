"""
Start and help command handlers for PDF Telegram Bot.
Provides welcome messages and usage instructions.
"""

from telegram import Update
from telegram.ext import ContextTypes

import config
from utils import analytics


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command - Show welcome message and basic instructions.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_name = update.effective_user.first_name
    
    # Track user activity
    analytics.track_user(update.effective_user, 'start')
    
    welcome_message = f"""
👋 <b>Welcome {user_name}!</b>

I'm <b>{config.BOT_NAME}</b> - Your free PDF manipulation assistant! 🎉

🔧 <b>What I Can Do:</b>
- 📄 Merge multiple PDFs into one
- ✂️ Split PDFs and extract specific pages
- 🗜️ Compress PDFs to reduce file size
- 🖼️ Convert PDFs to images
- 📄 Convert images to PDF

⚡ <b>Quick Start:</b>
1. Send me PDF files or images
2. Use commands below to process them
3. Get your result instantly!
4. Click on any command to learn more about it.

📋 <b>Available Commands:</b>
/merge - Merge multiple PDFs into one
/split - Extract pages (e.g., /split 1-3)
/compress - Reduce PDF file size
/toimage - Convert PDF to images
/topdf - Convert images to PDF
/help - Detailed help and examples
/about - Bot information
/cancel - Cancel current operation
/stats - View bot usage statistics (admin only)

💁🏻‍♀️ For Official Support, Visit @SnapBotHub

💡 <b>Tip:</b> Send me files first, then use the commands!

Need help? Type /help for detailed instructions.

Let's get started! 🚀
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='HTML'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /help command - Show detailed usage instructions.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    # Track user activity
    analytics.track_user(update.effective_user, 'help')
    
    help_message = """
📚 <b>Detailed Help Guide</b>

━━━━━━━━━━━━━━━━━━━━━

<b>1️⃣ MERGE PDFs</b>
Combine multiple PDF files into one document.

<b>How to use:</b>
- Send 2 or more PDF files
- Type: /merge
- Receive merged PDF

<b>Example:</b>
Send: report1.pdf, report2.pdf
Command: /merge
Result: merged.pdf (contains all pages)

<b>Limits:</b>
- Min files: 2
- Max files: 20
- Max size per file: 50MB

━━━━━━━━━━━━━━━━━━━━━

<b>2️⃣ SPLIT PDF</b>
Extract specific pages from a PDF.

<b>How to use:</b>
- Send 1 PDF file
- Type: /split &lt;page_specification&gt;
- Receive extracted pages

<b>Page Specifications:</b>
- Single page: /split 5
- Page range: /split 1-3
- Multiple pages: /split 1,3,5
- From page to end: /split 3-end
- Mix formats: /split 1-3,5,7-end

<b>Examples:</b>
/split 1-3 → Extract pages 1, 2, 3
/split 2,4,6 → Extract pages 2, 4, 6
/split 5-end → Extract from page 5 to last page

━━━━━━━━━━━━━━━━━━━━━

<b>3️⃣ COMPRESS PDF</b>
Reduce PDF file size while maintaining quality.

<b>How to use:</b>
- Send 1 PDF file
- Type: /compress [quality]
- Receive compressed PDF

<b>Quality Levels:</b>
- /compress → Default (balanced)
- /compress low → Maximum compression
- /compress high → Better quality, less compression

<b>Example:</b>
Send: large_document.pdf (10MB)
Command: /compress
Result: compressed.pdf (3-5MB typically)

━━━━━━━━━━━━━━━━━━━━━

<b>4️⃣ PDF TO IMAGES</b>
Convert each PDF page to an image file.

<b>How to use:</b>
- Send 1 PDF file
- Type: /toimage, /topng, or /tojpg
- Receive images (PNG format default)

<b>Example:</b>
Send: presentation.pdf (5 pages)
Command: /toimage
Result: 5 separate image files

<b>Notes:</b>
- Each page becomes a separate image
- High quality (200 DPI)
- For PDFs with many pages (&gt;10), consider file size

━━━━━━━━━━━━━━━━━━━━━

<b>5️⃣ IMAGES TO PDF</b>
Combine multiple images into one PDF.

<b>How to use:</b>
- Send 2+ images (JPG, PNG, etc.)
- Type: /topdf
- Receive combined PDF

<b>Supported formats:</b>
JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP

<b>Example:</b>
Send: photo1.jpg, photo2.jpg, photo3.png
Command: /topdf
Result: combined.pdf (3 pages)

<b>Limits:</b>
- Max images: 50
- Images are ordered by upload time

━━━━━━━━━━━━━━━━━━━━━

<b>⚠️ IMPORTANT NOTES:</b>

<b>File Size Limits:</b>
- Maximum file size: 50MB per file
- This is Telegram's limit for bot downloads

<b>Temporary Storage:</b>
- Files are automatically deleted after processing
- No files are stored permanently
- Your privacy is protected

<b>Processing Time:</b>
- Small files: Instant
- Large files: May take 30-60 seconds
- You'll see progress updates

<b>Error Messages:</b>
If something goes wrong, you'll receive:
- Clear error message
- Suggestion for fixing the issue
- Can retry with /cancel and start over

━━━━━━━━━━━━━━━━━━━━━

<b>🆘 COMMON ISSUES:</b>

<b>"No files found"</b>
→ Upload files before using commands

<b>"File too large"</b>
→ Compress files or split into smaller PDFs

<b>"Invalid page range"</b>
→ Check page numbers match PDF length

<b>"Processing failed"</b>
→ File may be corrupted, try another file

━━━━━━━━━━━━━━━━━━━━━

<b>💡 TIPS &amp; TRICKS:</b>

1. <b>Merge in order:</b> Files are merged in the order you send them

2. <b>Batch processing:</b> Send all files at once, then use command

3. <b>Quality vs Size:</b> For compress, use:
   • "low" for maximum compression
   • "high" for best quality

4. <b>Page extraction:</b> Use /split to remove unwanted pages before sharing

5. <b>Cancel anytime:</b> Use /cancel to abort current operation

━━━━━━━━━━━━━━━━━━━━━

<b>❓ Still Need Help?</b>

- Try /about for bot info
- Check supported formats above
- Ensure files aren't corrupted
- Restart with /start

Happy PDF processing! 🎉
"""
    
    await update.message.reply_text(
        help_message,
        parse_mode='HTML'
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /about command - Show bot information.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    # Track user activity
    analytics.track_user(update.effective_user, 'about')
    
    bot_info = config.get_bot_info()
    
    about_message = f"""
ℹ️ <b>About This Bot</b>

<b>Name:</b> {bot_info['name']}
<b>Version:</b> {bot_info['version']}
<b>Description:</b> {bot_info['description']}

━━━━━━━━━━━━━━━━━━━━━

<b>📊 System Info:</b>
- Max file size: 50MB
- Max PDFs to merge: 20
- Max images to convert: 50
- Supported formats: PDF, JPG, PNG, GIF, BMP, TIFF, WEBP

━━━━━━━━━━━━━━━━━━━━━

<b>✨ Features:</b>
- Merge multiple PDFs
- Split PDFs by page range
- Compress PDFs efficiently
- Convert PDF to images
- Convert images to PDF

<b>🔒 Privacy:</b>
- No data storage
- Files deleted after processing
- Secure temporary storage
- No tracking or analytics

<b>💰 Cost:</b>
- Completely FREE
- No limits on usage
- No ads or subscriptions

━━━━━━━━━━━━━━━━━━━━━

<b>👨‍💻 Developer:</b>
{bot_info['developer']}

<b>🐛 Report Issues:</b>
Found a bug? Have suggestions?
Reach out to our Official Support Channel : @snapbothub

━━━━━━━━━━━━━━━━━━━━━

Made with ❤️ for the Telegram community!

Type /help for usage instructions.
"""
    
    await update.message.reply_text(
        about_message,
        parse_mode='HTML'
    )


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /cancel command - Cancel current operation and clean up files.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    from utils import file_manager
    
    user_id = update.effective_user.id
    
    # Track user activity
    analytics.track_user(update.effective_user, 'cancel')
    
    # Clean up user's temporary files
    file_manager.cleanup_user_files(user_id)
    
    # Clear user data from context
    context.user_data.clear()
    
    await update.message.reply_text(
        "✅ Operation cancelled!\n\n"
        "All temporary files have been deleted.\n"
        "You can start a new operation anytime. 🔄",
        parse_mode='HTML'
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /stats command - Show bot usage statistics (admin only).
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_id = update.effective_user.id
    
    # Check if user is admin
    if user_id not in config.ADMIN_USER_IDS:
        await update.message.reply_text(
            "⚠️ This command is only available to bot administrators.",
            parse_mode='HTML'
        )
        return
    
    # Get statistics
    stats = analytics.get_statistics()
    
    # Format today's users
    today_users_text = ""
    if stats['today_users']:
        today_users_text = "\n".join([
            f"• {user['name']} (@{user['username'] or 'N/A'}) - {user['operations']} ops"
            for user in stats['today_users']
        ])
    else:
        today_users_text = "No users today yet."
    
    # Format all-time top users
    top_users_text = ""
    if stats['top_users']:
        top_users_text = "\n".join([
            f"{i+1}. {user['name']} (@{user['username'] or 'N/A'}) - {user['operations']} ops"
            for i, user in enumerate(stats['top_users'][:10])
        ])
    else:
        top_users_text = "No data yet."
    
    stats_message = f"""
📊 <b>Bot Usage Statistics</b>

━━━━━━━━━━━━━━━━━━━━━

<b>📅 TODAY'S STATS</b>
- Unique Users: {stats['today_unique_users']}
- Total Operations: {stats['today_operations']}

<b>👥 Today's Users:</b>
{today_users_text}

━━━━━━━━━━━━━━━━━━━━━

<b>📈 ALL-TIME STATS</b>
- Total Unique Users: {stats['total_unique_users']}
- Total Operations: {stats['total_operations']}

<b>🏆 Top 10 Users:</b>
{top_users_text}

━━━━━━━━━━━━━━━━━━━━━

<b>🔧 Operations Breakdown:</b>
- Merge: {stats['operations_by_type'].get('merge', 0)}
- Split: {stats['operations_by_type'].get('split', 0)}
- Compress: {stats['operations_by_type'].get('compress', 0)}
- PDF to Images: {stats['operations_by_type'].get('toimage', 0)}
- Images to PDF: {stats['operations_by_type'].get('topdf', 0)}

━━━━━━━━━━━━━━━━━━━━━

Last updated: {stats['last_updated']}
"""
    
    await update.message.reply_text(
        stats_message,
        parse_mode='HTML'
    )