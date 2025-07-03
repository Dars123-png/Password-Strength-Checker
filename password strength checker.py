import tkinter as tk
from tkinter import messagebox, ttk
import re
import nltk
from nltk.corpus import words
from cryptography.fernet import Fernet
import os

# Matplotlib to embed chart in Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Ensure NLTK words corpus is downloaded ---
try:
    english_words = set(words.words())
except LookupError:
    nltk.download('words')
    english_words = set(words.words())

# --- Encryption key handling ---
def get_or_create_key():
    key_file = 'key.key'
    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        return key

# --- Chart update ---
def update_chart(counts):
    for widget in chart_frame.winfo_children():
        widget.destroy()  # Clear old chart

    fig, ax = plt.subplots(figsize=(4,3), dpi=100)
    categories = list(counts.keys())
    values = [counts[c] for c in categories]

    ax.bar(categories, values, color=['blue', 'green', 'orange', 'red'])
    ax.set_title("Password Composition")
    ax.set_ylabel("Count")

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# --- Check password strength & update UI and chart ---
def check_strength():
    pwd = entry.get().strip()
    suggestions = []
    counts = {'Uppercase':0, 'Lowercase':0, 'Digits':0, 'Special':0}

    if not pwd:
        messagebox.showwarning("⚠️ Error", "Please enter a password.")
        return
    score = 0
    counts['Uppercase'] = len(re.findall(r"[A-Z]", pwd))
    counts['Lowercase'] = len(re.findall(r"[a-z]", pwd))
    counts['Digits']    = len(re.findall(r"\d", pwd))
    counts['Special']   = len(re.findall(r"[^A-Za-z0-9]", pwd))

    if len(pwd) >= 8:
        score += 1
    else:
        suggestions.append("🔒 Make it at least 8 characters.")
    if counts['Uppercase'] > 0:
        score += 1
    else:
        suggestions.append("🔠 Add uppercase letters.")
    if counts['Lowercase'] > 0:
        score += 1
    else:
        suggestions.append("🔡 Add lowercase letters.")
    if counts['Digits'] > 0:
        score += 1
    else:
        suggestions.append("🔢 Add digits.")
    if counts['Special'] > 0:
        score += 1
    else:
        suggestions.append("🔣 Add special symbols (!@#$ etc.).")

    core = re.sub(r"[^A-Za-z]", "", pwd).lower()
    if core and core in english_words:
        suggestions.append("⚠️ Avoid using simple dictionary words.")

    # Update strength bar & label
    strength = score * 20
    strength_bar['value'] = strength
    if score >= 4:
        percent_label.config(text="💪 Strong")
    elif score == 3:
        percent_label.config(text="👍 Moderate")
    else:
        percent_label.config(text="⚠️ Weak")

    if suggestions:
        advice = "\n".join(suggestions)
        messagebox.showinfo("Suggestions", advice)

    # Update embedded chart
    update_chart(counts)

# --- Save & Load password (same) ---
def save_password():
    pwd = entry.get().encode()
    if not pwd:
        messagebox.showwarning("⚠️ Error", "No password to save.")
        return
    key = get_or_create_key()
    cipher = Fernet(key)
    token = cipher.encrypt(pwd)
    try:
        with open('password.enc', 'wb') as f:
            f.write(token)
        messagebox.showinfo("✅ Saved", "Password encrypted and saved.")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to save password: {e}")

def load_password():
    try:
        key = get_or_create_key()
        cipher = Fernet(key)
        with open('password.enc', 'rb') as f:
            encrypted = f.read()
        decrypted = cipher.decrypt(encrypted).decode()
        messagebox.showinfo("🔓 Decrypted Password", f"Your password is:\n{decrypted}")
    except FileNotFoundError:
        messagebox.showerror("❌ Error", "No saved password found.")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to decrypt: {e}")

def toggle():
    entry.config(show="" if show_var.get() else "*")

# --- Tkinter UI setup ---
root = tk.Tk()
root.title("🔐 Password Strength Checker with Chart")

tk.Label(root, text="Enter Password:").pack(pady=5)
entry = tk.Entry(root, show="*", width=30)
entry.pack(pady=5)

show_var = tk.BooleanVar()
tk.Checkbutton(root, text="Show Password", variable=show_var, command=toggle).pack(pady=5)

tk.Button(root, text="Check Strength", command=check_strength).pack(pady=5)
tk.Button(root, text="Save Password", command=save_password).pack(pady=5)
tk.Button(root, text="Load Password", command=load_password).pack(pady=5)

frame_strength = tk.Frame(root)
frame_strength.pack(pady=5)
tk.Label(frame_strength, text="Password Strength").pack(side=tk.LEFT, padx=(0, 10))
strength_bar = ttk.Progressbar(frame_strength, orient="horizontal", length=200, mode="determinate")
strength_bar.pack(side=tk.LEFT)
percent_label = tk.Label(frame_strength, text="0%")
percent_label.pack(side=tk.LEFT, padx=(10,0))

# --- Frame to hold chart ---
chart_frame = tk.Frame(root)
chart_frame.pack(pady=10)

root.mainloop()
