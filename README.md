# 📄 PDF Tools Telegram Bot

A powerful, free, and easy-to-use Telegram bot for PDF manipulation. Merge, split, compress PDFs, and convert between PDF and image formats - all within Telegram!

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Bot Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)

## ✨ Features

🔧 **Core Features:**
- **Merge PDFs** - Combine multiple PDF files into one document
- **Split PDFs** - Extract specific pages from PDFs with flexible page ranges
- **Compress PDFs** - Reduce file size with configurable quality levels
- **PDF to Images** - Convert PDF pages to individual images (PNG/JPG)
- **Images to PDF** - Combine multiple images into a single PDF

⚡ **Additional Benefits:**
- 100% Free and open-source
- No file storage - complete privacy
- Fast processing with async operations
- User-friendly with detailed error messages
- Works on free hosting platforms
- Supports concurrent users
- Auto cleanup of temporary files

## 📋 Table of Contents

- [Demo](#-demo)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Deployment](#-deployment)
- [System Requirements](#-system-requirements)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🎬 Demo

**Bot Commands:**
```
/start      - Welcome message and feature overview
/help       - Detailed usage guide with examples
/merge      - Merge multiple PDFs into one
/split      - Extract specific pages from PDF
/compress   - Reduce PDF file size
/toimage    - Convert PDF to images
/topdf      - Convert images to PDF
/cancel     - Cancel operation and clear files
/about      - Bot information
```

**Example Usage:**
```
1. Send file1.pdf, file2.pdf to the bot
2. Type: /merge
3. Receive merged PDF instantly!
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Telegram account
- Bot token from [@BotFather](https://t.me/BotFather)

### 5-Minute Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/pdf-telegram-bot.git
cd pdf-telegram-bot

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install system dependencies (Ubuntu/Debian)
sudo apt-get install poppler-utils

# 4. Create .env file from template
cp .env.example .env

# 5. Edit .env and add your bot token
nano .env  # or use any text editor
# Add: BOT_TOKEN=your_token_from_botfather

# 6. Run the bot
python bot.py
```

That's it! Your bot is now running! 🎉

## 📦 Installation

### Step 1: Get Your Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions:
   - Choose a name for your bot (e.g., "My PDF Bot")
   - Choose a username (must end with 'bot', e.g., "my_pdf_tools_bot")
4. Copy the bot token provided (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. **Keep this token secret!** Don't share it publicly

### Step 2: System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
1. Download poppler from [this link](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Extract to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\Library\bin` to system PATH

### Step 3: Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### Step 4: Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your bot token
# BOT_TOKEN=your_actual_bot_token_here
```

### Step 5: Run the Bot

```bash
python bot.py
```

You should see:
```
INFO - Starting PDF Tools Bot v1.0.0...
INFO - Bot is starting... Press Ctrl+C to stop.
```

## ⚙️ Configuration

### Environment Variables

Edit the `.env` file to customize bot behavior:

```bash
# Required
BOT_TOKEN=your_bot_token_here

# Optional - Override defaults
MAX_FILE_SIZE=52428800      # 50MB in bytes
MAX_MERGE_FILES=20          # Max PDFs to merge
MAX_IMAGE_FILES=50          # Max images to convert

# Customization
BOT_NAME=My PDF Bot
BOT_DEVELOPER=Your Name
GITHUB_REPO=https://github.com/yourusername/pdf-bot
```

### File Size Limits

- **Maximum file size:** 50MB (Telegram's limit)
- **Maximum PDFs to merge:** 20 files
- **Maximum images to convert:** 50 images

These can be adjusted in `config.py` or via environment variables.

## 📖 Usage

### Merge PDFs

```
1. Send multiple PDF files (2+) to the bot
2. Type: /merge
3. Bot combines all PDFs and sends result
```

**Features:**
- Maintains page order
- Supports up to 20 PDFs
- Shows file count and size

### Split PDFs

```
1. Send a PDF file to the bot
2. Type: /split <page_specification>
```

**Page Specifications:**
- `/split 1-3` - Extract pages 1, 2, 3
- `/split 1,3,5` - Extract pages 1, 3, 5
- `/split 2-end` - From page 2 to last page
- `/split 1-3,5,7-end` - Mix multiple formats

### Compress PDFs

```
1. Send a PDF file to the bot
2. Type: /compress [quality]
```

**Quality Levels:**
- `/compress` - Default (balanced)
- `/compress low` - Maximum compression
- `/compress high` - Better quality

**Result:** Shows before/after file size comparison

### PDF to Images

```
1. Send a PDF file to the bot
2. Type: /toimage, /topng, or /tojpg
3. Receive images (PNG format by default)
```

**Features:**
- High quality (200 DPI)
- Each page becomes separate image
- Automatic ZIP for PDFs with 10+ pages

### Images to PDF

```
1. Send multiple images to the bot
2. Type: /topdf
3. Receive combined PDF
```

**Supported formats:** JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP

## 🚢 Deployment

The bot is designed to run on free hosting platforms. See [DEPLOY.md](DEPLOY.md) for detailed guides.

### Quick Deploy Options

**Railway.app** (Recommended)
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

**Render.com**
1. Connect GitHub repository
2. Create new Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python bot.py`
5. Add environment variables

**PythonAnywhere**
1. Upload files via dashboard
2. Create virtual environment
3. Install dependencies
4. Configure bot to run as background task

See [DEPLOY.md](DEPLOY.md) for step-by-step instructions with screenshots.

## 💻 System Requirements

### Minimum Requirements
- **CPU:** 1 core
- **RAM:** 512 MB
- **Storage:** 1 GB
- **Python:** 3.9+

### Recommended for Production
- **CPU:** 2 cores
- **RAM:** 1 GB
- **Storage:** 5 GB
- **Python:** 3.11+

### Dependencies
- Python 3.9+
- poppler-utils (system package)
- python-telegram-bot 20.7
- PyPDF2 3.0.1
- pikepdf 8.10.1
- pdf2image 1.17.0
- Pillow 10.2.0

## 🔧 Troubleshooting

### Common Issues

**1. Bot doesn't respond**
```bash
# Check if bot token is correct
grep BOT_TOKEN .env

# Check logs for errors
python bot.py
```

**2. "poppler not found" error**
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Verify installation
which pdftoppm
```

**3. PDF processing fails**
- Ensure PDF is not password-protected
- Check if PDF is corrupted (try opening it)
- Verify file size is under 50MB
- Use `/cancel` and try again

**4. Import errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**5. Permission errors**
```bash
# Ensure temp directory is writable
chmod 755 /tmp/pdf_bot_temp

# Or change temp directory in config.py
```

### Getting Help

- Check the [Issues](https://github.com/yourusername/pdf-telegram-bot/issues) page
- Read the [detailed help](DEPLOY.md) guide
- Contact via Telegram: [@your_username](https://t.me/your_username)

## 📊 Project Structure

```
pdf-telegram-bot/
├── bot.py                 # Main bot application
├── config.py              # Configuration and settings
├── requirements.txt       # Python dependencies
├── runtime.txt           # Python version specification
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── DEPLOY.md            # Deployment guide
├── handlers/            # Command handlers
│   ├── __init__.py
│   ├── start.py        # Start, help, about commands
│   ├── merge.py        # Merge PDF handler
│   ├── split.py        # Split PDF handler
│   ├── compress.py     # Compress PDF handler
│   └── convert.py      # Conversion handlers
└── utils/              # Utility functions
    ├── __init__.py
    ├── file_manager.py # File handling utilities
    └── pdf_operations.py # PDF processing functions
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/pdf-telegram-bot.git

# Create development branch
git checkout -b dev

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests (if available)
pytest

# Format code
black .
```

### Coding Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints where appropriate
- Write descriptive commit messages
- Add comments for complex logic
- Test thoroughly before submitting PR

## 📝 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [PyPDF2](https://github.com/py-pdf/PyPDF2) - PDF manipulation library
- [pikepdf](https://github.com/pikepdf/pikepdf) - PDF compression
- [pdf2image](https://github.com/Belval/pdf2image) - PDF to image conversion
- [Pillow](https://github.com/python-pillow/Pillow) - Image processing

## 📧 Contact

- **Developer:** Your Name
- **Email:** your.email@example.com
- **GitHub:** [@yourusername](https://github.com/yourusername)
- **Telegram:** [@your_username](https://t.me/your_username)

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Made with ❤️ for the Telegram community**

[⬆ Back to Top](#-pdf-tools-telegram-bot)
