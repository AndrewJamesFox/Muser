# Muser

Muser is a lightweight desktop application for capturing spontaneous and transient thoughts as they occur. It provides a minimal, distraction-free interface for quick text entry, persistent local storage, and automatic PDF archiving.

## Features
- Simple Tkinter-based GUI for rapid thought logging
- Persistent SQLite database with automatic timestamping
- Scrollable history view of recent thought entries
- Keyboard shortcuts for saving and deleting thoughts
- ID-based deletion with confirmation
- Automatic PDF export on application exit

## Architecture
- `gui.py` – Tkinter UI, keyboard shortcuts, and interaction logic
- `db_log.py` – SQLite database layer for storing, retrieving, and deleting thoughts
- `pdf_export.py` – PDF generation using ReportLab
- `main.py` – Application entry point and lifecycle management

The project follows a modular, MVC-style structure to keep UI logic, persistence, and export functionality cleanly separated.

## Technologies
- Python
- Tkinter
- SQLite
- ReportLab

## Use Case
Muser is designed for capturing transiet ideas, reflections, or thoughts with minimal friction, while ensuring thoughts are safely stored and easily archived for later review.
