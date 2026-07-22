from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer

class TypingIndicator(QLabel):
    def __init__(self, parent=None):
        super().__init__("AgriBoot is thinking...", parent)
        self.setStyleSheet("color: #888; padding: 5px; background: #e5ddd5; border-radius: 5px;")
        self.hide()
        self._dots = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_dots)
        self.timer.setInterval(500)

    def start_typing(self):
        self._dots = 0
        self.setText("AgriBoot is thinking")
        self.show()
        self.timer.start()

    def stop_typing(self):
        self.timer.stop()
        self.hide()

    def update_dots(self):
        self._dots = (self._dots + 1) % 4
        dots = "." * self._dots
        self.setText(f"AgriBoot is thinking{dots}")