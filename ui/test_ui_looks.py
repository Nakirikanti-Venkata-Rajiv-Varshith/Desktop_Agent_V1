import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt, QTimer

class ModernTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Computer Desktop Agent - V1 Console")
        self.resize(680, 480) 
        self._init_ui()
        self._apply_styles()
        
        # --- Demo State Timer ---
        # Toggles the state every 3 seconds to test the green vs orange glow effect
        self.is_processing = False
        self.demo_timer = QTimer()
        self.demo_timer.timeout.connect(self._toggle_demo_state)
        self.demo_timer.start(3000)

    def _init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(22, 22, 22, 22) 

        # Header Label
        header_lbl = QLabel("SYSTEM LIVE STREAM OUTPUT")
        header_lbl.setObjectName("HeaderLabel")
        layout.addWidget(header_lbl)

        # Main Chat Display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.append("<b><font color='#b388ff'>[System]</font></b> Cyberpunk aesthetic theme engine initialized successfully.<br>")
        self.chat_display.append("<font color='#ffffff'><b>User:</b> let's make this look absolutely incredible</font>")
        self.chat_display.append("<b><font color='#b388ff'>[System] AI Agent:</font></b><br><font color='#f8f8f2'>Notice the subtle dark glass container look, deep background contrast, and glowing interactive focus states. Much more premium.</font><br>")
        layout.addWidget(self.chat_display)

        # Status Bar Info (Uses dynamic properties)
        self.status_bar = QLabel("● SYSTEM READY")
        self.status_bar.setObjectName("StatusBar")
        self.status_bar.setProperty("state", "ready") # Initial state matching QSS rules
        layout.addWidget(self.status_bar)

        # Input Row (Prompt bar + Execute Button)
        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)

        self.prompt_bar = QLineEdit()
        self.prompt_bar.setPlaceholderText("Type your next instruction here...")
        
        self.execute_btn = QPushButton("EXECUTE")
        
        input_layout.addWidget(self.prompt_bar, stretch=5)
        input_layout.addWidget(self.execute_btn, stretch=1)
        layout.addLayout(input_layout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def set_system_state(self, state: str):
        """
        Changes system indicator styles dynamically.
        Pass 'processing' for orange glow, or 'ready' for green glow.
        """
        if state == "processing":
            self.status_bar.setText("● SYSTEM PROCESSING...")
            self.status_bar.setProperty("state", "processing")
        else:
            self.status_bar.setText("● SYSTEM READY")
            self.status_bar.setProperty("state", "ready")
        
        # Forces PyQt to re-evaluate the QSS rule style change instantly
        self.status_bar.style().unpolish(self.status_bar)
        self.status_bar.style().polish(self.status_bar)

    def _toggle_demo_state(self):
        """Internal demo function switcher to show off your dynamic styles."""
        self.is_processing = not self.is_processing
        target_state = "processing" if self.is_processing else "ready"
        self.set_system_state(target_state)

    def _apply_styles(self):
        """Global UI stylesheet matching Gemini visual hierarchy and typography definitions."""
        stylesheet = """
            /* Main Window Core */
            QMainWindow {
                background-color: #08080a; 
            }

            /* Section Header */
            QLabel#HeaderLabel {
                color: #a1a1b3; 
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 1.5px; 
                font-family: 'Google Sans', 'Inter', 'Segoe UI', sans-serif;
            }

            /* Main Text Area Monitor Block */
            QTextEdit {
                background-color: #111115; 
                border: 1px solid #22222e; 
                border-radius: 10px;
                color: #f8f8f2; 
                padding: 14px;
                font-size: 13px;
                font-family: 'JetBrains Mono', 'Roboto Mono', 'Consolas', monospace;
            }

            /* --- Dynamic State Status Bar Rules --- */
            
            /* Green Glow Variant (State: ready) */
            QLabel#StatusBar[state="ready"] {
                color: #00ff87; 
                font-weight: bold;
                font-size: 11px;
                letter-spacing: 0.5px;
                padding-left: 2px;
                font-family: 'Google Sans', 'Inter', 'Segoe UI', sans-serif;
            }
            
            /* Orange Glow Variant (State: processing) */
            QLabel#StatusBar[state="processing"] {
                color: #ff9100; 
                font-weight: bold;
                font-size: 11px;
                letter-spacing: 0.5px;
                padding-left: 2px;
                font-family: 'Google Sans', 'Inter', 'Segoe UI', sans-serif;
            }

            /* Command Input Field Box */
            QLineEdit {
                background-color: #111115;
                border: 1px solid #22222e;
                border-radius: 8px;
                color: #ffffff; 
                padding: 11px 14px;
                font-size: 13px;
                font-family: 'Google Sans', 'Inter', 'Segoe UI', sans-serif;
            }
            QLineEdit:focus {
                border: 1px solid #b388ff; 
            }

            /* Run Trigger Button Layout */
            QPushButton {
                background-color: #b388ff; 
                color: #08080a; 
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
                letter-spacing: 1.2px;
                padding: 11px 20px;
                font-family: 'Google Sans', 'Inter', 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background-color: #d1b3ff; 
            }
            QPushButton:pressed {
                background-color: #9055ff; 
            }
        """
        self.setStyleSheet(stylesheet)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernTestWindow()
    window.show()
    sys.exit(app.exec())