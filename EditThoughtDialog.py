from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
import db_log

class EditThoughtDialog(QDialog):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)
        self.db_path = db_path
        self.setWindowTitle("Edit Thought")
        self.setModal(True)
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # ID input
        layout.addWidget(QLabel("Enter Thought ID to edit:"))
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")
        layout.addWidget(self.id_input)

        # Load button to fetch content
        self.load_btn = QPushButton("Load Thought")
        self.load_btn.clicked.connect(self.load_thought)
        layout.addWidget(self.load_btn, alignment=Qt.AlignRight)

        # Text box for editing
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # Save/Cancel buttons
        buttons_row = QHBoxLayout()
        buttons_row.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_row.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_changes)
        buttons_row.addWidget(save_btn)

        layout.addLayout(buttons_row)

        self.setLayout(layout)
        self.current_id = None

    def load_thought(self):
        db_log.init_db(self.db_path)
        try:
            thought_id = int(self.id_input.text())
        except ValueError:
            return
        # Fetch thought from DB
        all_thoughts = db_log.get_all_thoughts(self.db_path)
        for tid, ts, content in all_thoughts:
            if tid == thought_id:
                self.text_edit.setText(content)
                self.current_id = tid
                return

    def save_changes(self):
        if self.current_id is None:
            return
        new_content = self.text_edit.toPlainText().strip()
        if not new_content:
            return
        db_log.update_thought(self.db_path, self.current_id, new_content)
        self.accept()
