import tkinter as tk
import subprocess
import sys
import os

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Application")
        self.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select an application to run:").pack(pady=10)

        quiz_maker_button = tk.Button(self, text="Quiz Maker", command=self.run_quiz_maker)
        quiz_maker_button.pack(fill=tk.X, padx=50, pady=5)

        quiz_taker_button = tk.Button(self, text="Quiz Taker", command=self.run_quiz_taker)
        quiz_taker_button.pack(fill=tk.X, padx=50, pady=5)

    def run_quiz_maker(self):
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), 'quiz_maker.py')])

    def run_quiz_taker(self):
        subprocess.Popen([sys.executable, os.path.join(os.getcwd(), 'quiz_taker.py')])

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
