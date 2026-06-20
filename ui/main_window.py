import os
import subprocess
import time
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import QThread, pyqtSignal
from ui.prompt_bar import PromptBar
from planner.task_planner import TaskPlanner
from executor.action_executor import ActionExecutor
from tools.logger import agent_logger
import subprocess
from ui.command_splitter import split_commands
import time

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
            # Prevent splitting conversational requests like "summarize and explain" 
            # into separate tool executions if it contains specific keywords
            if "summarize" in self.text.lower() and "explain" in self.text.lower():
                commands = [self.text]  # Treat it as a single cohesive request
            else:
                commands = split_commands(self.text)

            overall_success = True

            for command in commands:
                self.status_signal.emit(f"Analyzing: {command}")
                
                plan = self.planner.create_plan(command)
                self.status_signal.emit("Valid payload compiled. Handing control over to executor...")

                # 1. Modify execute_task_plan inside your pipeline or loop to let us capture the payload string
                # Since we want to pass the result back out, we look at the executor steps
                for step in plan.steps:
                    self.status_signal.emit(f"Executing Tool: {step.tool}.{step.function}")
                    
                    # Run the single tool step execution
                    # Note: To ensure your executor returns the text string data, ensure execute_single returns (success, result)
                    # For now, we will inspect the file path directly to be 100% bulletproof:
                    try:
                        # Let the tool run and save the file
                        success = self.executor.execute_single(step, status_callback=None)
                        
                        txt_path = "data/yt_transcript.txt"
                        # If a transcript was freshly written to our cache folder, invoke Ollama to respond!
                        if success and step.tool == "youtube" and os.path.exists(txt_path) and os.path.getsize(txt_path) > 0:
                            self.status_signal.emit("Transcript file ready. Querying local Ollama (qwen3:8b) for final summary...")
                            
                            with open(txt_path, "r", encoding="utf-8") as f:
                                transcript_content = f.read()

                            # Build the clean generation prompt
                            ollama_prompt = (
                                f"The user asked: '{self.text}' based on the active video.\n"
                                f"Here is the raw transcript context to analyze and answer the question:\n\n"
                                f"--- TRANSCRIPT START ---\n{transcript_content}\n--- TRANSCRIPT END ---"
                            )

                            # Directly query your local Ollama endpoint from the worker thread
                            import requests
                            response = requests.post(
                                "http://localhost:11434/api/generate",
                                json={
                                    "model": "qwen3:8b",
                                    "prompt": ollama_prompt,
                                    "stream": False
                                },
                                timeout=60
                            )

                            if response.status_code == 200:
                                final_reply = response.json().get("response", "")
                                # Send the actual final summary text up to the PyQt6 window!
                                self.status_signal.emit(f"\n<b>AI Agent:</b>\n{final_reply}")
                            else:
                                self.status_signal.emit(f"Ollama generation failed with code: {response.status_code}")
                        else:
                            # If it was a regular non-youtube tool, just notify completion
                            overall_success = overall_success and success
                            
                    except Exception as step_error:
                        self.status_signal.emit(f"Step execution error: {str(step_error)}")
                        overall_success = False

                time.sleep(1)

            self.finished_signal.emit(overall_success)

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
        
        # Run startup wipe sequence right as the window initializes
        self._initialize_session()
        self._init_ui()

    def _initialize_session(self):
        """Wipes old data files on every agent startup."""
        txt_path = "data/yt_transcript.txt"
        if os.path.exists(txt_path):
            try:
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write("")
                agent_logger.info("Stale session transcript data wiped clean on initialization.")
            except Exception as e:
                agent_logger.warning(f"Failed to clean data cache file during startup: {str(e)}")

    def _cleanup_session(self):
        """Completely deletes the temporary transcript file when exiting."""
        txt_path = "data/yt_transcript.txt"
        if os.path.exists(txt_path):
            try:
                os.remove(txt_path)
                agent_logger.info("Session file data cleanly purged from disk.")
            except Exception as e:
                agent_logger.warning(f"Error during session file cleanup: {str(e)}")

    def _init_ui(self):
        self.setWindowTitle("AI Computer Desktop Agent - V1 Console")
        self.resize(650, 450)

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        
        self.status_bar = QLabel("System Ready")
        self.status_bar.setWordWrap(True)
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
            self.status_bar.setText("Console history cleared.")
            return

        if cleaned_text in ["exit", "quit", "close"]:
            self.close()
            return

        self.chat_display.append(f"<b>User:</b> {text}")
        self.prompt_bar.set_running_state(True)

        self.worker = AgentWorker(self.planner, self.executor, text)
        self.worker.status_signal.connect(self._update_status)
        self.worker.finished_signal.connect(self._handle_worker_completion)
        self.worker.start()

    def _update_status(self, status: str):
        # Check if this is the large text summary block from the AI Agent
        if "<b>AI Agent:</b>" in status or len(status) > 150:
            # 1. Separate the header from the actual response body
            header = "<b><font color='#2980b9'>[System] AI Agent:</font></b><br>"
            body = status.replace("<b>AI Agent:</b>", "").strip()
            
            # 2. Convert markdown newlines into clean HTML paragraph breaks for PyQt6
            formatted_body = body.replace("\n", "<br>")
            
            # 3. Append the beautifully spaced HTML block to your chat layout
            self.chat_display.append(f"{header}{formatted_body}<br>")
            self.status_bar.setText("Model finished generating response.")
        else:
            # Normal small system updates fit perfectly in the bottom bar
            self.status_bar.setText(status)
            self.chat_display.append(f"<font color='#2980b9'>[System]</font> {status}")

    def _handle_worker_completion(self, success: bool):
        self.prompt_bar.set_running_state(False)
        if success:
            self.status_bar.setText("Task cycle finished successfully.")
        else:
            self.status_bar.setText("Cycle terminated early due to processing faults.")

    def closeEvent(self, event):
        """Triggers automatically when the window is closed."""
        # 1. Clear out the temporary transcript file from disk
        self._cleanup_session()

        # 2. Shut down your local Ollama instance
        try:
            subprocess.run(["ollama", "stop", "qwen3:8b"], timeout=10)
            agent_logger.info("Ollama model unloaded successfully.")
        except Exception as e:
            agent_logger.warning(f"Failed to unload Ollama model: {str(e)}")

        event.accept()