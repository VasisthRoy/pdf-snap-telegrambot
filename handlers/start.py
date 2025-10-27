"""
Start and help command handlers for PDF Telegram Bot.
Provides welcome messages and usage instructions.
"""

from telegram import Update
from telegram.ext import ContextTypes

import config


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command - Show welcome message and basic instructions.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    user_name = update.effective_user.first_name
    
    welcome_message = f"""
👋 *Welcome {user_name}\\!*

I'm *{config.BOT_NAME}* \\- Your free PDF manipulation assistant\\! 🎉

🔧 *What I Can Do:*
- 📄 Merge multiple PDFs into one
- ✂️ Split PDFs and extract specific pages
- 🗜️ Compress PDFs to reduce file size
- 🖼️ Convert PDFs to images
- 📄 Convert images to PDF

⚡ *Quick Start:*
1\\. Send me PDF files or images
2\\. Use commands below to process them
3\\. Get your result instantly\\!

📋 *Available Commands:*
/merge \\- Merge multiple PDFs into one
/split \\- Extract pages \\(e\\.g\\., /split 1\\-3\\)
/compress \\- Reduce PDF file size
/toimage \\- Convert PDF to images
/topdf \\- Convert images to PDF
/help \\- Detailed help and examples
/about \\- Bot information
/cancel \\- Cancel current operation

💡 *Tip:* Send me files first, then use the commands\\!

Need help? Type /help for detailed instructions\\.

Let's get started\\! 🚀
"""
    
    await update.message.reply_text(
        welcome_message,
        parse_mode='MarkdownV2'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /help command - Show detailed usage instructions.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    help_message = """
📚 *Detailed Help Guide*

*1️⃣ MERGE PDFs*
Combine multiple PDF files into one document\\.

*How to use:*
- Send 2 or more PDF files
- Type: /merge
- Receive merged PDF

*Example:*
Send: report1\\.pdf, report2\\.pdf
Command: /merge
Result: merged\\.pdf \\(contains all pages\\)

*Limits:*
- Min files: 2
- Max files: 20
- Max size per file: 50MB

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*2️⃣ SPLIT PDF*
Extract specific pages from a PDF\\.

*How to use:*
- Send 1 PDF file
- Type: /split \\<page\\_specification\\>
- Receive extracted pages

*Page Specifications:*
- Single page: /split 5
- Page range: /split 1\\-3
- Multiple pages: /split 1,3,5
- From page to end: /split 3\\-end
- Mix formats: /split 1\\-3,5,7\\-end

*Examples:*
/split 1\\-3 → Extract pages 1, 2, 3
/split 2,4,6 → Extract pages 2, 4, 6
/split 5\\-end → Extract from page 5 to last page

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*3️⃣ COMPRESS PDF*
Reduce PDF file size while maintaining quality\\.

*How to use:*
- Send 1 PDF file
- Type: /compress \\[quality\\]
- Receive compressed PDF

*Quality Levels:*
- /compress → Default \\(balanced\\)
- /compress low → Maximum compression
- /compress high → Better quality, less compression

*Example:*
Send: large\\_document\\.pdf \\(10MB\\)
Command: /compress
Result: compressed\\.pdf \\(3\\-5MB typically\\)

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*4️⃣ PDF TO IMAGES*
Convert each PDF page to an image file\\.

*How to use:*
- Send 1 PDF file
- Type: /toimage, /topng, or /tojpg
- Receive images \\(PNG format default\\)

*Example:*
Send: presentation\\.pdf \\(5 pages\\)
Command: /toimage
Result: 5 separate image files

*Notes:*
- Each page becomes a separate image
- High quality \\(200 DPI\\)
- For PDFs with many pages \\(\\>10\\), consider file size

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*5️⃣ IMAGES TO PDF*
Combine multiple images into one PDF\\.

*How to use:*
- Send 2\\+ images \\(JPG, PNG, etc\\.\\)
- Type: /topdf
- Receive combined PDF

*Supported formats:*
JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP

*Example:*
Send: photo1\\.jpg, photo2\\.jpg, photo3\\.png
Command: /topdf
Result: combined\\.pdf \\(3 pages\\)

*Limits:*
- Max images: 50
- Images are ordered by upload time

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*⚠️ IMPORTANT NOTES:*

*File Size Limits:*
- Maximum file size: 50MB per file
- This is Telegram's limit for bot downloads

*Temporary Storage:*
- Files are automatically deleted after processing
- No files are stored permanently
- Your privacy is protected

*Processing Time:*
- Small files: Instant
- Large files: May take 30\\-60 seconds
- You'll see progress updates

*Error Messages:*
If something goes wrong, you'll receive:
- Clear error message
- Suggestion for fixing the issue
- Can retry with /cancel and start over

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*🆘 COMMON ISSUES:*

*"No files found"*
→ Upload files before using commands

*"File too large"*
→ Compress files or split into smaller PDFs

*"Invalid page range"*
→ Check page numbers match PDF length

*"Processing failed"*
→ File may be corrupted, try another file

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*💡 TIPS & TRICKS:*

1\\. *Merge in order:* Files are merged in the order you send them

2\\. *Batch processing:* Send all files at once, then use command

3\\. *Quality vs Size:* For compress, use:
   • "low" for maximum compression
   • "high" for best quality

4\\. *Page extraction:* Use /split to remove unwanted pages before sharing

5\\. *Cancel anytime:* Use /cancel to abort current operation

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*❓ Still Need Help?*

- Try /about for bot info
- Check supported formats above
- Ensure files aren't corrupted
- Restart with /start

Happy PDF processing\\! 🎉
"""
    
    await update.message.reply_text(
        help_message,
        parse_mode='MarkdownV2'
    )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /about command - Show bot information.
    
    Args:
        update: Telegram update object
        context: Telegram context object
    """
    bot_info = config.get_bot_info()
    
    about_message = f"""
ℹ️ *About This Bot*

*Name:* {bot_info['name']}
*Version:* {bot_info['version']}
*Description:* {bot_info['description']}

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*📊 System Info:*
- Max file size: 50MB
- Max PDFs to merge: 20
- Max images to convert: 50
- Supported formats: PDF, JPG, PNG, GIF, BMP, TIFF, WEBP

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*✨ Features:*
- Merge multiple PDFs
- Split PDFs by page range
- Compress PDFs efficiently
- Convert PDF to images
- Convert images to PDF

*🔒 Privacy:*
- No data storage
- Files deleted after processing
- Secure temporary storage
- No tracking or analytics

*💰 Cost:*
- Completely FREE
- No limits on usage
- No ads or subscriptions

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

*👨‍💻 Developer:*
{bot_info['developer']}

*🐛 Report Issues:*
Found a bug? Have suggestions?
Reach out to our Official Support Channel : @snapbothub

\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-\\-

Made with ❤️ for the Telegram community\\!

Type /help for usage instructions\\.
"""
    
    await update.message.reply_text(
        about_message,
        parse_mode='MarkdownV2'
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
    
    # Clean up user's temporary files
    file_manager.cleanup_user_files(user_id)
    
    # Clear user data from context
    context.user_data.clear()
    
    await update.message.reply_text(
        "✅ Operation cancelled\\!\n\n"
        "All temporary files have been deleted\\.\n"
        "You can start a new operation anytime\\. 🔄",
        parse_mode='MarkdownV2'
    )