import subprocess

class AppTool:

    APPS = {
        "chrome":"chromium",
        "chromium": "chromium",
        "firefox":"firefox",
        "terminal":"gnome-terminal",
        "vscode":"code"
    }

    @staticmethod
    def open(app):

        cmd = AppTool.APPS.get(app)

        if not cmd:
            return f"Unknown App: {app}"

        subprocess.Popen([cmd])

        return f"Opened {app}"