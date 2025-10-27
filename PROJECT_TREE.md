# 🌲 PDF Telegram Bot - Project Tree

```
pdf-telegram-bot/
│
├── 📄 Core Application Files
│   ├── bot.py                      # Main bot application (entry point)
│   ├── config.py                   # Configuration and settings management
│   └── requirements.txt            # Python dependencies
│
├── 🤖 Bot Handlers (handlers/)
│   ├── __init__.py                # Package initializer
│   ├── start.py                   # /start, /help, /about, /cancel commands
│   ├── merge.py                   # /merge command and PDF file handler
│   ├── split.py                   # /split command for page extraction
│   ├── compress.py                # /compress command for size reduction
│   └── convert.py                 # /toimage, /topdf conversion handlers
│
├── 🛠️ Utilities (utils/)
│   ├── __init__.py                # Package initializer
│   ├── file_manager.py            # File operations and cleanup
│   └── pdf_operations.py          # PDF processing functions
│
├── 📚 Documentation
│   ├── README.md                  # Main documentation (START HERE!)
│   ├── DEPLOY.md                  # Deployment guide for 3 platforms
│   ├── TESTING.md                 # Complete testing guide
│   ├── CONTRIBUTING.md            # Contribution guidelines
│   ├── PROJECT_SUMMARY.md         # This overview document
│   └── LICENSE                    # MIT License
│
├── 🚀 Deployment Files
│   ├── Procfile                   # Railway/Heroku deployment
│   ├── nixpacks.toml             # Railway configuration
│   ├── runtime.txt               # Python version specification
│   ├── Dockerfile                # Docker containerization
│   └── docker-compose.yml        # Docker Compose configuration
│
├── ⚙️ Configuration
│   ├── .env.example              # Environment variables template
│   └── .gitignore                # Git ignore rules
│
└── ⚡ Setup Script
    └── quick_start.sh            # Automated setup script
```

## 📊 File Statistics

### Code Files
```
bot.py                 202 lines    Main application logic
config.py               99 lines    Configuration management
handlers/start.py      186 lines    Basic commands
handlers/merge.py      155 lines    Merge functionality
handlers/split.py      146 lines    Split functionality
handlers/compress.py   165 lines    Compression
handlers/convert.py    281 lines    Conversions
utils/file_manager.py  173 lines    File operations
utils/pdf_operations.py 291 lines    PDF processing
───────────────────────────────────────────────────
Total Code:          ~1,700 lines
```

### Documentation Files
```
README.md              519 lines    Main documentation
DEPLOY.md              672 lines    Deployment guide
TESTING.md             640 lines    Testing procedures
CONTRIBUTING.md        474 lines    Contribution guide
PROJECT_SUMMARY.md     389 lines    Project overview
───────────────────────────────────────────────────
Total Docs:          ~2,700 lines
```

### Configuration Files
```
requirements.txt        13 lines    Python dependencies
.env.example            44 lines    Environment template
Dockerfile              34 lines    Docker configuration
docker-compose.yml      20 lines    Docker Compose
Procfile                 1 line     Railway/Heroku
nixpacks.toml            4 lines    Railway config
runtime.txt              1 line     Python version
.gitignore              58 lines    Git ignore
───────────────────────────────────────────────────
Total Config:          ~175 lines
```

## 🎯 Key Components

### 1. Entry Point
```
bot.py
  └── Imports handlers and starts bot
  └── Registers all commands
  └── Sets up error handling
  └── Manages cleanup scheduler
```

### 2. Handler Flow
```
User sends message
     ↓
Telegram → bot.py → Appropriate Handler
                         ↓
                    File Manager (download)
                         ↓
                    PDF Operations (process)
                         ↓
                    Send Result to User
                         ↓
                    File Manager (cleanup)
```

### 3. File Processing Flow
```
1. User uploads file(s)
   ↓
2. Bot validates file type & size
   ↓
3. Downloads to /tmp/pdf_bot_temp/user_ID/
   ↓
4. Stores path in context.user_data
   ↓
5. User issues command (/merge, /split, etc.)
   ↓
6. Handler processes files
   ↓
7. Sends result to user
   ↓
8. Cleanup deletes all temp files
```

## 📦 Module Dependencies

```
bot.py
  ├── requires: telegram, telegram.ext
  ├── imports: config
  ├── imports: all handlers
  └── imports: utils.cleanup_scheduler

handlers/*
  ├── requires: telegram, telegram.ext
  ├── imports: config
  ├── imports: utils.file_manager
  └── imports: utils.pdf_operations

utils/pdf_operations.py
  ├── requires: PyPDF2
  ├── requires: pikepdf
  ├── requires: pdf2image
  ├── requires: Pillow
  └── imports: config

utils/file_manager.py
  ├── requires: telegram
  ├── requires: pathlib
  └── imports: config

config.py
  └── requires: os, pathlib
```

## 🔄 Data Flow

### User Context Storage
```
context.user_data = {
    'pdf_files': [Path, Path, ...],     # Uploaded PDF paths
    'image_files': [Path, Path, ...]     # Uploaded image paths
}
```

### Temporary File Structure
```
/tmp/pdf_bot_temp/
  ├── user_123456_abc123/
  │   ├── document1.pdf
  │   ├── document2.pdf
  │   ├── image1.jpg
  │   ├── image2.png
  │   └── images/
  │       ├── page_001.png
  │       └── page_002.png
  │
  └── user_789012_def456/
      └── document.pdf
```

## 🎨 Architecture Diagram

```
┌─────────────────────────────────────────────┐
│           Telegram User Interface           │
└─────────────────┬───────────────────────────┘
                  │
         ┌────────▼────────┐
         │   telegram      │
         │   API Client    │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │    bot.py       │
         │  Main Handler   │
         └────────┬────────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
┌─────▼─────┐ ┌──▼───┐ ┌────▼────┐
│  config   │ │ utils │ │handlers │
│  .py      │ │       │ │         │
└───────────┘ └───┬───┘ └────┬────┘
                  │           │
         ┌────────▼───────────▼────────┐
         │   File System Operations    │
         │  /tmp/pdf_bot_temp/         │
         └─────────────────────────────┘
```

## 🔍 Feature Map

```
Commands
├── /start
│   └── start.py → start_command()
│
├── /help
│   └── start.py → help_command()
│
├── /about
│   └── start.py → about_command()
│
├── /cancel
│   └── start.py → cancel_command()
│
├── /merge
│   └── merge.py → merge_command()
│       └── pdf_operations.merge_pdfs()
│
├── /split <pages>
│   └── split.py → split_command()
│       └── pdf_operations.split_pdf()
│
├── /compress [quality]
│   └── compress.py → compress_command()
│       └── pdf_operations.compress_pdf()
│
├── /toimage | /topng | /tojpg
│   └── convert.py → pdf_to_images_command()
│       └── pdf_operations.pdf_to_images()
│
└── /topdf
    └── convert.py → images_to_pdf_command()
        └── pdf_operations.images_to_pdf()

File Handlers
├── PDF Document
│   └── merge.py → handle_pdf_file()
│
└── Photo/Image
    └── convert.py → handle_image_file()
```

## 📝 Quick Reference

### Want to...
- **Start the bot locally?** → `python bot.py`
- **Deploy to Railway?** → See DEPLOY.md section "Railway.app"
- **Test features?** → See TESTING.md
- **Add a feature?** → See CONTRIBUTING.md
- **Configure settings?** → Edit `config.py` or `.env`
- **Check logs?** → Look for console output or check hosting logs
- **Fix an error?** → See "Troubleshooting" in README.md

### Files to Edit
- **Bot token:** `.env` file
- **Bot settings:** `config.py`
- **Commands:** `handlers/*.py`
- **PDF logic:** `utils/pdf_operations.py`
- **File handling:** `utils/file_manager.py`

### Don't Edit
- `__pycache__/` (auto-generated)
- `.env` (don't commit to git!)
- `/tmp/pdf_bot_temp/` (temporary files)

## 🎯 Where to Start

### As a User
1. Read `README.md` (Quick Start section)
2. Get bot token from @BotFather
3. Run `quick_start.sh` OR manually setup
4. Test locally
5. Deploy (see `DEPLOY.md`)

### As a Developer
1. Read `README.md` (Installation section)
2. Read `CONTRIBUTING.md` (Development Setup)
3. Study code in `handlers/` and `utils/`
4. Make changes
5. Test (see `TESTING.md`)
6. Submit PR

### As a Deployer
1. Read `DEPLOY.md`
2. Choose platform (Railway recommended)
3. Follow step-by-step guide
4. Configure environment variables
5. Deploy and monitor logs

---

**This tree shows the complete structure of your production-ready bot!** 🌲

Need help? Start with `README.md`! 📖
