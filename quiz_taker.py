import tkinter as tk
from tkinter import messagebox, ttk
import os
import xml.etree.ElementTree as ET

QUIZZES_DIR = "quizzes"

class QuizTakerApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Quiz Taker")
        self.geometry("800x600")
        self.create_widgets()
        self.populate_quiz_list()

    def create_widgets(self):
        self.quiz_listbox = tk.Listbox(self)
        self.quiz_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.quiz_listbox.bind('<<ListboxSelect>>', self.on_quiz_selected)

        self.start_button = tk.Button(self, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack(side=tk.BOTTOM)

    def populate_quiz_list(self):
        self.quiz_listbox.delete(0, tk.END)
        if not os.path.exists(QUIZZES_DIR):
            os.makedirs(QUIZZES_DIR)
        for file in os.listdir(QUIZZES_DIR):
            if file.endswith('.qqz'):
                self.quiz_listbox.insert(tk.END, file)

    def on_quiz_selected(self, event):
        selection = self.quiz_listbox.curselection()
        if selection:
            self.selected_quiz = self.quiz_listbox.get(selection[0])

    def start_quiz(self):
        if hasattr(self, 'selected_quiz'):
            quiz_path = os.path.join(QUIZZES_DIR, self.selected_quiz)
            self.quiz_window = QuizWindow(self, quiz_path)
            self.quiz_window.grab_set()

class QuizWindow(tk.Toplevel):
    def __init__(self, parent, quiz_path):
        super().__init__(parent)
        self.quiz_path = quiz_path
        self.load_quiz()
        self.current_question_index = 0
        self.selected_answer = tk.StringVar()
        self.create_widgets()
        self.correct_answers_count = 0

    def load_quiz(self):
        self.quiz_tree = ET.parse(self.quiz_path)
        self.quiz_root = self.quiz_tree.getroot()
        self.questions = self.quiz_root.findall('question')

    def create_widgets(self):
        self.question_label = tk.Label(self, text="")
        self.question_label.pack()

        self.answer_frame = tk.Frame(self)
        self.answer_frame.pack()

        self.next_button = tk.Button(self, text="Next", command=self.next_question)
        self.next_button.pack()

        self.display_question()



    def display_question(self):
        self.clear_answers()
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            # Check if 'prompt' is an attribute or a child, and retrieve text accordingly
            question_text = question.get('prompt') if question.get('prompt') else question.find('prompt').text
            print("Displaying question text:", question_text)  # Debugging output
            self.question_label.config(text=question_text)

            answers = question.findall('answer')
            if not answers:  # Check if answers are found
                print("No answers found for question:", question_text)
            for i, answer in enumerate(answers):
                # Assuming answer text is directly within the answer element
                answer_text = answer.text
                print(f"Creating radio button for answer {i}: {answer_text}")  # Debugging output
                rb = tk.Radiobutton(self.answer_frame, text=answer_text, variable=self.selected_answer, value=str(i))
                rb.pack(anchor=tk.W)
            # After packing widgets, print the size of the answer_frame to debug
            print("answer_frame size:", self.answer_frame.winfo_width(), "x", self.answer_frame.winfo_height())
        else:
            self.finish_quiz()


    def clear_answers(self):
        for widget in self.answer_frame.winfo_children():
            widget.destroy()


    def next_question(self):
        current_question = self.questions[self.current_question_index]
        selected_answer_index = int(self.selected_answer.get())
        answers = current_question.findall('answer')
        
        if 'correct' in answers[selected_answer_index].attrib and answers[selected_answer_index].get('correct') == "yes":
            self.correct_answers_count += 1
        
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            self.finish_quiz()

    def finish_quiz(self):
        total_questions = len(self.questions)
        score_percentage = (self.correct_answers_count / total_questions) * 100
        messagebox.showinfo(
            "Quiz Finished",
            f"The quiz is complete! You got {self.correct_answers_count} out of {total_questions} right.\nScore: {score_percentage:.2f}%"
        )
        self.destroy()


    def finish_quiz(self):
        total_questions = len(self.questions)
        score_percentage = (self.correct_answers_count / total_questions) * 100
        messagebox.showinfo(
            "Quiz Finished",
            f"The quiz is complete! You got {self.correct_answers_count} out of {total_questions} right.\nScore: {score_percentage:.2f}%"
        )
        self.destroy()


if __name__ == "__main__":
    app = QuizTakerApp()
    app.mainloop()
