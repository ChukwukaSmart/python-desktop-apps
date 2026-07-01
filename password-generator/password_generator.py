"""
Password Generator Desktop App
Built with Tkinter (built-in) + pyperclip (for clipboard copy)

Install the one extra dependency before running:
    pip install pyperclip
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("420x420")
        self.root.resizable(False, False)
        self.root.configure(bg="#f4f4f9")

        title_label = tk.Label(
            root, text="Password Generator", font=("Helvetica", 18, "bold"),
            bg="#f4f4f9", fg="#333"
        )
        title_label.pack(pady=15)

        # --- Length selector ---
        length_frame = tk.Frame(root, bg="#f4f4f9")
        length_frame.pack(pady=10)

        tk.Label(
            length_frame, text="Password Length:", font=("Helvetica", 11),
            bg="#f4f4f9"
        ).pack(side=tk.LEFT, padx=5)

        self.length_var = tk.IntVar(value=12)
        self.length_spinbox = tk.Spinbox(
            length_frame, from_=4, to=64, textvariable=self.length_var,
            width=5, font=("Helvetica", 11)
        )
        self.length_spinbox.pack(side=tk.LEFT, padx=5)

        # --- Character type options ---
        options_frame = tk.LabelFrame(
            root, text="Include", font=("Helvetica", 11, "bold"),
            bg="#f4f4f9", padx=15, pady=10
        )
        options_frame.pack(pady=15, padx=30, fill="x")

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)

        tk.Checkbutton(
            options_frame, text="Uppercase letters (A-Z)", variable=self.use_upper,
            bg="#f4f4f9", anchor="w"
        ).pack(fill="x")
        tk.Checkbutton(
            options_frame, text="Lowercase letters (a-z)", variable=self.use_lower,
            bg="#f4f4f9", anchor="w"
        ).pack(fill="x")
        tk.Checkbutton(
            options_frame, text="Digits (0-9)", variable=self.use_digits,
            bg="#f4f4f9", anchor="w"
        ).pack(fill="x")
        tk.Checkbutton(
            options_frame, text="Symbols (!@#$...)", variable=self.use_symbols,
            bg="#f4f4f9", anchor="w"
        ).pack(fill="x")

        # --- Exclude ambiguous characters option ---
        self.exclude_ambiguous = tk.BooleanVar(value=False)
        tk.Checkbutton(
            options_frame, text="Exclude ambiguous chars (l, 1, O, 0)",
            variable=self.exclude_ambiguous, bg="#f4f4f9", anchor="w"
        ).pack(fill="x")

        # --- Generate button ---
        generate_btn = tk.Button(
            root, text="Generate Password", font=("Helvetica", 11, "bold"),
            bg="#4CAF50", fg="white", command=self.generate_password
        )
        generate_btn.pack(pady=10)

        # --- Result display ---
        result_frame = tk.Frame(root, bg="#f4f4f9")
        result_frame.pack(pady=10)

        self.result_var = tk.StringVar()
        self.result_entry = tk.Entry(
            result_frame, textvariable=self.result_var, font=("Consolas", 13),
            width=28, justify="center", state="readonly"
        )
        self.result_entry.pack(side=tk.LEFT, padx=5)

        copy_btn = tk.Button(
            result_frame, text="Copy", width=8, bg="#2196F3", fg="white",
            font=("Helvetica", 10, "bold"), command=self.copy_to_clipboard
        )
        copy_btn.pack(side=tk.LEFT)

        # --- Strength indicator ---
        self.strength_label = tk.Label(
            root, text="", font=("Helvetica", 10, "bold"), bg="#f4f4f9"
        )
        self.strength_label.pack(pady=5)

        # Generate one immediately on launch
        self.generate_password()

    def generate_password(self):
        length = self.length_var.get()

        char_pool = ""
        if self.use_upper.get():
            char_pool += string.ascii_uppercase
        if self.use_lower.get():
            char_pool += string.ascii_lowercase
        if self.use_digits.get():
            char_pool += string.digits
        if self.use_symbols.get():
            char_pool += "!@#$%^&*()-_=+[]{};:,.<>?"

        if self.exclude_ambiguous.get():
            for ch in "l1O0Iio":
                char_pool = char_pool.replace(ch, "")

        if not char_pool:
            messagebox.showwarning(
                "No Character Types Selected",
                "Please select at least one character type."
            )
            return

        # Make sure at least one char from each selected category appears
        password_chars = []
        categories = []
        if self.use_upper.get():
            categories.append(string.ascii_uppercase)
        if self.use_lower.get():
            categories.append(string.ascii_lowercase)
        if self.use_digits.get():
            categories.append(string.digits)
        if self.use_symbols.get():
            categories.append("!@#$%^&*()-_=+[]{};:,.<>?")

        for cat in categories:
            if self.exclude_ambiguous.get():
                cat = "".join(c for c in cat if c not in "l1O0Iio")
            if cat:
                password_chars.append(random.choice(cat))

        remaining_length = max(length - len(password_chars), 0)
        password_chars += [random.choice(char_pool) for _ in range(remaining_length)]
        random.shuffle(password_chars)
        password = "".join(password_chars[:length])

        self.result_var.set(password)
        self.update_strength_label(password)

    def update_strength_label(self, password):
        length = len(password)
        variety = sum([
            any(c.isupper() for c in password),
            any(c.islower() for c in password),
            any(c.isdigit() for c in password),
            any(c in "!@#$%^&*()-_=+[]{};:,.<>?" for c in password),
        ])

        if length >= 16 and variety >= 4:
            strength, color = "Strong", "#2e7d32"
        elif length >= 10 and variety >= 3:
            strength, color = "Medium", "#f9a825"
        else:
            strength, color = "Weak", "#c62828"

        self.strength_label.config(text=f"Strength: {strength}", fg=color)

    def copy_to_clipboard(self):
        password = self.result_var.get()
        if not password:
            return
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
