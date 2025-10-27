"""
System check utility for PDF Telegram Bot.
Verifies that all required system dependencies are available.
"""

import subprocess
import sys


def check_ghostscript() -> bool:
    """Check if Ghostscript is available."""
    try:
        result = subprocess.run(
            ['gs', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Ghostscript found: version {version}")
            return True
        else:
            print("❌ Ghostscript command failed")
            return False
    except FileNotFoundError:
        print("❌ Ghostscript (gs) not found in PATH")
        print("📦 Install with: apt-get install ghostscript")
        return False
    except Exception as e:
        print(f"❌ Error checking Ghostscript: {e}")
        return False


def check_poppler() -> bool:
    """Check if poppler-utils is available."""
    try:
        result = subprocess.run(
            ['pdftoppm', '-v'],
            capture_output=True,
            text=True,
            timeout=5
        )
        # pdftoppm returns version info on stderr
        if 'pdftoppm' in result.stderr.lower() or result.returncode == 0:
            print(f"✅ Poppler-utils found")
            return True
        else:
            print("❌ Poppler-utils command failed")
            return False
    except FileNotFoundError:
        print("❌ Poppler-utils (pdftoppm) not found in PATH")
        print("📦 Install with: apt-get install poppler-utils")
        return False
    except Exception as e:
        print(f"❌ Error checking Poppler-utils: {e}")
        return False


def run_system_checks() -> bool:
    """
    Run all system checks.
    
    Returns:
        bool: True if all required dependencies are available
    """
    print("\n" + "="*50)
    print("🔍 Running System Dependency Checks")
    print("="*50)
    
    checks = {
        'Ghostscript': check_ghostscript(),
        'Poppler-utils': check_poppler()
    }
    
    print("\n" + "="*50)
    print("📊 System Check Summary")
    print("="*50)
    
    for name, status in checks.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name}: {'OK' if status else 'MISSING'}")
    
    all_passed = all(checks.values())
    
    if not all_passed:
        print("\n⚠️  WARNING: Some dependencies are missing!")
        print("📋 Bot will work with limited functionality:")
        if not checks['Ghostscript']:
            print("   • PDF compression will use fallback method (less effective)")
        if not checks['Poppler-utils']:
            print("   • PDF to image conversion will fail")
        print("\n💡 For full functionality, install missing dependencies.")
    else:
        print("\n✅ All system dependencies are available!")
    
    print("="*50 + "\n")
    
    # Only fail if poppler is missing (critical)
    # Ghostscript is optional (has fallback)
    if not checks['Poppler-utils']:
        print("❌ CRITICAL: Poppler-utils is required for basic functionality!")
        print("🛑 Bot cannot start without it.\n")
        return False
    
    return True


if __name__ == '__main__':
    if not run_system_checks():
        sys.exit(1)