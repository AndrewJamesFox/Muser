import os
import sys
import settings
from SettingsDialog import SettingsDialog
import pdf_export
import db_log
from ThoughtCard import ThoughtCard
from EnlargeCardDialog import EnlargeCardDialog
from DeleteThoughtDialog import DeleteThoughtDialog
from EditThoughtDialog import EditThoughtDialog
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QScrollArea
)
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtCore import Qt


class MuserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Muser")
        self.resize(900, 600)
        self.settings = settings.load_settings()
        self.pdf_export_dir = self.settings["pdf_export_dir"]   #musings.pdf export path

        main = QHBoxLayout(self)

        ### PANELS
        ## LEFT PANEL
        left_panel = QVBoxLayout()
        left_panel.setSpacing(5)

        # LEFT HEADER
        left_header = QHBoxLayout()
        left_header.setSpacing(10)
        left_label = QLabel("Your thought...")
        left_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        left_header.addWidget(left_label, alignment=Qt.AlignLeft)

        left_header.addStretch()

        # save button
        save_btn = QPushButton("Save")
        save_btn.setToolTip("Save the current thought (Cmd+Return)")
        save_btn.clicked.connect(self.save_thought)
        #left_header.addWidget(save_btn, alignment=Qt.AlignRight)
        left_header.addWidget(save_btn)

        # edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setToolTip("Edit a thought by ID (Cmd+E)")
        edit_btn.clicked.connect(self.open_edit_dialog)
        #left_header.addWidget(edit_btn, alignment=Qt.AlignRight)
        left_header.addWidget(edit_btn)

        # delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setToolTip("Delete a thought by ID (Cmd+L)")
        delete_btn.clicked.connect(self.open_delete_dialog)
        #left_header.addWidget(delete_btn, alignment=Qt.AlignRight)
        left_header.addWidget(delete_btn)

        # settings button
        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self.open_settings_dialog)
        left_header.addWidget(settings_btn)

        left_panel.addLayout(left_header)  # add left header to left panel


        # LEFT TEXT AREA
        self.text_edit = QTextEdit()
        left_panel.addWidget(self.text_edit)

        self.sort_desc = True  # newest-first by default

        ## RIGHT PANEL
        right_panel = QVBoxLayout()
        right_panel.setSpacing(5)

        # RIGHT HEADER
        right_header = QHBoxLayout()
        right_label = QLabel("Thought Log")
        right_label.setStyleSheet("font-weight: bold; font-size: 12pt;")
        right_header.addWidget(right_label, alignment=Qt.AlignLeft)
        sort_btn = QPushButton("Sort")  #SORT BUTTON
        sort_btn.setFixedWidth(60)
        sort_btn.clicked.connect(self.toggle_sort)
        right_header.addWidget(sort_btn, alignment=Qt.AlignRight)

        # RIGHT SCROLL AREA
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10) #spacing between cards
        self.scroll_layout.addStretch()
        self.scroll_area.setWidget(self.scroll_content)

        right_panel.addLayout(right_header)
        right_panel.addWidget(self.scroll_area)

        # ADD TO MAIN
        main.addLayout(left_panel, 2)   #add left panel
        main.addLayout(right_panel, 1)  #add right panel

        self.load_thoughts_from_db()  #load thoughts from db automatically


        ###-------------------------------------------------
        ### KEYBOARD SHORTCUTS
        ###-------------------------------------------------
        # Save Thought: Cmd+Return
        save_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        save_shortcut.activated.connect(self.save_thought)

        # Edit Thought: Cmd+E
        edit_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        edit_shortcut.activated.connect(self.open_edit_dialog)

        # Delete Thought: Cmd+D
        delete_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        delete_shortcut.activated.connect(self.open_delete_dialog)


        ###-------------------------------------------------
        ### BUTTON STYLE SHEETS
        ###-------------------------------------------------
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 5px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #008000;
            }
        """)

        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 5px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #0096FF;
            }
        """)

        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 5px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #FF0000;
            }
        """)

        sort_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                border-radius: 5px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #FFFF00;
            }
        """)


    ###-------------------------------------------------
    ### HELPER FUNCTIONS
    ###-------------------------------------------------
    def show_enlarged_card(self, thought_id, timestamp, content):
        dlg = EnlargeCardDialog(thought_id, timestamp, content, parent=self)
        dlg.showMaximized()  #maximize the dialog
        dlg.exec()  #start modal event loop


    ## CLICK BUTTON FUNCTIONS
    def toggle_sort(self):
        self.sort_desc = not self.sort_desc
        self.load_thoughts_from_db()


    def save_thought(self):
        content = self.text_edit.toPlainText().strip()
        if not content:
            return
        db_log.add_thought(content)
        self.text_edit.clear()          #clear input
        self.load_thoughts_from_db()    #refresh right panel


    def load_thoughts_from_db(self):
        # Clear existing cards (if any)
        for i in reversed(range(self.scroll_layout.count() - 1)):  # keep the stretch at the end
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        thoughts = db_log.get_all_thoughts()  # fetch from DB
        if not self.sort_desc:
            thoughts = reversed(thoughts)  # oldest first

        for thought_id, timestamp, content in thoughts:
            card = ThoughtCard(thought_id, timestamp, content)
            card.clicked.connect(lambda id, ts, text: self.show_enlarged_card(id, ts, text))
            self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, card)


    def open_edit_dialog(self):
        dialog = EditThoughtDialog(parent=self)
        if dialog.exec():  # only runs if user clicks Save
            self.load_thoughts_from_db()  # refresh right panel


    def open_delete_dialog(self):
        dialog = DeleteThoughtDialog(parent=self)
        if dialog.exec():  # only runs if user clicks Delete
            thought_id = dialog.get_id()
            if thought_id is not None:
                db_log.delete_thought(thought_id)
                self.load_thoughts_from_db()

    def open_settings_dialog(self):
        old_dir = self.pdf_export_dir

        dialog = SettingsDialog(self.pdf_export_dir, parent=self)
        if dialog.exec():
            new_dir = dialog.export_dir

            if new_dir != old_dir:
                # Remove old PDF
                old_pdf = os.path.join(old_dir, "musings.pdf")
                if os.path.exists(old_pdf):
                    try:
                        os.remove(old_pdf)
                    except OSError:
                        pass

                # Update state
                self.pdf_export_dir = new_dir
                self.settings["pdf_export_dir"] = new_dir
                settings.save_settings(self.settings)

                # Export immediately
                new_pdf = os.path.join(new_dir, "musings.pdf")
                pdf_export.export_to_pdf(new_pdf)


    # on close
    def closeEvent(self, event):
        import os
        import pdf_export

        pdf_path = os.path.join(self.pdf_export_dir, "musings.pdf")
        pdf_export.export_to_pdf(pdf_path)

        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MuserApp()
    window.show()
    sys.exit(app.exec())