from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFileDialog, QHBoxLayout
from PySide6.QtCore import Qt
from pathlib import Path

class SettingsDialog(QDialog):
    def __init__(self, current_dir, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setFixedSize(400, 140)

        self.export_dir = current_dir

        layout = QVBoxLayout(self)

        self.label = QLabel(f"PDF export location:\n{self.export_dir}")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

        browse_btn = QPushButton("Change Location")
        browse_btn.clicked.connect(self.choose_directory)
        layout.addWidget(browse_btn, alignment=Qt.AlignLeft)

        buttons = QHBoxLayout()
        buttons.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        buttons.addWidget(close_btn)

        layout.addLayout(buttons)

    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Export Directory", self.export_dir
        )
        if directory:
            self.export_dir = directory
            self.label.setText(f"PDF export location:\n{self.export_dir}")
