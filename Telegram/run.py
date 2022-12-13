import os
import platform
import subprocess
from pathlib import Path


def main():
    is_linux = True
    if platform.system().lower() == "windows":
        is_linux = False
    if not os.path.exists(Path("venv")):

        subprocess.run(["python -m venv venv"])
        if is_linux:
            subprocess.run(["source", "venv/bin/activate", "&&", "pip",  "install", "-r", "requirements.txt"])
        else:
            subprocess.run(["venv\\Scripts\\activate", "&&", "pip",  "install", "-r", "requirements.txt"])
    if is_linux:
        subprocess.run(["./telegram_bot_run"])
    else:
        subprocess.run(["run.bat"])
