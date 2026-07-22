from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QListWidgetItem,
    QDialogButtonBox, QMessageBox
)
from PyQt5.QtCore import Qt

class HistoryDialog(QDialog):
    def __init__(self, history, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Query History")
        self.setMinimumSize(550, 450)

        layout = QVBoxLayout(self)

        self.list_widget = QListWidget()
        for item in history:
            text = f"{item['query']}  ({item['timestamp']})"
            list_item = QListWidgetItem(text)
            list_item.setData(Qt.UserRole, item)
            self.list_widget.addItem(list_item)

        self.list_widget.itemDoubleClicked.connect(self.show_details)
        layout.addWidget(self.list_widget)

        btn_box = QDialogButtonBox(QDialogButtonBox.Close)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def show_details(self, item):
        data = item.data(Qt.UserRole)
        result = data.get('result', {})
        intent = result.get('intent', 'N/A')
        conf = result.get('intent_confidence', 0.0)
        retrieval = result.get('retrieval_confidence', 0.0)
        answer = result.get('answer', 'N/A')
        entities = result.get('entities', [])

        entity_str = "\n".join([f"  • {e['entity']}: {e['value']}" for e in entities]) if entities else "  None"

        msg = (
            f"Query: {data['query']}\n\n"
            f"Intent: {intent}\n"
            f"Confidence: {conf:.2f}\n"
            f"Retrieval confidence: {retrieval:.2f}\n\n"
            f"Entities:\n{entity_str}\n\n"
            f"Answer:\n{answer}"
        )
        QMessageBox.information(self, "Query Details", msg)