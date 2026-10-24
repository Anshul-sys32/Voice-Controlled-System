import subprocess
import platform
import shlex
import re
from difflib import get_close_matches


APP_MAP = {
    "brave": "brave",
    "browser": "brave",
    "chrome": "google-chrome",
    "firefox": "firefox",

    "code": "code",
    "vscode": "code",

    "vlc": "vlc",
    "obs": "obs",

    "terminal": "konsole",
    "file manager": "dolphin",

    "discord": "discord",
    "obsidian": "obsidian",

    "htop": "konsole -e htop"
}


def resolve_app(app_name):
    if app_name in APP_MAP:
        return APP_MAP[app_name]

    match = get_close_matches(app_name, APP_MAP.keys(), n=1, cutoff=0.6)
    if match:
        return APP_MAP[match[0]]

    return app_name


class Executor:

    def __init__(self):
        self.running_apps = {}

    def open_app(self, app_name: str):

        # sanitize
        app_name = re.sub(r"[^\w\s-]", "", app_name)
        app_name = re.sub(r"\s+", " ", app_name).strip().lower()

        command = resolve_app(app_name)

        print(f"Trying to open: {command}")

        try:
            if platform.system() == "Linux":
                cmd_parts = shlex.split(command)
                process = subprocess.Popen(cmd_parts)

            elif platform.system() == "Windows":
                process = subprocess.Popen(command)

            elif platform.system() == "Darwin":
                process = subprocess.Popen(["open", "-a", command])

            self.running_apps[app_name] = process

        except Exception as e:
            print(f"Failed to open {command}: {e}")

    def close_app(self, app_name: str):

        app_name = app_name.lower()

        process = self.running_apps.get(app_name)

        if process:
            process.terminate()
            del self.running_apps[app_name]
            print(f"Closed {app_name}")
            return

        try:
            if platform.system() == "Linux":
                subprocess.Popen(["pkill", "-f", app_name])

            elif platform.system() == "Windows":
                subprocess.Popen(["taskkill", "/IM", f"{app_name}.exe", "/F"])

            elif platform.system() == "Darwin":
                subprocess.Popen(["pkill", app_name])

        except Exception as e:
            print(f"Failed to close {app_name}: {e}")