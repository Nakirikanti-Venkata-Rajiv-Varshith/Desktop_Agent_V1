import os
import subprocess
import time
import requests
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import QThread, pyqtSignal
from ui.prompt_bar import PromptBar
from planner.task_planner import TaskPlanner
from executor.action_executor import ActionExecutor
from tools.logger import agent_logger
from ui.command_splitter import split_commands

# Import your aesthetic premium style rule configuration
from ui.prompt_window_looks import AESTHETIC_DARK_QSS

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

                for step in plan.steps:
                    self.status_signal.emit(f"Executing Tool: {step.tool}.{step.function}")
                    
                    try:
                        # Let the tool run and save the file cache
                        success = self.executor.execute_single(step, status_callback=self.status_signal.emit)
                        
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
        
        # Apply the aesthetic dark stylesheet skin globally
        self.setStyleSheet(AESTHETIC_DARK_QSS)

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
        self.resize(680, 480) # Modern roomier workspace proportions

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(22, 22, 22, 22)

        # Header Label
        header_lbl = QLabel("SYSTEM LIVE STREAM OUTPUT")
        header_lbl.setObjectName("HeaderLabel") # Connects widget style to custom QSS rules
        layout.addWidget(header_lbl)

        # Main Chat Display Monitor
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Glow Indicator Status Bar
        self.status_bar = QLabel("● SYSTEM READY")
        self.status_bar.setObjectName("StatusBar") # Connects widget style to custom QSS rules
        self.status_bar.setWordWrap(True)
        self.status_bar.setProperty("state", "ready") # Connects to custom dynamic property toggle rule
        layout.addWidget(self.status_bar)

        # Input Prompt Element
        self.prompt_bar = PromptBar()
        self.prompt_bar.command_submitted.connect(self._process_command)
        layout.addWidget(self.prompt_bar)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def set_ui_processing_state(self, is_processing: bool):
        """Toggles the status bar between active orange processing and green idle ready states."""
        if is_processing:
            self.status_bar.setText("● SYSTEM PROCESSING...")
            self.status_bar.setProperty("state", "processing")
        else:
            self.status_bar.setText("● SYSTEM READY")
            self.status_bar.setProperty("state", "ready")
        
        # Force the Qt graphics styling engine to update custom widget attributes dynamically
        self.status_bar.style().unpolish(self.status_bar)
        self.status_bar.style().polish(self.status_bar)

    def _process_command(self, text: str):
        cleaned_text = text.strip().lower()

        if cleaned_text in ["clear", "cls", "reset"]:
            self.chat_display.clear()
            self.set_ui_processing_state(False)
            return

        if cleaned_text in ["exit", "quit", "close"]:
            self.close()
            return

        # High-visibility contrast text for User entry
        self.chat_display.append(f"<font color='#ffffff'><b>User:</b> {text}</font>")
        self.prompt_bar.set_running_state(True)
        
        # Trigger orange glow status
        self.set_ui_processing_state(True)

        self.worker = AgentWorker(self.planner, self.executor, text)
        self.worker.status_signal.connect(self._update_status)
        self.worker.finished_signal.connect(self._handle_worker_completion)
        self.worker.start()

    def _update_status(self, status: str):
        # Check if this is a large response block from the local LLM Agent
        if "<b>AI Agent:</b>" in status or len(status) > 150:
            header = "<b><font color='#b388ff'>[System] AI Agent:</font></b><br>"
            body = status.replace("<b>AI Agent:</b>", "").strip()
            
            # Format markdown newline configurations to clean HTML page breaks
            formatted_body = body.replace("\n", "<br>")
            self.chat_display.append(f"{header}<font color='#f8f8f2'>{formatted_body}</font><br>")
        else:
            # High-visibility muted gray layout font for minor updates
            self.chat_display.append(f"<font color='#b388ff'>[System]</font> <font color='#a1a1b3'>{status}</font>")

    def _handle_worker_completion(self, success: bool):
        self.prompt_bar.set_running_state(False)
        
        # Return status dot state back to green idle glow
        self.set_ui_processing_state(False)
        
        if not success:
            self.chat_display.append("<font color='#ff5555'>[Warning] Sequence cycle terminated early due to processing faults.</font>")

    def closeEvent(self, event):
        """Triggers automatically when the window layout is closed."""
        self._cleanup_session()

        try:
            subprocess.run(["ollama", "stop", "qwen3:8b"], timeout=10)
            agent_logger.info("Ollama model unloaded successfully.")
        except Exception as e:
            agent_logger.warning(f"Failed to unload Ollama model: {str(e)}")

        event.accept()