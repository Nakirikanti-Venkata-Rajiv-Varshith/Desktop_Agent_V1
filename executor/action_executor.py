from llm.parser import ActionPlanSchema, ActionItem
from executor.app_launcher import AppLauncher
from executor.browser_controller import BrowserController
from tools.logger import agent_logger

class ActionExecutor:
    """Sequential engine loop routing abstract tasks toward low-level sub-systems."""
    
    def __init__(self):
        self.launcher = AppLauncher()
        self.browser = BrowserController()

    def execute(self, plan: ActionPlanSchema, status_callback=None) -> bool:
        """Iterates steps within thread barriers to protect UI stability flags."""
        if not plan.actions:
            agent_logger.warning("Execution schema contains an empty action matrix.")
            if status_callback: status_callback("Plan empty.")
            return False

        for index, item in enumerate(plan.actions, start=1):
            msg = f"Executing sub-task [{index}/{len(plan.actions)}]: {item.action.upper()}"
            agent_logger.info(msg)
            if status_callback: status_callback(msg)
            
            success = self._dispatch_item(item)
            if not success:
                err_msg = f"Pipeline execution failed on step action: {item.action}"
                agent_logger.error(err_msg)
                if status_callback: status_callback(err_msg)
                return False
                
        if status_callback: status_callback("All actions completed successfully.")
        return True

    def _dispatch_item(self, item: ActionItem) -> bool:
        if item.action == "open_app":
            return self.launcher.launch(item.app)
        elif item.action == "open_url":
            return self.browser.open_url(item.url)
        elif item.action == "search":
            return self.browser.search_google(item.query)
        return False