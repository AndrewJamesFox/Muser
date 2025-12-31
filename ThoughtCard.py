from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QFontMetrics
from datetime import datetime
from ElidedLabel import ElidedLabel

class ThoughtCard(QFrame):
    clicked = Signal(int, str, str)

    def __init__(self, thought_id, timestamp, content):
        super().__init__()
        self.setFixedHeight(80)
        self.thought_id = thought_id
        self.timestamp = timestamp
        self.content = content

        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)

        main = QVBoxLayout()
        main.setContentsMargins(10, 10, 10, 10)
        main.setAlignment(Qt.AlignTop)

        top = QHBoxLayout()

        # DATETIME format
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            dt = datetime.fromisoformat(timestamp)
        formatted_time = dt.strftime("%b %d, %Y")  # e.g., "May 05, 2025"


        # DATE LABEL
        date_label = QLabel(formatted_time)
        font = QFont()
        font.setBold(True)
        date_label.setFont(font)
        date_label.setStyleSheet("color: black;")
        top.addWidget(date_label, alignment=Qt.AlignLeft)

        # ID LABEL
        id_label = QLabel(f"{thought_id}")
        id_label.setFont(font)
        id_label.setStyleSheet("color: black;")
        top.addWidget(id_label, alignment=Qt.AlignRight)
        main.addLayout(top)

        # TIME LABEL
        time_label = QLabel(dt.strftime("@ %H:%M"))
        time_label.setStyleSheet("color: gray; font-size: 10pt;")
        main.addWidget(time_label, alignment=Qt.AlignLeft)

        main.addSpacing(5)

        # THOUGHT LABEL
        content_label = ElidedLabel(content)
        content_label.setStyleSheet("color: black;")
        content_label.setAlignment(Qt.AlignTop)
        content_label.setFixedHeight(40)  # or based on card height minus date/time
        content_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        main.addWidget(content_label)

        main.addStretch()
        self.setLayout(main)

        # Enable mouse tracking & clickable
        self.setMouseTracking(True)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.thought_id, self.timestamp, self.content)

