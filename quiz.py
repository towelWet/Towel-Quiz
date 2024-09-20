import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, scrolledtext
from tkinter import ttk
import os
import shutil
import xml.etree.ElementTree as ET
import subprocess
import sys

def get_documents_folder():
    if sys.platform == 'win32':
        return os.path.join(os.environ['USERPROFILE'], 'Documents')
    elif sys.platform == 'darwin':  # macOS
        return os.path.join(os.path.expanduser('~'), 'Documents')
    else:
        # For Linux and other systems, default to the home directory
        return os.path.join(os.path.expanduser('~'), 'Documents')

def get_quizzes_dir():
    return os.path.join(get_documents_folder(), 'quizzes')

QUIZZES_DIR = get_quizzes_dir()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quiz Application")
        self.geometry("300x200")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select an option:").pack(pady=10)

        quiz_maker_button = tk.Button(self, text="Quiz Maker", command=self.open_quiz_maker)
        quiz_maker_button.pack(fill=tk.X, padx=50, pady=5)

        quiz_taker_button = tk.Button(self, text="Quiz Taker", command=self.open_quiz_taker)
        quiz_taker_button.pack(fill=tk.X, padx=50, pady=5)

    def open_quiz_maker(self):
        quiz_maker = QuizMakerApp(self)
        quiz_maker.grab_set()

    def open_quiz_taker(self):
        quiz_taker = QuizTakerApp(self)
        quiz_taker.grab_set()

# --------------------------- Quiz Maker Classes ---------------------------

class QuizMakerApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Quiz Maker")
        self.geometry("800x600")
        self.create_widgets()
        self.populate_quiz_tree()

    def create_widgets(self):
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Use Treeview instead of Listbox
        self.quiz_tree = ttk.Treeview(left_frame)
        self.quiz_tree.heading('#0', text='Quizzes', anchor='w')
        self.quiz_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.quiz_tree.bind('<<TreeviewSelect>>', self.on_quiz_selected)
        self.quiz_tree.bind('<Button-3>', self.show_context_menu)

        buttons_frame = tk.Frame(left_frame)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.add_quiz_button = tk.Button(buttons_frame, text="Add New Quiz", command=self.create_quiz)
        self.add_quiz_button.pack(fill=tk.X)

        self.add_folder_button = tk.Button(buttons_frame, text="Create New Folder", command=self.create_folder)
        self.add_folder_button.pack(fill=tk.X)

        self.import_quiz_button = tk.Button(buttons_frame, text="Import Quiz", command=self.import_quiz)
        self.import_quiz_button.pack(fill=tk.X)

        self.browse_quiz_dir_button = tk.Button(buttons_frame, text="Browse Quiz Directory", command=self.browse_quiz_directory)
        self.browse_quiz_dir_button.pack(fill=tk.X)

    def populate_quiz_tree(self):
        if not os.path.exists(QUIZZES_DIR):
            os.makedirs(QUIZZES_DIR)
        self.quiz_tree.delete(*self.quiz_tree.get_children())
        self.insert_tree_items('', QUIZZES_DIR)

    def insert_tree_items(self, parent, path):
        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                node = self.quiz_tree.insert(parent, 'end', text=item, open=False)
                self.insert_tree_items(node, full_path)
            elif item.endswith('.qqz'):
                self.quiz_tree.insert(parent, 'end', text=item, values=(full_path,))

    def on_quiz_selected(self, event):
        selection = self.quiz_tree.selection()
        if selection:
            item = self.quiz_tree.item(selection[0])
            full_path = self.get_full_path(selection[0])
            if os.path.isfile(full_path) and full_path.endswith('.qqz'):
                self.edit_quiz(full_path)

    def get_full_path(self, item_id):
        parts = []
        while item_id:
            item = self.quiz_tree.item(item_id)
            parts.insert(0, item['text'])
            item_id = self.quiz_tree.parent(item_id)
        return os.path.join(QUIZZES_DIR, *parts)

    def create_quiz(self):
        quiz_name = simpledialog.askstring("Create Quiz", "Enter quiz name:")
        if quiz_name:
            selection = self.quiz_tree.selection()
            if selection:
                folder_selected = self.get_full_path(selection[0])
                if not os.path.isdir(folder_selected):
                    folder_selected = os.path.dirname(folder_selected)
            else:
                folder_selected = QUIZZES_DIR
            quiz_path = os.path.join(folder_selected, f"{quiz_name}.qqz")
            if not os.path.exists(quiz_path):
                quiz = ET.Element('quiz', name=quiz_name)
                tree = ET.ElementTree(quiz)
                os.makedirs(os.path.dirname(quiz_path), exist_ok=True)
                tree.write(quiz_path, encoding='utf-8', xml_declaration=True)
                self.populate_quiz_tree()
                messagebox.showinfo("Success", f"Quiz '{quiz_name}' created successfully.")
            else:
                messagebox.showerror("Error", "A quiz with this name already exists.")

    def create_folder(self):
        folder_name = simpledialog.askstring("Create Folder", "Enter folder name:")
        if folder_name:
            selection = self.quiz_tree.selection()
            if selection:
                parent_folder = self.get_full_path(selection[0])
                if not os.path.isdir(parent_folder):
                    parent_folder = os.path.dirname(parent_folder)
            else:
                parent_folder = QUIZZES_DIR
            new_folder_path = os.path.join(parent_folder, folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                self.populate_quiz_tree()
                messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully.")
            else:
                messagebox.showerror("Error", "A folder with this name already exists.")

    def import_quiz(self):
        file_path = filedialog.askopenfilename(
            title="Import Quiz",
            filetypes=[("Quiz Files", "*.qqz"), ("XML Files", "*.xml"), ("All Files", "*.*")]
        )
        if file_path:
            selection = self.quiz_tree.selection()
            if selection:
                folder_selected = self.get_full_path(selection[0])
                if not os.path.isdir(folder_selected):
                    folder_selected = os.path.dirname(folder_selected)
            else:
                folder_selected = QUIZZES_DIR
            quiz_name = os.path.basename(file_path)
            destination = os.path.join(folder_selected, quiz_name)
            if os.path.exists(destination):
                messagebox.showerror("Error", "A quiz with this name already exists in the selected folder.")
            else:
                shutil.copy(file_path, destination)
                self.populate_quiz_tree()
                messagebox.showinfo("Success", f"Quiz '{quiz_name}' imported successfully.")

    def browse_quiz_directory(self):
        if sys.platform.startswith('darwin'):
            subprocess.Popen(['open', QUIZZES_DIR])
        elif os.name == 'nt':
            os.startfile(QUIZZES_DIR)
        elif os.name == 'posix':
            subprocess.Popen(['xdg-open', QUIZZES_DIR])
        else:
            messagebox.showerror("Error", "Cannot open directory on this operating system.")

    def show_context_menu(self, event):
        item_id = self.quiz_tree.identify_row(event.y)
        if item_id:
            self.quiz_tree.selection_set(item_id)
            context_menu = tk.Menu(self, tearoff=0)
            context_menu.add_command(label="Rename", command=lambda: self.rename_item(item_id))
            context_menu.add_command(label="Delete", command=lambda: self.delete_item(item_id))
            context_menu.add_command(label="Move", command=lambda: self.move_item(item_id))
            context_menu.tk_popup(event.x_root, event.y_root)

    def rename_item(self, item_id):
        full_path = self.get_full_path(item_id)
        new_name = simpledialog.askstring("Rename", "Enter new name:")
        if new_name:
            parent_path = os.path.dirname(full_path)
            new_path = os.path.join(parent_path, new_name)
            if os.path.isdir(full_path):
                if not os.path.exists(new_path):
                    os.rename(full_path, new_path)
                    self.populate_quiz_tree()
                else:
                    messagebox.showerror("Error", "A folder with this name already exists.")
            elif os.path.isfile(full_path):
                if not new_path.endswith('.qqz'):
                    new_path += '.qqz'
                if not os.path.exists(new_path):
                    os.rename(full_path, new_path)
                    self.populate_quiz_tree()
                else:
                    messagebox.showerror("Error", "A quiz with this name already exists.")

    def delete_item(self, item_id):
        full_path = self.get_full_path(item_id)
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{full_path}'?")
        if confirm:
            try:
                if os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                elif os.path.isfile(full_path):
                    os.remove(full_path)
                self.populate_quiz_tree()
                messagebox.showinfo("Success", "Item deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete item: {e}")

    def move_item(self, item_id):
        full_path = self.get_full_path(item_id)
        destination = filedialog.askdirectory(initialdir=QUIZZES_DIR, title="Select Destination Folder")
        if destination:
            if os.path.commonpath([full_path]) == os.path.commonpath([full_path, destination]):
                messagebox.showerror("Error", "Cannot move a folder inside itself.")
                return
            new_path = os.path.join(destination, os.path.basename(full_path))
            if not os.path.exists(new_path):
                shutil.move(full_path, new_path)
                self.populate_quiz_tree()
                messagebox.showinfo("Success", "Item moved successfully.")
            else:
                messagebox.showerror("Error", "An item with the same name already exists in the destination.")

    def edit_quiz(self, quiz_path):
        quiz_editor = QuizEditor(self, quiz_path)
        quiz_editor.grab_set()

class QuizEditor(tk.Toplevel):
    def __init__(self, parent, quiz_path):
        super().__init__(parent)
        self.quiz_path = quiz_path
        self.selected_question = None
        self.create_widgets()
        self.load_quiz()

    def create_widgets(self):
        self.title("Quiz Editor")
        self.geometry("800x600")

        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.question_listbox = tk.Listbox(left_frame)
        self.question_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.question_listbox.bind('<<ListboxSelect>>', self.on_question_selected)

        buttons_frame = tk.Frame(left_frame)
        buttons_frame.pack(side=tk.BOTTOM, fill=tk.X)

        add_question_button = tk.Button(buttons_frame, text="Add New Question", command=self.add_question)
        add_question_button.pack(fill=tk.X)

        remove_question_button = tk.Button(buttons_frame, text="Remove Question", command=self.remove_question)
        remove_question_button.pack(fill=tk.X)

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
            self.save_quiz()
            self.populate_question_list()

    def remove_question(self):
        selection = self.question_listbox.curselection()
        if selection:
            question_index = selection[0]
            question = self.quiz_root.findall('question')[question_index]
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove this question?")
            if confirm:
                self.quiz_root.remove(question)
                self.save_quiz()
                self.populate_question_list()
                self.clear_edit_area()
        else:
            messagebox.showerror("Error", "Please select a question to remove.")

    def clear_edit_area(self):
        for widget in self.edit_area.winfo_children():
            widget.destroy()
        self.selected_question = None

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

        for answer in self.selected_question.findall('answer'):
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
            answer_text.insert(0, answer.text if answer.text is not None else "")

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
            self.selected_question.remove(answer)
        answer_frame.destroy()

    def save_question(self):
        question_text = self.question_entry.get()
        if question_text:
            self.selected_question.set('prompt', question_text)

            # Remove all existing answer elements
            for answer in self.selected_question.findall('answer'):
                self.selected_question.remove(answer)

            # Add new answer elements
            for answer_frame in self.answers_frame.winfo_children():
                answer_text = answer_frame.answer_text_widget.get()
                is_correct = answer_frame.is_correct_var.get()

                if answer_text.strip():
                    answer_element = ET.SubElement(self.selected_question, 'answer')
                    if is_correct:
                        answer_element.set('correct', 'yes')
                    answer_element.text = answer_text

            # Write the updated XML to file and refresh the question list
            self.save_quiz()
            messagebox.showinfo("Success", "Question saved successfully.")
        else:
            messagebox.showerror("Error", "The question text cannot be empty.")

    def save_quiz(self):
        self.quiz_tree.write(self.quiz_path, encoding='utf-8', xml_declaration=True)
        self.populate_question_list()

# --------------------------- Quiz Taker Classes ---------------------------

class QuizTakerApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Quiz Taker")
        self.geometry("800x600")
        self.create_widgets()
        self.populate_quiz_tree()

    def create_widgets(self):
        left_frame = tk.Frame(self)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Use Treeview instead of Listbox
        self.quiz_tree = ttk.Treeview(left_frame)
        self.quiz_tree.heading('#0', text='Quizzes', anchor='w')
        self.quiz_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.quiz_tree.bind('<<TreeviewSelect>>', self.on_quiz_selected)

        self.start_button = tk.Button(self, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack(side=tk.BOTTOM)

    def populate_quiz_tree(self):
        if not os.path.exists(QUIZZES_DIR):
            os.makedirs(QUIZZES_DIR)
        self.quiz_tree.delete(*self.quiz_tree.get_children())
        self.insert_tree_items('', QUIZZES_DIR)

    def insert_tree_items(self, parent, path):
        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                node = self.quiz_tree.insert(parent, 'end', text=item, open=False)
                self.insert_tree_items(node, full_path)
            elif item.endswith('.qqz'):
                self.quiz_tree.insert(parent, 'end', text=item, values=(full_path,))

    def on_quiz_selected(self, event):
        selection = self.quiz_tree.selection()
        if selection:
            item = self.quiz_tree.item(selection[0])
            full_path = self.get_full_path(selection[0])
            if os.path.isfile(full_path) and full_path.endswith('.qqz'):
                self.selected_quiz = full_path

    def get_full_path(self, item_id):
        parts = []
        while item_id:
            item = self.quiz_tree.item(item_id)
            parts.insert(0, item['text'])
            item_id = self.quiz_tree.parent(item_id)
        return os.path.join(QUIZZES_DIR, *parts)

    def start_quiz(self):
        if hasattr(self, 'selected_quiz'):
            quiz_path = self.selected_quiz
            self.quiz_window = QuizWindow(self, quiz_path)
            self.quiz_window.grab_set()
        else:
            messagebox.showerror("Error", "Please select a quiz to start.")

class QuizWindow(tk.Toplevel):
    def __init__(self, parent, quiz_path):
        super().__init__(parent)
        self.parent = parent  # Reference to the parent window
        self.quiz_path = quiz_path
        self.current_question_index = 0
        self.selected_answer = tk.StringVar()
        self.user_answers = []  # List to store user's answers and correctness
        self.correct_answers_count = 0

        self.load_quiz()
        self.create_widgets()

    def load_quiz(self):
        self.quiz_tree = ET.parse(self.quiz_path)
        self.quiz_root = self.quiz_tree.getroot()
        self.questions = self.quiz_root.findall('question')

    def create_widgets(self):
        self.title("Quiz")
        self.geometry("800x600")

        self.question_label = tk.Label(self, text="", wraplength=600, justify="left")
        self.question_label.pack(pady=10)

        self.answer_frame = tk.Frame(self)
        self.answer_frame.pack()

        self.next_button = tk.Button(self, text="Next", command=self.next_question)
        self.next_button.pack(pady=10)

        self.display_question()

    def display_question(self):
        self.clear_answers()
        self.selected_answer.set(None)  # Reset selected answer

        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            question_text = question.get('prompt') if question.get('prompt') else ""
            self.question_label.config(text=f"Q{self.current_question_index + 1}: {question_text}")

            answers = question.findall('answer')
            for i, answer in enumerate(answers):
                answer_text = answer.text.strip() if answer.text else ""
                rb = tk.Radiobutton(
                    self.answer_frame,
                    text=answer_text,
                    variable=self.selected_answer,
                    value=str(i),
                    wraplength=600,
                    justify="left"
                )
                rb.pack(anchor=tk.W)
        else:
            self.finish_quiz()

    def clear_answers(self):
        for widget in self.answer_frame.winfo_children():
            widget.destroy()

    def next_question(self):
        selected_index = self.selected_answer.get()
        if selected_index == '' or selected_index is None:
            messagebox.showerror("Error", "Please select an answer before proceeding.")
            return

        selected_answer_index = int(selected_index)
        current_question = self.questions[self.current_question_index]
        answers = current_question.findall('answer')

        # Check if the selected answer is correct
        is_correct = False
        selected_answer_text = answers[selected_answer_index].text.strip() if answers[selected_answer_index].text else ""
        if 'correct' in answers[selected_answer_index].attrib and answers[selected_answer_index].get('correct') == "yes":
            self.correct_answers_count += 1
            is_correct = True

        # Get correct answer text
        correct_answer_text = self.get_correct_answer_text(answers)

        # Store user's selected answer and correctness
        self.user_answers.append({
            'question': current_question.get('prompt'),
            'selected_answer': selected_answer_text,
            'correct_answer': correct_answer_text,
            'is_correct': is_correct
        })

        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            self.finish_quiz()

    def get_correct_answer_text(self, answers):
        for answer in answers:
            if 'correct' in answer.attrib and answer.get('correct') == "yes":
                return answer.text.strip() if answer.text else ""
        return ""

    def finish_quiz(self):
        total_questions = len(self.questions)
        score_percentage = (self.correct_answers_count / total_questions) * 100

        # Create a new window to display detailed results
        result_window = tk.Toplevel(self.parent)
        result_window.title("Quiz Results")
        result_window.geometry("800x600")

        result_label = tk.Label(result_window, text=f"You got {self.correct_answers_count} out of {total_questions} right.\nScore: {score_percentage:.2f}%")
        result_label.pack(pady=10)

        # Create a scrollable text widget to display detailed results
        result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD)
        result_text.pack(fill=tk.BOTH, expand=True)

        # Build the detailed results
        for idx, answer_info in enumerate(self.user_answers):
            question_num = idx + 1
            question_text = answer_info['question']
            selected_answer = answer_info['selected_answer']
            correct_answer = answer_info['correct_answer']
            is_correct = answer_info['is_correct']

            result_text.insert(tk.END, f"Question {question_num}: {question_text}\n")
            result_text.insert(tk.END, f"Your Answer: {selected_answer}\n")
            if is_correct:
                result_text.insert(tk.END, "Result: Correct\n\n")
            else:
                result_text.insert(tk.END, f"Correct Answer: {correct_answer}\n")
                result_text.insert(tk.END, "Result: Incorrect\n\n")

        result_text.configure(state='disabled')  # Make the text read-only

        # Close the quiz window
        self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
