from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt

class DeleteThoughtDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Delete Thought")
        self.setModal(True)
        self.setFixedSize(250, 120)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        layout.addWidget(QLabel("Enter Thought ID to delete:"))

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")
        layout.addWidget(self.id_input)

        # Buttons row
        buttons_row = QHBoxLayout()
        buttons_row.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_row.addWidget(cancel_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.accept)
        buttons_row.addWidget(delete_btn)

        layout.addLayout(buttons_row)

        self.setLayout(layout)

    def get_id(self):
        try:
            return int(self.id_input.text())
        except ValueError:
            return None
