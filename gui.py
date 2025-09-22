import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

import db_log as db


class MuserApp:
    def __init__(self, root):
        """Initialize primary application class."""
        self.root = root                        # store root window in instance var for later access
        self.setup_ui()                         # build GUI interface
        self.update_thoughts_view()             # load saved thoughts from db and display them

    def setup_ui(self):
        """Set up UI."""
        self.root.title("Muser")                # main window title

        ## MAIN FRAME
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.LEFT,           # put on left panel
                        fill=tk.BOTH,           # expand in both directions
                        expand=True,            # allow frame expansion to fill space
                        padx=10, pady=10)       # pixels padding around frame

        # Text Input Box
        tk.Label(main_frame, text="What's on your mind?").pack(pady=5)  # label
        self.entry_box = tk.Text(main_frame, height=10, wrap=tk.WORD)   # text entry box
        self.entry_box.pack(padx=10, pady=5, fill=tk.BOTH, expand=True) # pad text entry box

        ## BUTTON FRAME
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)

        # Save Button
        save_btn = tk.Button(btn_frame,
                             text="Save Thought (Ctrl+Enter)",
                             command=self.save_thought)
        save_btn.pack()

        # Delete Button / Functionality
        self.delete_id_entry = tk.Entry(btn_frame, width=5)             # entry box for number to delete
        self.delete_id_entry.pack(side=tk.RIGHT, padx=5)
        self.delete_id_entry.bind('<Return>', self.handle_delete_enter) # bind Enter key to delete
        delete_btn = tk.Button(btn_frame,                               # actual delete button
                               text="Delete (ctrl+e)",
                               command=self.delete_thought)
        delete_btn.pack(side=tk.LEFT, padx=5)


        ## VIEWER FRAME
        viewer_frame = tk.Frame(self.root, width=300)
        viewer_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 10), pady=10)

        # Scrollable widget to view thoughts
        self.thoughts_text = scrolledtext.ScrolledText(viewer_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.thoughts_text.pack(fill=tk.BOTH, expand=True)


        ## KEYBOARD SHORTCUTS
        # Save Thought Shortcut
        self.entry_box.bind('<Control-Return>', self.handle_save_shortcut)  # windows
        self.entry_box.bind('<Command-Return>', self.handle_save_shortcut)  # macOS

        # Delete Thought Shortcut
        self.root.bind('<Control-e>', self.focus_delete_entry)  # windows
        self.root.bind('<Command-e>', self.focus_delete_entry)  # macOS

        # Delete Thought Entry box Toggle
        self.root.bind('<Control-e>', self.toggle_delete_focus) # windows
        self.root.bind('<Command-e>', self.toggle_delete_focus) # macOS


    ### CORE FUNCTIONS
    def save_thought(self):
        """Save current text thought to database."""
        # get all text from entry box, with stripped white space
        content = self.entry_box.get("1.0", tk.END).strip()
        # do nothing if entry box is empty
        if not content:
            return

        # Save Thought
        db.add_thought(content)                     # call database function to save
        self.entry_box.delete("1.0", tk.END) # clear entry box
        self.update_thoughts_view()                 # update viewer


    def delete_thought(self):
        """Delete thought by its ID."""
        # Get typed thought ID
        try:
            thought_id = int(self.delete_id_entry.get())
        except ValueError:  # do nothing if entry is not valid ID
            return

        # Confirmation Dialog
        answer = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete thought ID {thought_id}?")
        if answer:                                          # if Yes pressed
            db.delete_thought(thought_id)                   # delete thought from database
            self.update_thoughts_view()                     # refresh viewer
            self.delete_id_entry.delete(0, tk.END)     # clear delete entry box
            self.entry_box.focus_set()                      # move cursor back to thought entry box


    def update_thoughts_view(self):
        """Refresh viewer."""
        thoughts = db.get_all_thoughts()                # retrieve all thoughts
        self.thoughts_text.config(state=tk.NORMAL)      # temporarily enable editing
        self.thoughts_text.delete("1.0", tk.END) # delete previous contents

        # Get datetime for timestamp
        for thought_id, timestamp, content in thoughts:
            # try conversion
            try:
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.fromisoformat(timestamp)

            formatted_time = dt.strftime("%B %d, %Y @ %I:%M %p") # custom format for timestamp

            # Insert formatted thought into widget
            self.thoughts_text.insert(tk.END,
                                      f"{'-'*10}[{thought_id}]{'-'*10}\n{formatted_time}\n\n{content.strip()}\n\n"
            )

        self.thoughts_text.config(state=tk.DISABLED)    # disable editing


    ### KEYBOARD FUNCTIONS
    def handle_save_shortcut(self, event=None):
        """Handle saving keyboard shortcuts."""
        self.save_thought()
        return "break"


    def focus_delete_entry(self, event=None):
        """Focus cursor to delete entry box."""
        self.delete_id_entry.focus_set()                      # focus cursor to delete box
        self.delete_id_entry.select_range(0, tk.END)    # highlight all text
        return "break"


    def handle_delete_enter(self, event=None):
        """Allow pressing Enter in delete box."""
        self.delete_thought()
        return "break"          # Prevent default beep or other unwanted behavior


    def toggle_delete_focus(self, event=None):
        """Toggle focus between delete and main entry boxes."""
        focused = self.root.focus_get()
        if focused == self.delete_id_entry:                       # if focus in delete entry box
            self.entry_box.focus_set()                            # focus to main entry box
        else:
            self.delete_id_entry.focus_set()                      # focus to delete entry box
            self.delete_id_entry.select_range(0, tk.END)    # select all text to easily delete
        return "break"