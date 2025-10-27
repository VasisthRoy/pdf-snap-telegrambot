# 🧪 Testing Guide - PDF Tools Telegram Bot

Complete testing guide to ensure your bot works correctly.

## 📋 Table of Contents

- [Pre-Testing Setup](#-pre-testing-setup)
- [Manual Testing Checklist](#-manual-testing-checklist)
- [Feature-by-Feature Tests](#️-feature-by-feature-tests)
- [Error Handling Tests](#-error-handling-tests)
- [Performance Tests](#-performance-tests)
- [Automated Testing](#-automated-testing)

## 🔧 Pre-Testing Setup

### 1. Prepare Test Files

Create a `test_files/` directory with:

**PDFs:**
- `small.pdf` (1-2 pages, < 1MB)
- `medium.pdf` (10-20 pages, 5-10MB)
- `large.pdf` (50+ pages, 20-40MB)
- `corrupted.pdf` (intentionally corrupted file)
- `password-protected.pdf` (encrypted PDF)

**Images:**
- `image1.jpg` (standard photo)
- `image2.png` (transparent background)
- `image3.gif` (animated)
- Various sizes: small (< 100KB), medium (1-5MB), large (> 10MB)

### 2. Start Bot Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Run bot
python bot.py
```

### 3. Open Telegram

- Start a chat with your bot
- Clear any previous files
- Type `/start`

## ✅ Manual Testing Checklist

### Basic Commands

- [ ] `/start` - Shows welcome message with all commands
- [ ] `/help` - Displays detailed help guide
- [ ] `/about` - Shows bot information
- [ ] `/cancel` - Clears user data and files
- [ ] Invalid command - Bot should handle gracefully

### Bot Responsiveness

- [ ] Bot responds within 2 seconds
- [ ] Messages are properly formatted
- [ ] Emojis display correctly
- [ ] Markdown formatting works
- [ ] Links are clickable

### File Handling

- [ ] Bot accepts PDF files
- [ ] Bot accepts image files (JPG, PNG, GIF, etc.)
- [ ] Bot rejects non-PDF/image files
- [ ] File size validation works
- [ ] Multiple files can be uploaded
- [ ] Files are stored temporarily
- [ ] Files are deleted after processing

## 🛠️ Feature-by-Feature Tests

### 1. Merge PDFs

#### Test Case 1.1: Basic Merge (2 PDFs)
```
Steps:
1. Send small.pdf
2. Send medium.pdf
3. Type /merge

Expected Result:
✅ Bot combines both PDFs
✅ Shows file count (2 PDFs)
✅ Shows total size
✅ Sends merged PDF
✅ Cleans up temp files

Pass/Fail: ___
```

#### Test Case 1.2: Multiple PDFs
```
Steps:
1. Send 5 different PDF files
2. Type /merge

Expected Result:
✅ All 5 PDFs merged in order
✅ Page count is sum of all pages
✅ File size displayed

Pass/Fail: ___
```

#### Test Case 1.3: Maximum PDFs
```
Steps:
1. Send 20 PDF files
2. Type /merge

Expected Result:
✅ Successfully merges all 20 files
✅ Processing time < 2 minutes
✅ Resulting file sent successfully

Pass/Fail: ___
```

#### Test Case 1.4: Error - Not Enough Files
```
Steps:
1. Send only 1 PDF
2. Type /merge

Expected Result:
❌ Bot shows error message
✅ Explains minimum 2 PDFs needed
✅ Provides usage example

Pass/Fail: ___
```

#### Test Case 1.5: Error - Too Many Files
```
Steps:
1. Send 25 PDF files
2. Type /merge

Expected Result:
❌ Bot shows error message
✅ Explains maximum 20 PDFs limit
✅ Suggests using /cancel

Pass/Fail: ___
```

### 2. Split PDF

#### Test Case 2.1: Split Range (1-3)
```
Steps:
1. Send a 10-page PDF
2. Type /split 1-3

Expected Result:
✅ Extracts pages 1, 2, 3
✅ New PDF has 3 pages
✅ Page content is correct

Pass/Fail: ___
```

#### Test Case 2.2: Split Individual Pages
```
Steps:
1. Send a 10-page PDF
2. Type /split 1,5,10

Expected Result:
✅ Extracts pages 1, 5, 10
✅ New PDF has 3 pages
✅ Pages in correct order

Pass/Fail: ___
```

#### Test Case 2.3: Split to End
```
Steps:
1. Send a 10-page PDF
2. Type /split 5-end

Expected Result:
✅ Extracts pages 5-10
✅ New PDF has 6 pages
✅ All pages present

Pass/Fail: ___
```

#### Test Case 2.4: Complex Split
```
Steps:
1. Send a 20-page PDF
2. Type /split 1-3,5,10-end

Expected Result:
✅ Extracts pages 1,2,3,5,10,11...20
✅ Correct number of pages
✅ No duplicate pages

Pass/Fail: ___
```

#### Test Case 2.5: Error - No Page Specification
```
Steps:
1. Send a PDF
2. Type /split (without page numbers)

Expected Result:
❌ Bot shows error message
✅ Shows PDF has X pages
✅ Provides format examples

Pass/Fail: ___
```

#### Test Case 2.6: Error - Invalid Page Range
```
Steps:
1. Send a 5-page PDF
2. Type /split 1-10

Expected Result:
❌ Bot shows error message
✅ Explains pages 6-10 don't exist
✅ Shows valid range (1-5)

Pass/Fail: ___
```

### 3. Compress PDF

#### Test Case 3.1: Default Compression
```
Steps:
1. Send a large PDF (10-20MB)
2. Type /compress

Expected Result:
✅ PDF is compressed
✅ Shows before/after size
✅ Shows compression percentage
✅ File size reduced by 30-70%

Pass/Fail: ___
```

#### Test Case 3.2: Low Quality (Maximum Compression)
```
Steps:
1. Send a large PDF
2. Type /compress low

Expected Result:
✅ Maximum compression applied
✅ Significant size reduction
✅ File still readable

Pass/Fail: ___
```

#### Test Case 3.3: High Quality (Minimal Compression)
```
Steps:
1. Send a large PDF
2. Type /compress high

Expected Result:
✅ Minimal compression
✅ Slight size reduction
✅ Quality maintained

Pass/Fail: ___
```

#### Test Case 3.4: Already Optimized PDF
```
Steps:
1. Send a well-compressed PDF
2. Type /compress

Expected Result:
✅ Bot attempts compression
✅ Shows compression not effective
✅ Sends original file back

Pass/Fail: ___
```

### 4. PDF to Images

#### Test Case 4.1: Small PDF (5 pages)
```
Steps:
1. Send a 5-page PDF
2. Type /toimage

Expected Result:
✅ Converts all 5 pages
✅ Sends 5 separate images
✅ Images are high quality (200 DPI)
✅ Each image labeled (Page X of 5)

Pass/Fail: ___
```

#### Test Case 4.2: Large PDF (20+ pages)
```
Steps:
1. Send a 20-page PDF
2. Type /toimage

Expected Result:
✅ Shows warning about many pages
✅ Converts all pages
✅ Sends images as ZIP file
✅ ZIP contains all pages

Pass/Fail: ___
```

#### Test Case 4.3: JPG Format
```
Steps:
1. Send a PDF
2. Type /tojpg

Expected Result:
✅ Converts to JPG format
✅ Images sent successfully
✅ File size smaller than PNG

Pass/Fail: ___
```

### 5. Images to PDF

#### Test Case 5.1: Multiple Images
```
Steps:
1. Send 3 JPG images
2. Type /topdf

Expected Result:
✅ Combines into 3-page PDF
✅ Images in upload order
✅ Aspect ratios maintained
✅ Good quality

Pass/Fail: ___
```

#### Test Case 5.2: Mixed Formats
```
Steps:
1. Send JPG, PNG, GIF files
2. Type /topdf

Expected Result:
✅ All formats converted
✅ Single PDF created
✅ All pages present

Pass/Fail: ___
```

#### Test Case 5.3: Transparent PNG
```
Steps:
1. Send PNG with transparency
2. Type /topdf

Expected Result:
✅ Converts successfully
✅ White background added
✅ No transparency issues

Pass/Fail: ___
```

## ⚠️ Error Handling Tests

### File Errors

#### Test Case E1: Corrupted PDF
```
Steps:
1. Send corrupted.pdf
2. Try any operation

Expected Result:
❌ Bot detects corruption
✅ Shows helpful error message
✅ Suggests uploading valid file

Pass/Fail: ___
```

#### Test Case E2: Password-Protected PDF
```
Steps:
1. Send encrypted PDF
2. Try any operation

Expected Result:
❌ Bot cannot process
✅ Explains file is protected
✅ Suggests removing password first

Pass/Fail: ___
```

#### Test Case E3: File Too Large
```
Steps:
1. Send PDF > 50MB

Expected Result:
❌ Bot rejects file
✅ Shows file size and limit
✅ Suggests compression/splitting

Pass/Fail: ___
```

#### Test Case E4: Wrong File Type
```
Steps:
1. Send .docx or .txt file
2. Try PDF operation

Expected Result:
❌ Bot rejects file
✅ Explains expecting PDF
✅ Lists supported formats

Pass/Fail: ___
```

### Command Errors

#### Test Case E5: No Files Uploaded
```
Steps:
1. Type /merge without uploading files

Expected Result:
❌ Bot shows error
✅ Explains files needed first
✅ Shows step-by-step example

Pass/Fail: ___
```

#### Test Case E6: Wrong File Count
```
Steps:
1. Send 1 PDF
2. Type /merge

Expected Result:
❌ Shows error
✅ Explains need 2+ files
✅ Current count displayed

Pass/Fail: ___
```

## 📊 Performance Tests

### Speed Tests

#### Test P1: Small File Processing
```
Metric: Time to merge 2 small PDFs (< 1MB each)
Target: < 5 seconds
Actual: ___ seconds
Pass/Fail: ___
```

#### Test P2: Medium File Processing
```
Metric: Time to compress 10MB PDF
Target: < 15 seconds
Actual: ___ seconds
Pass/Fail: ___
```

#### Test P3: Large File Processing
```
Metric: Time to convert 30-page PDF to images
Target: < 60 seconds
Actual: ___ seconds
Pass/Fail: ___
```

### Concurrent Users

#### Test P4: Multiple Users
```
Steps:
1. Have 3-5 people use bot simultaneously
2. Each performs different operations

Expected Result:
✅ All operations complete successfully
✅ No file mixing between users
✅ Response time acceptable for all

Pass/Fail: ___
```

### Memory Tests

#### Test P5: Memory Cleanup
```
Steps:
1. Process 10 large files sequentially
2. Use /cancel after each
3. Monitor system memory

Expected Result:
✅ Memory usage returns to baseline
✅ No memory leaks
✅ Temp files deleted

Pass/Fail: ___
```

## 🤖 Automated Testing

### Setup Test Script

Create `test_bot.py`:

```python
import asyncio
from telegram import Bot
from telegram.error import TelegramError

async def test_bot_connection(token):
    """Test if bot is responding"""
    try:
        bot = Bot(token)
        me = await bot.get_me()
        print(f"✅ Bot connected: @{me.username}")
        return True
    except TelegramError as e:
        print(f"❌ Connection failed: {e}")
        return False

async def test_commands(token, chat_id):
    """Test basic commands"""
    bot = Bot(token)
    commands = ['/start', '/help', '/about']
    
    for cmd in commands:
        try:
            await bot.send_message(chat_id, cmd)
            print(f"✅ Command {cmd} sent")
        except Exception as e:
            print(f"❌ Command {cmd} failed: {e}")

# Run tests
asyncio.run(test_bot_connection("YOUR_TOKEN"))
```

## 📝 Test Report Template

```
=================================
PDF TELEGRAM BOT - TEST REPORT
=================================

Date: __________
Tester: __________
Version: __________

SUMMARY:
--------
Total Tests: ___
Passed: ___
Failed: ___
Skipped: ___

FEATURE TESTS:
--------------
Merge PDFs: [ PASS / FAIL ]
Split PDFs: [ PASS / FAIL ]
Compress PDFs: [ PASS / FAIL ]
PDF to Images: [ PASS / FAIL ]
Images to PDF: [ PASS / FAIL ]

ERROR HANDLING:
---------------
File Errors: [ PASS / FAIL ]
Command Errors: [ PASS / FAIL ]
Edge Cases: [ PASS / FAIL ]

PERFORMANCE:
------------
Speed Tests: [ PASS / FAIL ]
Memory Tests: [ PASS / FAIL ]
Concurrent Users: [ PASS / FAIL ]

CRITICAL ISSUES:
----------------
1. _____________________
2. _____________________
3. _____________________

MINOR ISSUES:
-------------
1. _____________________
2. _____________________

RECOMMENDATIONS:
----------------
1. _____________________
2. _____________________

OVERALL RESULT: [ PASS / FAIL ]

Notes:
______________________
______________________
```

## ✅ Deployment Testing

Before deploying to production:

- [ ] All core features tested and passing
- [ ] Error handling verified
- [ ] Performance acceptable
- [ ] Memory cleanup working
- [ ] Tested on deployment platform
- [ ] Environment variables configured
- [ ] Logs are readable and helpful
- [ ] Bot responds within acceptable time
- [ ] File size limits enforced
- [ ] Temp files cleaned up properly

---

**Remember:** Test thoroughly before deploying! Users depend on your bot working correctly. 🧪

[⬆ Back to Top](#-testing-guide---pdf-tools-telegram-bot)
