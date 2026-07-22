# frontend/app/threads/api_thread.py
import requests
from PyQt5.QtCore import QThread, pyqtSignal
from ..utils.config import API_URL

class APIThread(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        try:
            # Optional: print debug info (remove in production)
            print(f"Sending query to {API_URL}/ask: {self.query}")

            response = requests.post(
                f"{API_URL}/ask",
                json={"query": self.query},
                timeout=30,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 200:
                try:
                    data = response.json()
                    self.finished.emit(data)
                except requests.exceptions.JSONDecodeError:
                    self.error.emit("Invalid JSON response from server.")
            else:
                error_detail = f"API error {response.status_code}"
                try:
                    error_detail += f": {response.json().get('detail', response.text)}"
                except:
                    error_detail += f": {response.text}"
                self.error.emit(error_detail)

        except requests.exceptions.ConnectionError:
            self.error.emit("Could not connect to AgriBoot API. Is it running?")
        except requests.exceptions.Timeout:
            self.error.emit("Request timed out. The API is taking too long.")
        except Exception as e:
            self.error.emit(f"Unexpected error: {str(e)}")