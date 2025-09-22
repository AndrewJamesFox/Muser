import tkinter as tk
from gui import MuserApp
import pdf_export
import db_log

def main():
    db_log.init_db()            # init db if it doesn't exist
    root = tk.Tk()              # create main window (root of GUI)
    root.geometry("900x600")    # set size of main window
    app = MuserApp(root)        # attach instance of MuserApp class to root window

    # When closing app window
    def on_close():
        pdf_export.export_to_pdf("musings.pdf")     # create/overwrite PDF
        root.destroy()                              # close app window

    root.protocol("WM_DELETE_WINDOW", on_close) # close when window's X button pressed
    root.mainloop()                                   # start event loop

if __name__ == "__main__":
    main()