from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QHBoxLayout, QMessageBox
)
from PySide6.QtCore import Qt
import os


class SettingsDialog(QDialog):
    def __init__(self, pdf_export_dir, db_path, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setModal(True)

        # Store original values (for cancel functionality)
        self.original_export_dir = pdf_export_dir
        self.original_db_path = db_path

        # Working values (what the user is changing)
        self.export_dir = pdf_export_dir
        self.db_path = db_path

        layout = QVBoxLayout(self)

        # ---- PDF EXPORT ----
        self.pdf_label = QLabel(f"PDF export location:\n{self.export_dir}")
        self.pdf_label.setWordWrap(True)
        layout.addWidget(self.pdf_label)

        pdf_btn = QPushButton("Change PDF Location")
        pdf_btn.clicked.connect(self.choose_pdf_directory)
        layout.addWidget(pdf_btn, alignment=Qt.AlignLeft)

        layout.addSpacing(12)

        # ---- DATABASE ----
        self.db_label = QLabel(f"Database location:\n{self.db_path}")
        self.db_label.setWordWrap(True)
        layout.addWidget(self.db_label)

        db_btn = QPushButton("Change Database Location")
        db_btn.clicked.connect(self.change_db_location)
        layout.addWidget(db_btn, alignment=Qt.AlignLeft)

        layout.addStretch()

        # ---- BUTTONS ----
        buttons = QHBoxLayout()
        buttons.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        buttons.addWidget(save_btn)

        layout.addLayout(buttons)

    # ---------- PDF ----------
    def choose_pdf_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select PDF Export Directory", self.export_dir
        )
        if directory:
            # Validate write access
            if not os.access(directory, os.W_OK):
                QMessageBox.warning(
                    self,
                    "Permission Denied",
                    f"Cannot write to:\n{directory}\n\nPlease choose a different location."
                )
                return

            self.export_dir = directory
            self.pdf_label.setText(f"PDF export location:\n{self.export_dir}")

    # ---------- DB ----------
    def change_db_location(self):
        new_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select Database Location",
            self.db_path,
            "SQLite Database (*.db)"
        )

        if not new_path:
            return

        # Ensure .db extension
        if not new_path.endswith('.db'):
            new_path += '.db'

        if os.path.abspath(new_path) == os.path.abspath(self.original_db_path):
            return  # no-op

        # Validate write access to the directory
        new_dir = os.path.dirname(new_path)
        if new_dir and not os.access(new_dir, os.W_OK):
            QMessageBox.warning(
                self,
                "Permission Denied",
                f"Cannot write to:\n{new_dir}\n\nPlease choose a different location."
            )
            return

        self.db_path = new_path
        self.db_label.setText(f"Database location:\n{self.db_path}")

    def has_changes(self):
        """Check if user made any changes."""
        return (
                self.export_dir != self.original_export_dir or
                self.db_path != self.original_db_path
        )

    def pdf_changed(self):
        """Check if PDF location changed."""
        return self.export_dir != self.original_export_dir

    def db_changed(self):
        """Check if DB location changed."""
        return self.db_path != self.original_db_path