"""Open apps and websites. Add your own apps in config.toml under [apps]."""
import os
import platform
import shutil
import subprocess
import webbrowser

from jarvis.skills import skill

# Built-in shortcuts. Users can add or override them in config.toml.
DEFAULT_APPS = {
    "Windows": {
        "notepad": "notepad",
        "calculator": "calc",
        "file explorer": "explorer",
        "explorer": "explorer",
        "paint": "mspaint",
        "settings": "ms-settings:",
        "task manager": "taskmgr",
        "command prompt": "cmd",
    },
    "Darwin": {"calculator": "Calculator", "notes": "Notes", "finder": "Finder", "safari": "Safari"},
    "Linux": {"calculator": "gnome-calculator", "files": "nautilus", "terminal": "gnome-terminal"},
}

WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "gmail": "https://mail.google.com",
}


def launch(target: str) -> None:
    system = platform.system()
    if system == "Windows":
        os.startfile(target)  # type: ignore[attr-defined]
    elif system == "Darwin":
        subprocess.Popen(["open", "-a", target] if not target.startswith("/") else ["open", target])
    else:
        subprocess.Popen([target], start_new_session=True)


@skill(r"^(?:open|launch|start) (?:the )?(?P<name>.+)$", name="open", help="open <app or website>")
def open_app(match, ctx):
    name = match.group("name").strip()
    apps = {**DEFAULT_APPS.get(platform.system(), {}), **{k.lower(): v for k, v in ctx.config.apps.items()}}

    if name in apps:
        try:
            launch(apps[name])
            return f"Opening {name}."
        except Exception as e:
            return f"I couldn't open {name}: {e}"

    if name in WEBSITES:
        webbrowser.open(WEBSITES[name])
        return f"Opening {name}."

    if shutil.which(name):
        subprocess.Popen([name], start_new_session=True)
        return f"Opening {name}."

    return f"I don't know how to open '{name}' yet. Add it under [apps] in config.toml."
