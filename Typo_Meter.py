import tkinter as tk
from tkinter import font as tkfont
import random
import time

class SpeedTypingTest:
    def __init__(self, master):
        self.master = master
        self.master.title("Speed Typing Test")
        self.master.geometry("600x400")

        self.text_samples = self.load_text()

        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.label = tk.Label(self.frame, text="Welcome to the Speed Typing Test", font=("Arial", 16))
        self.label.pack(pady=10)

        self.text_display = tk.Text(self.frame, wrap=tk.WORD, font=("Arial", 14), height=4, width=50, state='disabled')
        self.text_display.pack(pady=20)

        self.entry = tk.Entry(self.frame, font=("Arial", 14), width=50, state='disabled')
        self.entry.pack(pady=10)
        self.entry.bind('<KeyRelease>', self.check_input)

        self.start_button = tk.Button(self.frame, text="Start Test", command=self.start_test)
        self.start_button.pack(pady=10)

        self.result_label = tk.Label(self.frame, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.wpm_label = tk.Label(self.frame, text="WPM: 0", font=("Arial", 14))
        self.wpm_label.pack(pady=5)

        # Configure text tags for coloring
        self.text_display.tag_configure("correct", foreground="green")
        self.text_display.tag_configure("incorrect", foreground="red")

    def load_text(self):
        with open("TestCases.txt", "r") as f:
            return [line.strip() for line in f.readlines()]

    def start_test(self):
        self.target_text = random.choice(self.text_samples)
        self.text_display.config(state='normal')
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, self.target_text)
        self.text_display.config(state='disabled')
        self.entry.config(state='normal')
        self.entry.delete(0, tk.END)
        self.start_time = time.time()
        self.start_button.config(state=tk.DISABLED)
        self.result_label.config(text="")
        self.entry.focus()

        self.update_wpm()

    def check_input(self, event):
        current_text = self.entry.get()
        self.update_text_colors(current_text)
        
        if current_text == self.target_text:
            self.end_test()

    def update_text_colors(self, current_text):
        self.text_display.config(state='normal')
        self.text_display.delete(1.0, tk.END)
        
        for i, char in enumerate(self.target_text):
            if i < len(current_text):
                if char == current_text[i]:
                    self.text_display.insert(tk.END, char, "correct")
                else:
                    self.text_display.insert(tk.END, char, "incorrect")
            else:
                self.text_display.insert(tk.END, char)
        
        self.text_display.config(state='disabled')

    def end_test(self):
        end_time = time.time()
        time_taken = end_time - self.start_time
        words = len(self.target_text.split())
        wpm = int((words / time_taken) * 60)
        self.result_label.config(text=f"Test completed! Your speed: {wpm} WPM")
        self.entry.config(state='disabled')
        self.start_button.config(state=tk.NORMAL)

    def update_wpm(self):
        if self.entry['state'] == 'normal':
            current_time = time.time()
            time_elapsed = current_time - self.start_time
            if time_elapsed > 0:
                words_typed = len(self.entry.get().split())
                current_wpm = int((words_typed / time_elapsed) * 60)
                self.wpm_label.config(text=f"WPM: {current_wpm}")
            self.master.after(1000, self.update_wpm)  

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTypingTest(root)
    root.mainloop()