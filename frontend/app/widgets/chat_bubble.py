from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class ChatBubble(QWidget):
    def __init__(self, text, is_user, result=None, parent=None):
        super().__init__(parent)
        self.is_user = is_user
        self.text = text
        self.result = result

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)

        if is_user:
            # User message – simple green bubble, right‑aligned
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(8)

            msg = QLabel(text)
            msg.setWordWrap(True)
            msg.setStyleSheet("""
                background-color: #dcf8c6;
                border-radius: 16px;
                padding: 10px 16px;
                color: #111;
                font-size: 14px;
                max-width: 70%;
            """)
            avatar = QLabel("")
            avatar.setFont(QFont("Segoe UI Emoji", 20))
            avatar.setFixedSize(40, 40)
            avatar.setAlignment(Qt.AlignCenter)

            row.addStretch()
            row.addWidget(msg)
            row.addWidget(avatar)
            layout.addLayout(row)

        else:
            # Assistant message – card with metadata + answer
            container = QFrame()
            container.setFrameShape(QFrame.NoFrame)
            container.setStyleSheet("""
                QFrame {
                    background-color: #f8fafc;
                    border-left: 5px solid #3B82F6;
                    border-radius: 12px;
                    padding: 12px;
                    margin: 4px 0;
                }
            """)
            inner = QVBoxLayout(container)
            inner.setSpacing(6)

            # Metadata pills
            if result:
                intent = result.get("intent", "Unknown")
                conf = result.get("intent_confidence", 0.0)
                retrieval = result.get("retrieval_confidence", 0.0)
                entities = result.get("entities", [])

                color = "#10B981" if conf > 0.7 else "#F59E0B" if conf > 0.4 else "#d32f2f"

                # Row of pills
                pill_row = QHBoxLayout()
                pill_row.setSpacing(8)

                intent_pill = QLabel(f"INTENT: {intent}")
                intent_pill.setStyleSheet(
                    "background-color: #e3f2fd; color: #0d47a1; padding: 2px 12px; border-radius: 12px; font-weight: bold;"
                )
                pill_row.addWidget(intent_pill)

                conf_pill = QLabel(f"CONFIDENCE: {conf:.2f}")
                conf_pill.setStyleSheet(
                    f"background-color: {color}20; color: {color}; padding: 2px 12px; border-radius: 12px; border: 1px solid {color}40; font-weight: bold;"
                )
                pill_row.addWidget(conf_pill)

                ret_pill = QLabel(f"Retrieval: {retrieval:.2f}")
                ret_pill.setStyleSheet(
                    "background-color: #e3f2fd; color: #0d47a1; padding: 2px 12px; border-radius: 12px;"
                )
                pill_row.addWidget(ret_pill)
                pill_row.addStretch()
                inner.addLayout(pill_row)

                # Entity badge (top entity)
                if entities:
                    top = entities[0]
                    badge = QLabel(f"{top['entity']}: {top['value']}")
                    badge.setStyleSheet(
                        "background-color: #e8f5e9; color: #1b5e20; padding: 2px 12px; border-radius: 12px; font-size: 12px;"
                    )
                    inner.addWidget(badge)

            # Answer text
            answer_label = QLabel(text)
            answer_label.setWordWrap(True)
            answer_label.setStyleSheet("font-size: 14px; color: #111; margin-top: 4px;")
            inner.addWidget(answer_label)

            # Assemble with avatar on the left
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(8)

            avatar = QLabel("")
            avatar.setFont(QFont("Segoe UI Emoji", 20))
            avatar.setFixedSize(40, 40)
            avatar.setAlignment(Qt.AlignTop | Qt.AlignLeft)

            row.addWidget(avatar)
            row.addWidget(container, 1)   # container takes remaining space
            row.setAlignment(Qt.AlignLeft)
            layout.addLayout(row)