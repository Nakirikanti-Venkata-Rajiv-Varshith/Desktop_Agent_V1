import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from planner.task_planner import TaskPlanner
from executor.action_executor import ActionExecutor
from tools.logger import agent_logger
from utils.browser_bootstrap import ensure_cdp_running

def main():
    """Main application lifecycle entry point initialization block."""
    agent_logger.info("========================================")
    agent_logger.info("Initializing AI Computer Agent V1 Engine Bootstrap")
    agent_logger.info("========================================")

    ensure_cdp_running()
    app = QApplication(sys.argv)
    
    # Core system components instantiation
    planner = TaskPlanner()
    executor = ActionExecutor()
    
    # UI Setup
    window = MainWindow(planner, executor)
    window.show()
    
    agent_logger.info("System fully operational. Displaying UI interface windows.")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()