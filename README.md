# Muser

**Muser** is a lightweight desktop application for capturing spontaneous and transiet thoughts as they occur.

The app provides a simple writing surface, a chronological thought log, and automatic export to a readable PDF journal.

---

## Features

- Minimal desktop GUI for rapid thought capture
- Persistent local storage using SQLite with automatic timestamps
- Scrollable thought log with expandable thought cards
- Keyboard shortcuts for common actions (save, edit, delete)
- ID-based editing and deletion with confirmation dialogs
- Automatic PDF export of all thoughts on application exit
- Configurable PDF export location with persistent settings

---

## Architecture

The project is structured around small, focused modules with clear responsibilities:

- `app.py` – Main application window, layout, and event wiring
- `ThoughtCard.py` – UI component for displaying individual thoughts
- `EnlargeCardDialog.py` – Full-screen expanded view for reading long thoughts
- `db_log.py` – SQLite persistence layer (CRUD operations)
- `pdf_export.py` – PDF generation using ReportLab
- `settings.py` (or equivalent) – Persistent user settings (PDF export location)

UI logic, persistence, and export functionality are intentionally separated to keep the codebase easy to reason about and extend.

---

## Technologies

- Python
- PySide6 (Qt)
- SQLite
- ReportLab
