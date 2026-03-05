"""
madhushalasoftwareGpt — Auto Builder
Watches app.py for changes → auto rebuilds EXE
"""
import os
import sys
import time
import subprocess
import hashlib
from datetime import datetime

# ── Config ────────────────────────────────────────────────────────
WATCH_FILE   = "app.py"
APP_NAME     = "madhushalasoftwareGpt"
CHECK_EVERY  = 3   # seconds between checks
BUILD_CMD    = f"pyinstaller --onefile --noconsole --name {APP_NAME} {WATCH_FILE}"

# ── Colors for terminal ───────────────────────────────────────────
def green(t):  return f"\033[92m{t}\033[0m"
def yellow(t): return f"\033[93m{t}\033[0m"
def red(t):    return f"\033[91m{t}\033[0m"
def cyan(t):   return f"\033[96m{t}\033[0m"
def bold(t):   return f"\033[1m{t}\033[0m"

def get_file_hash(path):
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def log(msg, kind="info"):
    now = datetime.now().strftime("%H:%M:%S")
    if kind == "ok":      print(f"  [{now}] {green('✔')} {msg}")
    elif kind == "warn":  print(f"  [{now}] {yellow('⚡')} {msg}")
    elif kind == "error": print(f"  [{now}] {red('✘')} {msg}")
    elif kind == "build": print(f"  [{now}] {cyan('🔨')} {msg}")
    else:                 print(f"  [{now}]    {msg}")

def run_build():
    log("Change detected in app.py!", "warn")
    log("Starting EXE build... please wait", "build")
    print()

    # Clean old build
    for folder in ["dist", "build"]:
        if os.path.exists(folder):
            subprocess.run(f"rmdir /s /q {folder}", shell=True, capture_output=True)
    spec = f"{APP_NAME}.spec"
    if os.path.exists(spec):
        os.remove(spec)

    # Build
    start = time.time()
    result = subprocess.run(BUILD_CMD, shell=True, capture_output=True, text=True)
    elapsed = round(time.time() - start, 1)

    if result.returncode == 0:
        exe_path = os.path.abspath(f"dist\\{APP_NAME}.exe")
        print()
        print("  " + "━"*52)
        log(f"BUILD SUCCESSFUL in {elapsed}s! 🎉", "ok")
        log(f"EXE ready: dist\\{APP_NAME}.exe", "ok")
        print("  " + "━"*52)
        print()
    else:
        print()
        log(f"BUILD FAILED after {elapsed}s", "error")
        log("Error details:", "error")
        for line in result.stderr.split("\n")[-10:]:
            if line.strip():
                print(f"    {red(line)}")
        print()

def main():
    os.system("cls" if os.name=="nt" else "clear")
    print()
    print("  " + "━"*52)
    print(bold(f"  🍷 madhushalasoftwareGpt — Auto Builder"))
    print("  " + "━"*52)
    print(f"  {cyan('Watching:')}  {WATCH_FILE}")
    print(f"  {cyan('Output:')}    dist\\{APP_NAME}.exe")
    print(f"  {cyan('Check:')}     Every {CHECK_EVERY} seconds")
    print("  " + "━"*52)
    print(f"  {yellow('Save app.py → EXE rebuilds automatically!')}")
    print(f"  {red('Press Ctrl+C to stop')}")
    print("  " + "━"*52)
    print()

    if not os.path.exists(WATCH_FILE):
        log(f"{WATCH_FILE} not found in current directory!", "error")
        log("Run this script from your project folder.", "error")
        input("\n  Press Enter to exit...")
        sys.exit(1)

    last_hash = get_file_hash(WATCH_FILE)
    log(f"Watching {WATCH_FILE} for changes...", "ok")
    log("Initial build starting now...", "build")
    print()
    run_build()

    try:
        while True:
            time.sleep(CHECK_EVERY)
            current_hash = get_file_hash(WATCH_FILE)
            if current_hash and current_hash != last_hash:
                last_hash = current_hash
                run_build()
                log(f"Watching {WATCH_FILE} for changes...", "ok")
    except KeyboardInterrupt:
        print()
        log("Auto-builder stopped. Goodbye! 🍷", "warn")
        print()

if __name__ == "__main__":
    main()
