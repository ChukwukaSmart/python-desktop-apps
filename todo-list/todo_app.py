"""
Simple To-Do List Desktop App
Built with Tkinter (comes built-in with Python, no extra installs needed)
Saves tasks to a local file so they persist between sessions.
"""

import tkinter as tk
from tkinter import messagebox
import json
import os

SAVE_FILE = "todo_data.json"


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My To-Do List")
        self.root.geometry("420x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f9")

        self.tasks = []

        # --- Title ---
        title_label = tk.Label(
            root, text="To-Do List", font=("Helvetica", 18, "bold"),
            bg="#f4f4f9", fg="#333"
        )
        title_label.pack(pady=10)

        # --- Entry + Add button frame ---
        entry_frame = tk.Frame(root, bg="#f4f4f9")
        entry_frame.pack(pady=5)

        self.task_entry = tk.Entry(entry_frame, width=28, font=("Helvetica", 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        add_btn = tk.Button(
            entry_frame, text="Add", width=8, bg="#4CAF50", fg="white",
            font=("Helvetica", 10, "bold"), command=self.add_task
        )
        add_btn.pack(side=tk.LEFT)

        # --- Listbox to show tasks ---
        list_frame = tk.Frame(root)
        list_frame.pack(pady=10)

        self.task_listbox = tk.Listbox(
            list_frame, width=45, height=15, font=("Helvetica", 11),
            selectbackground="#a6d4fa", activestyle="none"
        )
        self.task_listbox.pack(side=tk.LEFT)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        self.task_listbox.bind("<Double-Button-1>", lambda event: self.toggle_done())

        # --- Buttons frame ---
        btn_frame = tk.Frame(root, bg="#f4f4f9")
        btn_frame.pack(pady=10)

        complete_btn = tk.Button(
            btn_frame, text="Mark Done", width=12, command=self.toggle_done
        )
        complete_btn.grid(row=0, column=0, padx=5)

        delete_btn = tk.Button(
            btn_frame, text="Delete", width=12, command=self.delete_task
        )
        delete_btn.grid(row=0, column=1, padx=5)

        clear_btn = tk.Button(
            btn_frame, text="Clear All", width=12, command=self.clear_all
        )
        clear_btn.grid(row=0, column=2, padx=5)

        # Load any previously saved tasks
        self.load_tasks()

        # Save tasks when window is closed
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_task(self):
        task_text = self.task_entry.get().strip()
        if task_text == "":
            messagebox.showwarning("Empty Task", "Please type a task before adding.")
            return
        self.tasks.append({"text": task_text, "done": False})
        self.task_entry.delete(0, tk.END)
        self.refresh_listbox()

    def toggle_done(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showinfo("No Selection", "Select a task first.")
            return
        index = selected[0]
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.refresh_listbox()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showinfo("No Selection", "Select a task to delete.")
            return
        index = selected[0]
        del self.tasks[index]
        self.refresh_listbox()

    def clear_all(self):
        if not self.tasks:
            return
        confirm = messagebox.askyesno("Clear All", "Delete all tasks?")
        if confirm:
            self.tasks = []
            self.refresh_listbox()

    def refresh_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            prefix = "[x] " if task["done"] else "[ ] "
            self.task_listbox.insert(tk.END, prefix + task["text"])
            if task["done"]:
                self.task_listbox.itemconfig(tk.END, fg="gray")

    def save_tasks(self):
        with open(SAVE_FILE, "w") as f:
            json.dump(self.tasks, f, indent=2)

    def load_tasks(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    self.tasks = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.tasks = []
        self.refresh_listbox()

    def on_close(self):
        self.save_tasks()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
