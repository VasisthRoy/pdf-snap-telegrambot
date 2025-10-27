# 🚀 Deployment Guide - PDF Tools Telegram Bot

Complete step-by-step guide for deploying your bot on various free hosting platforms.

## 📋 Table of Contents

- [Pre-Deployment Checklist](#-pre-deployment-checklist)
- [Railway.app Deployment](#️-railwayapp-deployment-recommended)
- [Render.com Deployment](#-rendercom-deployment)
- [PythonAnywhere Deployment](#-pythonanywhere-deployment)
- [Docker Deployment](#-docker-deployment-optional)
- [Monitoring and Logs](#-monitoring-and-logs)
- [Troubleshooting](#-troubleshooting)

## ✅ Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Bot token from @BotFather
- [ ] GitHub account (for Railway/Render)
- [ ] Code pushed to GitHub repository
- [ ] Tested bot locally
- [ ] `.env` file configured (don't push to GitHub!)
- [ ] All dependencies in `requirements.txt`

## 🚂 Railway.app Deployment (Recommended)

Railway offers the easiest deployment with generous free tier.

### Why Railway?

- ✅ $5 free credit monthly (500 hours runtime)
- ✅ Automatic deployments from GitHub
- ✅ Built-in environment variable management
- ✅ Persistent storage
- ✅ Easy monitoring and logs

### Step-by-Step Guide

#### 1. Prepare Your Repository

```bash
# Ensure all files are committed
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

#### 2. Create Railway Account

1. Go to [Railway.app](https://railway.app)
2. Click "Login" → "Login with GitHub"
3. Authorize Railway to access your GitHub

#### 3. Create New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `pdf-telegram-bot` repository
4. Railway will detect it's a Python project

#### 4. Configure Environment Variables

1. In your project dashboard, click on your service
2. Go to "Variables" tab
3. Click "New Variable"
4. Add the following:

```
BOT_TOKEN=your_actual_bot_token_here
```

**Important Variables:**
- `BOT_TOKEN` - **REQUIRED** - Your Telegram bot token
- `PYTHONUNBUFFERED=1` - Recommended for better logging

#### 5. Add System Dependencies

Create a file called `nixpacks.toml` in your project root:

```toml
[phases.setup]
aptPkgs = ["poppler-utils", "ghostscript"]

[start]
cmd = "python bot.py"
```

Commit and push:
```bash
git add nixpacks.toml
git commit -m "Add Railway configuration"
git push
```

#### 6. Deploy

Railway will automatically:
- Detect Python
- Install dependencies from `requirements.txt`
- Install poppler-utils
- Start your bot with `python bot.py`

**Watch the deployment:**
- Go to "Deployments" tab
- Click on the latest deployment
- Monitor logs in real-time

#### 7. Verify Deployment

1. Check deployment status (should be "Success")
2. View logs to ensure bot started
3. Test bot on Telegram by sending `/start`

### Railway CLI (Alternative Method)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to existing project or create new
railway link

# Add environment variables
railway variables set BOT_TOKEN=your_token_here

# Deploy
railway up

# View logs
railway logs
```

### Managing Your Bot on Railway

**View Logs:**
```bash
railway logs
# or via web dashboard → Deployments → View Logs
```

**Restart Bot:**
```bash
railway restart
# or via web dashboard → click "Restart"
```

**Update Environment Variables:**
- Dashboard → Variables → Edit
- Or use CLI: `railway variables set KEY=value`

## 🎨 Render.com Deployment

Render provides robust free tier with automatic SSL and monitoring.

### Why Render?

- ✅ 750 hours free per month
- ✅ Automatic deployments from GitHub
- ✅ Built-in SSL certificates
- ✅ Easy scaling options

### Step-by-Step Guide

#### 1. Create Render Account

1. Go to [Render.com](https://render.com)
2. Click "Get Started"
3. Sign up with GitHub

#### 2. Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `pdf-telegram-bot` repo
4. Click "Connect"

#### 3. Configure Service

Fill in the following details:

**Basic Settings:**
- **Name:** `pdf-telegram-bot` (or your preferred name)
- **Environment:** `Python 3`
- **Region:** Choose closest to your users
- **Branch:** `main`

**Build & Deploy:**
- **Build Command:**
  ```bash
  apt-get update && apt-get install -y poppler-utils && pip install -r requirements.txt
  ```

- **Start Command:**
  ```bash
  python bot.py
  ```

#### 4. Add Environment Variables

In "Environment Variables" section:

1. Click "Add Environment Variable"
2. Add:
   - **Key:** `BOT_TOKEN`
   - **Value:** `your_actual_bot_token_here`
3. Add:
   - **Key:** `PYTHON_VERSION`
   - **Value:** `3.9.18`

#### 5. Select Plan

- Choose **Free** plan
- Note: Free tier apps spin down after 15 minutes of inactivity
- They auto-wake when receiving requests

#### 6. Deploy

1. Click "Create Web Service"
2. Render will start building and deploying
3. Monitor progress in the logs

#### 7. Keep Bot Awake (Optional)

Free tier bots sleep after inactivity. To keep them awake:

**Option 1: Use Cron Jobs Service**

Create a `render.yaml` in your repository:

```yaml
services:
  - type: web
    name: pdf-telegram-bot
    env: python
    buildCommand: "apt-get update && apt-get install -y poppler-utils && pip install -r requirements.txt"
    startCommand: "python bot.py"
    envVars:
      - key: BOT_TOKEN
        sync: false
```

**Option 2: External Ping Service**

Use [UptimeRobot](https://uptimerobot.com) to ping your service every 5 minutes.

### Managing Your Bot on Render

**View Logs:**
- Dashboard → Select your service → Logs tab

**Manual Deploy:**
- Dashboard → Select your service → Manual Deploy button

**Environment Variables:**
- Dashboard → Select your service → Environment tab

**Restart:**
- Dashboard → Select your service → Manual Deploy → "Clear build cache & deploy"

## 🐍 PythonAnywhere Deployment

PythonAnywhere is great for Python applications with simple setup.

### Why PythonAnywhere?

- ✅ Free tier available
- ✅ No credit card required
- ✅ Built-in Python environment
- ✅ Web-based file editor

### Step-by-Step Guide

#### 1. Create Account

1. Go to [PythonAnywhere.com](https://www.pythonanywhere.com)
2. Click "Pricing & signup"
3. Choose "Create a Beginner account" (Free)
4. Complete registration

#### 2. Upload Your Code

**Method 1: Git Clone (Recommended)**

1. Go to "Consoles" → "Bash"
2. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/pdf-telegram-bot.git
   cd pdf-telegram-bot
   ```

**Method 2: Upload Files**

1. Go to "Files" tab
2. Click "Upload a file"
3. Upload all project files

#### 3. Install System Dependencies

In the Bash console:
```bash
# Unfortunately, free tier doesn't allow poppler installation
# You'll need to use paid tier ($5/month) for system packages

# For paid accounts:
# Contact support to install poppler-utils
```

**Note:** Free PythonAnywhere accounts cannot install system packages like poppler-utils, which is required for pdf2image. Consider upgrading to a paid account or using Railway/Render instead.

#### 4. Create Virtual Environment

```bash
cd ~/pdf-telegram-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. Configure Environment Variables

```bash
# Create .env file
nano .env

# Add your bot token:
BOT_TOKEN=your_actual_bot_token_here

# Save and exit (Ctrl+X, Y, Enter)
```

#### 6. Run Bot as Always-On Task

For paid accounts:

1. Go to "Tasks" tab
2. Create new task
3. Set command: `/home/yourusername/pdf-telegram-bot/venv/bin/python /home/yourusername/pdf-telegram-bot/bot.py`
4. Save

For free accounts:

1. Keep Bash console open
2. Run: `python bot.py`
3. Note: Console will timeout after inactivity

**Better Alternative:** Use Railway or Render for free tier with full support.

## 🐳 Docker Deployment (Optional)

For advanced users who want containerized deployment.

### Dockerfile

Create `Dockerfile` in project root:

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create temp directory
RUN mkdir -p /tmp/pdf_bot_temp

# Run bot
CMD ["python", "bot.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  bot:
    build: .
    container_name: pdf-telegram-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - /tmp/pdf_bot_temp:/tmp/pdf_bot_temp
```

### Deploy with Docker

```bash
# Build image
docker build -t pdf-telegram-bot .

# Run container
docker run -d \
  --name pdf-bot \
  --env-file .env \
  --restart unless-stopped \
  pdf-telegram-bot

# View logs
docker logs -f pdf-bot

# Stop
docker stop pdf-bot

# Start
docker start pdf-bot
```

### Docker Compose

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

## 📊 Monitoring and Logs

### Railway Logs

```bash
# CLI
railway logs

# Web Dashboard
Dashboard → Deployments → Click deployment → Logs
```

### Render Logs

```bash
# Web Dashboard only
Dashboard → Service → Logs tab
# Use filter options for specific log levels
```

### PythonAnywhere Logs

```bash
# Console logs
cat ~/pdf-telegram-bot/bot.log

# Error logs
~/pdf-telegram-bot/error.log
```

### Log Analysis Tips

**Common Log Messages:**

✅ **Success:**
```
INFO - Starting PDF Tools Bot v1.0.0...
INFO - Bot is starting...
INFO - Cleanup scheduler started
```

❌ **Errors:**
```
ERROR - Configuration validation failed!
# Solution: Check BOT_TOKEN in environment variables

ERROR - poppler not found
# Solution: Install poppler-utils system package

ERROR - [Errno 13] Permission denied
# Solution: Check file permissions on temp directory
```

## 🔧 Troubleshooting

### Common Deployment Issues

#### 1. Bot Not Starting

**Symptoms:** Deployment succeeds but bot doesn't respond

**Solutions:**
```bash
# Check logs for errors
railway logs  # or render logs

# Verify bot token
railway variables get BOT_TOKEN

# Test bot token with curl
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

#### 2. Poppler Not Found

**Symptoms:** `Error: poppler not found` in logs

**Solutions:**

**Railway:** Add `nixpacks.toml`:
```toml
[phases.setup]
aptPkgs = ["poppler-utils", "ghostscript"]
```

**Render:** Update build command:
```bash
apt-get update && apt-get install -y poppler-utils && pip install -r requirements.txt
```

**Docker:** Ensure `RUN apt-get install -y poppler-utils` in Dockerfile

#### 3. Import Errors

**Symptoms:** `ModuleNotFoundError: No module named 'telegram'`

**Solution:**
```bash
# Verify requirements.txt is present and correct
cat requirements.txt

# Force reinstall
pip install -r requirements.txt --force-reinstall
```

#### 4. File Permission Errors

**Symptoms:** `Permission denied` when writing files

**Solution:**
```bash
# Check temp directory permissions
ls -la /tmp/pdf_bot_temp

# Fix permissions
chmod 755 /tmp/pdf_bot_temp

# Or set different temp directory in config.py
TEMP_DIR = Path("/home/user/tmp/pdf_bot")
```

#### 5. Bot Timeout on Render Free Tier

**Symptoms:** Bot becomes unresponsive after 15 minutes

**Solution:**
- Upgrade to paid tier, OR
- Use Railway (better free tier), OR
- Implement keep-alive ping service

### Getting More Help

**Check logs first:**
- Railway: `railway logs`
- Render: Dashboard → Logs
- Docker: `docker logs pdf-bot`

**Common Solutions:**
1. Restart the service
2. Check environment variables
3. Verify all dependencies installed
4. Review recent code changes
5. Test locally first

**Need Support?**
- GitHub Issues: [Create an issue](https://github.com/yourusername/pdf-telegram-bot/issues)
- Telegram: Contact @your_username
- Email: your.email@example.com

## 🎉 Post-Deployment

### Best Practices

1. **Monitor Regularly**
   - Check logs daily for errors
   - Monitor resource usage
   - Track user feedback

2. **Keep Updated**
   - Update dependencies regularly
   - Monitor security advisories
   - Test updates locally first

3. **Backup Configuration**
   - Save environment variables
   - Document any customizations
   - Keep deployment notes

4. **Performance Optimization**
   - Monitor memory usage
   - Optimize file handling
   - Implement rate limiting if needed

### Scaling Tips

**When to Scale:**
- Consistent high CPU usage
- Memory warnings in logs
- Slow response times
- Many concurrent users (100+)

**How to Scale:**
- Upgrade to paid tier
- Add more workers
- Implement caching
- Optimize image processing
- Use external storage for large files

---

**Congratulations! Your bot is now deployed and running! 🎉**

[⬆ Back to Top](#-deployment-guide---pdf-tools-telegram-bot)
