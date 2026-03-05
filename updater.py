"""
madhushalasoftwareGpt — Auto Updater
Checks GitHub for new version → downloads & restarts EXE automatically
"""
import os
import sys
import time
import shutil
import threading
import subprocess
import urllib.request
import urllib.error

# ── GitHub Config ──────────────────────────────────────────────────
GITHUB_USER    = "mca70"
GITHUB_REPO    = "madhushalasoftwareGpt"
VERSION_URL    = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/main/version.txt"
EXE_URL        = f"https://github.com/{GITHUB_USER}/{GITHUB_REPO}/releases/latest/download/madhushalasoftwareGpt.exe"
LOCAL_VERSION_FILE = "version.txt"
APP_NAME       = "madhushalasoftwareGpt.exe"
CHECK_INTERVAL = 60 * 60  # check every 1 hour

def get_local_version():
    try:
        base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        vfile = os.path.join(base, LOCAL_VERSION_FILE)
        with open(vfile, "r") as f:
            return f.read().strip()
    except:
        return "0.0.0"

def get_remote_version():
    try:
        req = urllib.request.Request(VERSION_URL, headers={"Cache-Control": "no-cache"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode().strip()
    except:
        return None

def version_tuple(v):
    try:
        return tuple(int(x) for x in v.split("."))
    except:
        return (0, 0, 0)

def download_new_exe(callback=None):
    """Download new EXE to temp file, then replace current"""
    try:
        exe_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else APP_NAME)
        tmp_path = exe_path + ".new"
        old_path = exe_path + ".old"

        if callback: callback("downloading")

        urllib.request.urlretrieve(EXE_URL, tmp_path)

        if callback: callback("installing")

        # Rename current → .old, new → current
        if os.path.exists(old_path):
            os.remove(old_path)
        if os.path.exists(exe_path):
            os.rename(exe_path, old_path)
        os.rename(tmp_path, exe_path)

        if callback: callback("done")
        return True, exe_path
    except Exception as e:
        if callback: callback(f"error:{e}")
        return False, str(e)

def restart_app(exe_path):
    """Launch new EXE and exit current"""
    time.sleep(2)
    subprocess.Popen([exe_path])
    os._exit(0)

def check_for_update(on_update_found=None, on_no_update=None):
    """Check GitHub for update — call callbacks"""
    local  = get_local_version()
    remote = get_remote_version()
    if remote and version_tuple(remote) > version_tuple(local):
        if on_update_found:
            on_update_found(local, remote)
        return True, local, remote
    else:
        if on_no_update:
            on_no_update(local)
        return False, local, remote

def start_background_checker(on_update_found=None):
    """Run periodic update check in background thread"""
    def loop():
        while True:
            try:
                found, local, remote = check_for_update()
                if found and on_update_found:
                    on_update_found(local, remote)
            except:
                pass
            time.sleep(CHECK_INTERVAL)
    t = threading.Thread(target=loop, daemon=True)
    t.start()
