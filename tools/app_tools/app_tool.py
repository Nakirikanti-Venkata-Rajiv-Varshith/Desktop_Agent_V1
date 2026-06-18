import subprocess

class AppTool:

    APPS = {
        "chrome":"chromium",
        "firefox":"firefox",
        "terminal":"gnome-terminal",
        "vscode":"code"
    }

    @staticmethod
    def open(app):

        cmd = AppTool.APPS.get(app)

        if not cmd:
            return "Unknown App"

        subprocess.Popen([cmd])

        return f"Opened {app}"