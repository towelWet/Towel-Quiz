import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import xml.etree.ElementTree as ET

QUIZZES_DIR = "quizzes"

class QuizMakerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Maker")
        self.geometry("800x600")
        self.create_widgets()
        self.populate_quiz_list()

    def create_widgets(self):
        self.quiz_listbox = tk.Listbox(self)
        self.quiz_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.quiz_listbox.bind('<<ListboxSelect>>', self.on_quiz_selected)

        self.add_quiz_button = tk.Button(self, text="Add New Quiz", command=self.create_quiz)
        self.add_quiz_button.pack(side=tk.BOTTOM)

    def populate_quiz_list(self):
        if not os.path.exists(QUIZZES_DIR):
            os.makedirs(QUIZZES_DIR)
        self.quiz_listbox.delete(0, tk.END)
        for file in os.listdir(QUIZZES_DIR):
            if file.endswith('.qqz'):
                self.quiz_listbox.insert(tk.END, file)

    def on_quiz_selected(self, event):
        selection = self.quiz_listbox.curselection()
        if selection:
            selected_quiz = self.quiz_listbox.get(selection[0])
            quiz_path = os.path.join(QUIZZES_DIR, selected_quiz)
            self.edit_quiz(quiz_path)

    def create_quiz(self):
        quiz_name = simpledialog.askstring("Create Quiz", "Enter quiz name:")
        if quiz_name:
            quiz_path = os.path.join(QUIZZES_DIR, f"{quiz_name}.qqz")
            if not os.path.exists(quiz_path):
                quiz = ET.Element('quiz', name=quiz_name)
                tree = ET.ElementTree(quiz)
                tree.write(quiz_path, encoding='utf-8', xml_declaration=True)
                self.populate_quiz_list()
                messagebox.showinfo("Success", f"Quiz '{quiz_name}' created successfully.")
            else:
                messagebox.showerror("Error", "A quiz with this name already exists.")

    def edit_quiz(self, quiz_path):
        quiz_editor = QuizEditor(self, quiz_path)
        quiz_editor.grab_set()

class QuizEditor(tk.Toplevel):
    def __init__(self, parent, quiz_path):
        super().__init__(parent)
        self.quiz_path = quiz_path
        self.create_widgets()
        self.load_quiz()

    def create_widgets(self):
        self.question_listbox = tk.Listbox(self)
        self.question_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.question_listbox.bind('<<ListboxSelect>>', self.on_question_selected)

        self.add_question_button = tk.Button(self, text="Add New Question", command=self.add_question)
        self.add_question_button.pack(side=tk.BOTTOM)

        self.edit_area = tk.Frame(self)
        self.edit_area.pack(side=tk.RIGHT, fill="both", expand=True)

    def load_quiz(self):
        self.quiz_tree = ET.parse(self.quiz_path)
        self.quiz_root = self.quiz_tree.getroot()
        self.populate_question_list()

    def populate_question_list(self):
        self.question_listbox.delete(0, tk.END)
        for question in self.quiz_root.findall('question'):
            self.question_listbox.insert(tk.END, question.get('prompt'))

    def on_question_selected(self, event):
        selection = self.question_listbox.curselection()
        if selection:
            self.selected_question = self.quiz_root.findall('question')[selection[0]]
            self.display_question_editor()

    def add_question(self):
        question_text = simpledialog.askstring("New Question", "Enter the question:")
        if question_text:
            new_question = ET.SubElement(self.quiz_root, 'question', prompt=question_text)
            ET.SubElement(new_question, 'answers')
            self.save_quiz()


    def display_question_editor(self):
        for widget in self.edit_area.winfo_children():
            widget.destroy()
        self.correct_vars = []  # Reset the list of BooleanVars

        if not self.selected_question:
            return

        self.question_entry = tk.Entry(self.edit_area, width=50)
        self.question_entry.insert(0, self.selected_question.get('prompt'))
        self.question_entry.pack()

        self.answers_frame = tk.Frame(self.edit_area)
        self.answers_frame.pack(fill=tk.BOTH, expand=True)

        answers_element = self.selected_question.find('answers')
        if answers_element is None:
            answers_element = ET.SubElement(self.selected_question, 'answers')

        for answer in answers_element.findall('answer'):
            self.add_answer_editor(answer)

        self.add_answer_button = tk.Button(self.edit_area, text="Add Answer", command=self.add_new_answer_editor)
        self.add_answer_button.pack()

        self.save_button = tk.Button(self.edit_area, text="Save Question", command=self.save_question)
        self.save_button.pack()
            



    def add_answer_editor(self, answer=None):
        answer_frame = tk.Frame(self.answers_frame)
        answer_frame.pack(fill="x", padx=5, pady=2)

        answer_text = tk.Entry(answer_frame, width=40)
        answer_text.pack(side="left", fill="x", expand=True)
        if answer is not None:
            answer_text.insert(0, answer.get('text'))

        is_correct = tk.BooleanVar(value=answer.get('correct') == 'yes' if answer is not None else False)
        correct_check = tk.Checkbutton(answer_frame, text="Correct", variable=is_correct)
        correct_check.pack(side="left")

        delete_button = tk.Button(answer_frame, text="Delete", command=lambda: self.delete_answer(answer, answer_frame))
        delete_button.pack(side="right")

        answer_frame.answer_text_widget = answer_text
        answer_frame.is_correct_var = is_correct
        self.correct_vars.append(is_correct)


    def add_new_answer_editor(self):
        if self.selected_question is None:
            messagebox.showerror("Error", "Please select a question first.")
            return
        self.add_answer_editor()

    def delete_answer(self, answer, answer_frame):
        if answer is not None:
            answers_element = self.selected_question.find('answers')
            answers_element.remove(answer)
        answer_frame.destroy()

    def save_question(self):
        question_text = self.question_entry.get()
        if question_text:
            self.selected_question.set('prompt', question_text)
            answers_element = self.selected_question.find('answers')
            answers_element.clear()

            for answer_frame in self.answers_frame.winfo_children():
                # Directly access the Entry widget and BooleanVar stored in the frame
                answer_text = answer_frame.answer_text_widget.get()
                is_correct = answer_frame.is_correct_var.get()

                # Only add the answer if there is text
                if answer_text.strip():
                    ET.SubElement(answers_element, 'answer', text=answer_text, correct='yes' if is_correct else 'no')

            # Write the updated XML to file and refresh the question list
            self.save_quiz()
        else:
            messagebox.showerror("Error", "The question text cannot be empty.")

            
    def save_quiz(self):
        self.quiz_tree.write(self.quiz_path, encoding='utf-8', xml_declaration=True)
        self.populate_question_list()

if __name__ == "__main__":
    app = QuizMakerApp()
    app.mainloop()
