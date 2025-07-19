import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import threading
import os

wordlist = []

def load_wordlist():
    global wordlist
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path and os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            wordlist = [line.strip() for line in file if line.strip()]
        messagebox.showinfo("Success", f"Loaded {len(wordlist)} words from {os.path.basename(file_path)}.")
    else:
        messagebox.showerror("Error", "Invalid wordlist file.")

def crack_password():
    target_password = password_entry.get()

    if not target_password:
        messagebox.showwarning("Input Required", "Please enter a password to crack.")
        return
    if not wordlist:
        messagebox.showwarning("Wordlist Required", "Please load a wordlist first.")
        return

    crack_btn.config(state=tk.DISABLED)
    progress_bar["value"] = 0
    log_box.delete(1.0, tk.END)
    result_label.config(text="")

    def run_crack():
        start_time = time.time()  # Start the timer

        for i, word in enumerate(wordlist):
            time.sleep(0.001)  # Simulate cracking speed
            log_box.insert(tk.END, f"Trying: {word}\n")
            log_box.see(tk.END)

            progress = int(((i + 1) / len(wordlist)) * 100)
            progress_bar["value"] = progress
            root.update()

            if word == target_password:
                elapsed_time = time.time() - start_time  # Calculate elapsed time
                result_label.config(
                    text=f"✅ Password Cracked: {word}\n⏱️ Time Taken: {elapsed_time:.2f} seconds",
                    fg="lime"
                )
                crack_btn.config(state=tk.NORMAL)
                return

        result_label.config(text="❌ Password Not Found", fg="red")
        crack_btn.config(state=tk.NORMAL)

    threading.Thread(target=run_crack).start()

# GUI setup
root = tk.Tk()
root.title("Password Cracker with Wordlist Support")
root.geometry("550x500")
root.config(bg="#121212")

style = ttk.Style()
style.theme_use("clam")
style.configure("TProgressbar", foreground='green', background='lime')

tk.Label(root, text="🕵️‍♂️ Password Cracker", font=("Courier New", 18, "bold"),
         bg="#121212", fg="lime").pack(pady=10)

tk.Label(root, text="Enter Password to Crack:", bg="#121212", fg="white", font=("Arial", 12)).pack()
password_entry = tk.Entry(root, show="*", font=("Arial", 12), width=30)
password_entry.pack(pady=5)

tk.Button(root, text="Load Wordlist", command=load_wordlist,
          bg="#2e8b57", fg="white", font=("Arial", 11)).pack(pady=5)

crack_btn = tk.Button(root, text="Start Cracking", command=crack_password,
                      font=("Arial", 12, "bold"), bg="#ff4d4d", fg="white", padx=10, pady=5)
crack_btn.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
progress_bar.pack(pady=5)

tk.Label(root, text="Cracking Log:", bg="#121212", fg="white", font=("Arial", 12)).pack(pady=5)
log_box = tk.Text(root, height=10, width=60, bg="black", fg="lime", font=("Courier", 10))
log_box.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#121212")
result_label.pack(pady=10)

root.mainloop()
