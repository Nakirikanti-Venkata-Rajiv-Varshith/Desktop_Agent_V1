import subprocess
from config.settings import CHROME_COMMAND, FIREFOX_COMMAND, TERMINAL_COMMAND, VSCODE_COMMAND
from tools.logger import agent_logger

class AppLauncher:
    """Manages process spawning across standard local runtime applications."""
    
    def __init__(self):
        self.app_map = {
            "chrome": CHROME_COMMAND,
            "chromium": CHROME_COMMAND,
            "firefox": FIREFOX_COMMAND,
            "terminal": TERMINAL_COMMAND,
            "vscode": VSCODE_COMMAND
        }

    def launch(self, app_name: str) -> bool:
        """Triggers local execution binaries safely using non-blocking sub-processes."""
        if not app_name:
            return False
            
        normalized_name = app_name.lower().strip()
        binary = self.app_map.get(normalized_name)
        
        if not binary:
            agent_logger.error(f"Application target signature not registered: {app_name}")
            return False
            
        try:
            agent_logger.info(f"Spawning native subprocess: [{binary}]")
            # shell=False (default behavior here) prevents shell injection attacks
            subprocess.Popen([binary], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            agent_logger.error(f"OS Process execution error for binary [{binary}]: {str(e)}")
            return False