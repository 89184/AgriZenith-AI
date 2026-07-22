import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QScrollArea, QLineEdit, QPushButton,
    QApplication, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QBrush, QColor

from ..widgets.chat_bubble import ChatBubble
from ..widgets.typing_indicator import TypingIndicator
from ..threads.api_thread import APIThread
from ..dialogs.history_dialog import HistoryDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AgriBoot – Farmer Advisory")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(700, 500)

        self.history = []
        self.messages = []

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---------- Header (gradient background) ----------
        header = QLabel()
        header.setFixedHeight(140)
        header.setAlignment(Qt.AlignCenter)
        # Gradient
        gradient = QLinearGradient(0, 0, 0, header.height())
        gradient.setColorAt(0.0, QColor("#0A2540"))
        gradient.setColorAt(0.5, QColor("#1E3A8A"))
        gradient.setColorAt(1.0, QColor("#3B82F6"))
        palette = header.palette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        header.setPalette(palette)
        header.setAutoFillBackground(True)

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_layout.setSpacing(2)

        title = QLabel("AgriZenith AI")
        title.setFont(QFont("Arial", 26, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(
            "An Multi-Stage Intent Classification and Retrieval Framework for Intelligent Agricultural Advisory, with an Artificial Intelligence that brings agriculture to its highest level of intelligence, efficiency, and innovation."
        )
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: rgba(255,255,255,0.9);")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)

        sub2 = QLabel("Powered by RAG, LLMs, and Domain‑specific Knowledge")
        sub2.setFont(QFont("Arial", 10))
        sub2.setStyleSheet("color: rgba(255,255,255,0.7);")
        sub2.setAlignment(Qt.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addWidget(sub2)
        main_layout.addWidget(header)

        # ---------- Chat area ----------
        self.chat_scroll = QScrollArea()
        self.chat_scroll.setWidgetResizable(True)
        self.chat_scroll.setStyleSheet("background: #e5ddd5; border: none;")
        self.chat_content = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_content)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(5)
        self.chat_scroll.setWidget(self.chat_content)
        main_layout.addWidget(self.chat_scroll, 1)

        # ---------- Typing indicator ----------
        self.typing_indicator = TypingIndicator()
        main_layout.addWidget(self.typing_indicator)

        # ---------- Input area ----------
        input_container = QWidget()
        input_container.setStyleSheet("background: #f0f0f0; padding: 8px;")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(10, 5, 10, 5)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ask a farming question...")
        self.input_field.setStyleSheet("border-radius: 20px; padding: 8px 16px; border: 1px solid #ccc;")
        self.input_field.returnPressed.connect(self.send_message)

        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background: #138808;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0d6b05;
            }
        """)
        self.send_btn.clicked.connect(self.send_message)

        input_layout.addWidget(self.input_field, 1)
        input_layout.addWidget(self.send_btn)
        main_layout.addWidget(input_container)

        # ---------- Menu ----------
        menu = self.menuBar()
        history_action = menu.addAction("History")
        history_action.triggered.connect(self.show_history)

        # Welcome message (assistant)
        self.add_message(
            "Hello! I'm your farming advisor. Ask me anything about crops, "
            "fertilizers, pests, irrigation, market prices, and more.",
            False
        )

    def add_message(self, text, is_user, result=None):
        # Store message for history reference
        self.messages.append({"text": text, "is_user": is_user, "result": result})
        bubble = ChatBubble(text, is_user, result)
        self.chat_layout.addWidget(bubble)
        QApplication.processEvents()
        self.chat_scroll.verticalScrollBar().setValue(
            self.chat_scroll.verticalScrollBar().maximum()
        )

    def send_message(self):
        query = self.input_field.text().strip()
        if not query:
            return

        self.input_field.clear()
        self.input_field.setEnabled(False)
        self.send_btn.setEnabled(False)
        self.typing_indicator.start_typing()

        self.add_message(query, True)   # user message (no result)

        self.thread = APIThread(query)
        self.thread.finished.connect(self.on_api_finished)
        self.thread.error.connect(self.on_api_error)
        self.thread.start()

    def on_api_finished(self, result):
        try:
            self.typing_indicator.stop_typing()
            self.input_field.setEnabled(True)
            self.send_btn.setEnabled(True)

            if not isinstance(result, dict):
                raise ValueError("Unexpected API response format.")

            answer = result.get("answer", "Sorry, no answer provided.")
            self.add_message(answer, False, result)   # assistant message with metadata

            # Find the last user message from self.messages
            last_user = ""
            for msg in reversed(self.messages):
                if msg.get("is_user", False):
                    last_user = msg.get("text", "")
                    break

            self.history.append({
                "query": last_user or "?",
                "result": result,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.add_message(f"Internal error: {str(e)}", False)

    def on_api_error(self, error_msg):
        try:
            self.typing_indicator.stop_typing()
            self.input_field.setEnabled(True)
            self.send_btn.setEnabled(True)
            QMessageBox.warning(self, "Error", f"API error: {error_msg}")
            self.add_message(f"{error_msg}", False)
        except Exception as e:
            print(f"Error in error handler: {e}")
            self.add_message(f"Unexpected error: {str(e)}", False)

    def show_history(self):
        if not self.history:
            QMessageBox.information(self, "History", "No queries yet.")
            return
        from ..dialogs.history_dialog import HistoryDialog
        dialog = HistoryDialog(self.history, self)
        dialog.exec_()