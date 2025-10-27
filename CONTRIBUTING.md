# 🤝 Contributing to PDF Tools Telegram Bot

Thank you for considering contributing to this project! We welcome contributions from everyone.

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How Can I Contribute?](#-how-can-i-contribute)
- [Development Setup](#-development-setup)
- [Coding Guidelines](#-coding-guidelines)
- [Submitting Changes](#-submitting-changes)
- [Reporting Bugs](#-reporting-bugs)
- [Suggesting Features](#-suggesting-features)

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information
- Other unprofessional conduct

## 💡 How Can I Contribute?

### Types of Contributions

1. **Bug Reports** - Found a bug? Let us know!
2. **Feature Requests** - Have an idea? Share it!
3. **Code Contributions** - Fix bugs or add features
4. **Documentation** - Improve docs or add examples
5. **Testing** - Test features and report results
6. **Translation** - Help translate bot messages

### Good First Issues

Look for issues tagged with:
- `good first issue` - Perfect for newcomers
- `help wanted` - We need your help!
- `documentation` - Improve docs

## 🛠️ Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/pdf-telegram-bot.git
cd pdf-telegram-bot
```

### 2. Create Development Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Set Up Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 pytest

# Copy environment template
cp .env.example .env
# Add your test bot token
```

### 4. Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

### 5. Run Bot Locally

```bash
python bot.py
```

## 📝 Coding Guidelines

### Python Style Guide

We follow [PEP 8](https://pep8.org/) style guidelines.

**Key Points:**
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to all functions
- Include type hints where appropriate

### Code Formatting

Use `black` for automatic formatting:

```bash
# Format all Python files
black .

# Check formatting without changing files
black --check .
```

### Linting

Use `flake8` to check code quality:

```bash
# Run linter
flake8 .

# With specific rules
flake8 --max-line-length=100 --ignore=E501,W503 .
```

### Example Code Style

```python
"""
Module description here.
"""

from typing import List, Optional
from pathlib import Path


def process_pdf(
    pdf_path: Path,
    output_path: Path,
    quality: str = "default"
) -> bool:
    """
    Process a PDF file with specified quality.
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Path where processed PDF will be saved
        quality: Compression quality ("low", "default", or "high")
        
    Returns:
        bool: True if processing successful, False otherwise
        
    Raises:
        FileNotFoundError: If pdf_path doesn't exist
        ValueError: If quality is invalid
    """
    # Check if file exists
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    # Validate quality parameter
    valid_qualities = ["low", "default", "high"]
    if quality not in valid_qualities:
        raise ValueError(f"Invalid quality: {quality}")
    
    # Process PDF
    try:
        # Processing logic here
        return True
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return False
```

### Documentation Standards

**Function Docstrings:**
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief description of what function does.
    
    Longer description if needed, explaining behavior,
    edge cases, or important notes.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ErrorType: When this error occurs
    """
```

**Inline Comments:**
```python
# Use comments to explain WHY, not WHAT
# Bad: i = i + 1  # Increment i
# Good: i += 1  # Track number of processed files

# Explain complex logic
# Calculate compression ratio as percentage of size reduction
compression_ratio = ((original_size - compressed_size) / original_size) * 100
```

### Git Commit Messages

Format:
```
type: Brief description (50 chars max)

Longer explanation if needed (wrap at 72 chars)
- Bullet points for details
- Reference issues with #123

Fixes #123
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**
```
feat: Add PDF rotation feature

Added ability to rotate PDF pages by 90, 180, or 270 degrees.
- New /rotate command
- Updated help documentation
- Added tests for rotation

Fixes #42

---

fix: Handle corrupted PDF files gracefully

Previously, bot would crash on corrupted PDFs. Now shows
user-friendly error message and cleans up temp files.

Fixes #38

---

docs: Update deployment guide for Railway

Added section on setting environment variables and
troubleshooting common deployment issues.
```

## 📤 Submitting Changes

### Before Submitting

Checklist:
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### Pull Request Process

1. **Update Your Branch**
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Run Tests**
   ```bash
   # Format code
   black .
   
   # Run linter
   flake8 .
   
   # Test locally
   python bot.py
   # Test all features manually
   ```

3. **Push to Your Fork**
   ```bash
   git push origin your-branch
   ```

4. **Create Pull Request**
   - Go to original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added to complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally

## Screenshots (if applicable)

## Related Issues
Fixes #(issue number)
```

5. **Review Process**
   - Maintainers will review your PR
   - Address any requested changes
   - Once approved, it will be merged!

### After Your PR is Merged

```bash
# Update your local repository
git checkout main
git pull upstream main

# Delete your feature branch
git branch -d your-branch
git push origin --delete your-branch
```

## 🐛 Reporting Bugs

### Before Reporting

- Check if bug already reported in [Issues](https://github.com/yourusername/pdf-telegram-bot/issues)
- Test with latest version
- Try to reproduce consistently

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Send file '....'
4. Type command '....'

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Screenshots
If applicable, add screenshots

## Environment
- Bot Version: [e.g. 1.0.0]
- Python Version: [e.g. 3.9.7]
- OS: [e.g. Ubuntu 20.04]
- Hosting: [e.g. Railway, Local]

## Additional Context
Any other context about the problem

## Possible Solution
(Optional) Suggest a fix/reason
```

## 💭 Suggesting Features

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Problem it Solves
What problem does this solve?

## Proposed Solution
How should it work?

## Alternative Solutions
Other approaches you've considered

## Use Cases
Real-world examples of when this would be useful

## Additional Context
Mockups, examples, or references
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_pdf_operations.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Writing Tests

```python
import pytest
from pathlib import Path
from utils.pdf_operations import PDFOperations

def test_merge_pdfs():
    """Test PDF merging functionality"""
    # Setup
    pdf_ops = PDFOperations()
    pdf1 = Path("tests/data/test1.pdf")
    pdf2 = Path("tests/data/test2.pdf")
    output = Path("/tmp/merged.pdf")
    
    # Execute
    result = pdf_ops.merge_pdfs([pdf1, pdf2], output)
    
    # Assert
    assert result is True
    assert output.exists()
    
    # Cleanup
    output.unlink()

def test_merge_pdfs_invalid():
    """Test merging with invalid input"""
    pdf_ops = PDFOperations()
    
    with pytest.raises(ValueError):
        pdf_ops.merge_pdfs([], Path("/tmp/out.pdf"))
```

## 📚 Documentation

### Improving Documentation

- Fix typos and grammar
- Add examples
- Clarify confusing sections
- Add missing information
- Improve code comments

### Documentation Style

- Use clear, simple language
- Include code examples
- Add screenshots where helpful
- Keep formatting consistent
- Update table of contents

## 🌍 Translation

Help translate bot messages to other languages!

1. Copy `locales/en.json` to `locales/YOUR_LANGUAGE.json`
2. Translate all strings
3. Test with your language setting
4. Submit PR

## ❓ Questions?

- Open an issue with "Question:" prefix
- Contact maintainers via email
- Join our community chat

## 🎉 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Thanked in project README

Thank you for contributing! 🙏

---

**Happy Coding! 🚀**

[⬆ Back to Top](#-contributing-to-pdf-tools-telegram-bot)
