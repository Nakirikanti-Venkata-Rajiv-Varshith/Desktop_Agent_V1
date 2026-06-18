from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import QThread, pyqtSignal
from ui.prompt_bar import PromptBar
from planner.task_planner import TaskPlanner
from executor.action_executor import ActionExecutor
from tools.logger import agent_logger
import subprocess

class AgentWorker(QThread):
    """Background computation runner safeguarding UI layout components from locking loops."""
    status_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)

    def __init__(self, planner: TaskPlanner, executor: ActionExecutor, text: str):
        super().__init__()
        self.planner = planner
        self.executor = executor
        self.text = text

    def run(self):
        try:
            self.status_signal.emit("Analyzing input patterns via local LLM model...")
            plan = self.planner.create_plan(self.text)
            
            self.status_signal.emit("Valid payload compiled. Handing control over to executor...")
            success = self.executor.execute(plan, status_callback=self.status_signal.emit)
            self.finished_signal.emit(success)
        except Exception as e:
            agent_logger.error(f"Worker runtime exception captured: {str(e)}")
            self.status_signal.emit(f"Error: {str(e)}")
            self.finished_signal.emit(False)


class MainWindow(QMainWindow):
    """Core window module exposing controls and monitoring displays."""
    
    def __init__(self, planner: TaskPlanner, executor: ActionExecutor):
        super().__init__()
        self.planner = planner
        self.executor = executor
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("AI Computer Desktop Agent - V1 Console")
        self.resize(650, 450)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        
        self.status_bar = QLabel("System Ready")
        self.status_bar.setStyleSheet("color: #7f8c8d; font-style: italic; padding: 2px;")

        self.prompt_bar = PromptBar()
        self.prompt_bar.command_submitted.connect(self._process_command)

        layout.addWidget(QLabel("Execution Engine Stream Output:"))
        layout.addWidget(self.chat_display)
        layout.addWidget(self.status_bar)
        layout.addWidget(self.prompt_bar)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _process_command(self, text: str):

        cleaned_text = text.strip().lower()

        if cleaned_text in ["clear", "cls", "reset"]:

            self.chat_display.clear()

            self.status_bar.setText(
                "Console history cleared."
            )

            return

        if cleaned_text in ["exit", "quit", "close"]:

            self.close()

            return

        self.chat_display.append(
            f"<b>User:</b> {text}"
        )

        self.prompt_bar.set_running_state(
            True
        )

        self.worker = AgentWorker(
            self.planner,
            self.executor,
            text
        )

        self.worker.status_signal.connect(
            self._update_status
        )

        self.worker.finished_signal.connect(
            self._handle_worker_completion
        )

        self.worker.start()

    def _update_status(self, status: str):
        self.status_bar.setText(status)
        self.chat_display.append(f"<font color='#2980b9'>[System]</font> {status}")

    def _handle_worker_completion(self, success: bool):
        self.prompt_bar.set_running_state(False)
        if success:
            self.status_bar.setText("Task cycle finished successfully.")
        else:
            self.status_bar.setText("Cycle terminated early due to processing faults.")

    def closeEvent(self, event):

        try:

            subprocess.run(
                ["ollama", "stop", "qwen3:8b"],
                timeout=10
            )

            agent_logger.info(
                "Ollama model unloaded successfully."
            )

        except Exception as e:

            agent_logger.warning(
                f"Failed to unload Ollama model: {str(e)}"
            )

        event.accept()