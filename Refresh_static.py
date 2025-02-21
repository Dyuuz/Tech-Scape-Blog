import os
import time
import platform
import shutil
from pathlib import Path

def clear_browser_cache():
    print("🧹 Clearing browser cache...")

    system = platform.system()

    # Conditionals for different OS
    if system == "Windows":
        caches = [
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache"),
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache"),
            os.path.expandvars(r"%LOCALAPPDATA%\Mozilla\Firefox\Profiles")
        ]

    elif system == "Linux":
        caches = [
            os.path.expanduser("~/.cache/google-chrome/Default/Cache"),
            os.path.expanduser("~/.cache/mozilla/firefox/")
        ]

    elif system == "Darwin":
        caches = [
            os.path.expanduser("~/Library/Caches/Google/Chrome/Default/Cache"),
            os.path.expanduser("~/Library/Caches/Firefox/Profiles/")
        ]

    else:
        print("❌ Unsupported OS")
        return

    # Clear Chrome,Edge and Firefox cache
    for cache_dir in caches:
        if os.path.exists(cache_dir):
            try:
                # If Firefox exists, clear all cache directories
                if "firefox" in cache_dir.lower():
                    for profile_cache in Path(cache_dir).glob("*/cache2/entries"):
                        shutil.rmtree(profile_cache, ignore_errors=True)
                        print(f"✅ Cleared Firefox cache: {profile_cache}")
                # Checks for other OS
                else:
                    shutil.rmtree(cache_dir, ignore_errors=True)
                    print(f"✅ Cleared cache: {cache_dir}")

            except Exception as e:
                print(f"⚠️ Failed to clear cache: {cache_dir}\n{e}")
                
def install_cachebuster():
    print("Installing django-cachebuster...")
    os.system("pip install django-cachebuster")
    

def automate_static_refresh():
    # Call Django-cachebuster installation function
    install_cachebuster()
    time.sleep(3)

    print("Starting Static File Refresh Process...")

    # Call clear_browser_cache function
    clear_browser_cache()
    time.sleep(3)

    # Restart Django server
    print("Starting Django server...")
    
    # Close any running server process
    os.system("pkill -f runserver")  
    
    # Run server automatically
    os.system("python manage.py runserver")

    print("Static files refreshed and server restarted successfully!")

if __name__ == "__main__":
    automate_static_refresh()
