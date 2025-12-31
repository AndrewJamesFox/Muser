from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from datetime import datetime

class EnlargeCardDialog(QDialog):
    def __init__(self, thought_id, timestamp, content, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Thought #{thought_id}")
        self.setModal(True)
        self.setMinimumSize(400, 300)
        self.setStyleSheet("background-color: rgba(0,0,0,0);")  # transparent window background

        # Scroll area for really long thoughts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)
        main = QVBoxLayout(container)
        main.setAlignment(Qt.AlignTop)

        top = QHBoxLayout()

        # DATETIME format
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = datetime.fromisoformat(timestamp)

        # DATE LABEL
        date_label = QLabel(dt.strftime("%b %d, %Y"))
        font = QFont()
        font.setBold(True)
        date_label.setFont(font)
        date_label.setStyleSheet("color: black;")
        top.addWidget(date_label, alignment=Qt.AlignLeft)

        # ID LABEL
        id_label = QLabel(f"{thought_id}")
        id_label.setFont(font)
        top.addWidget(id_label, alignment=Qt.AlignRight)
        id_label.setStyleSheet("color: black;")
        main.addLayout(top)

        # TIME LABEL
        time_label = QLabel(dt.strftime("@ %H:%M"))
        time_label.setStyleSheet("color: gray; font-size: 10pt;")
        main.addWidget(time_label, alignment=Qt.AlignLeft)

        main.addSpacing(5)

        # THOUGHT LABEL
        content_label = QLabel(content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("color: black;")
        main.addWidget(content_label)


        # CLOSE BUTTON
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        main.addWidget(close_btn, alignment=Qt.AlignRight)

        scroll.setWidget(container)

        dlg_layout = QVBoxLayout(self)
        dlg_layout.addWidget(scroll)
