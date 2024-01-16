# QuizMakerApp README

## Overview
The `QuizMakerApp` is a Python-based GUI application designed for creating and editing quizzes. Utilizing the `tkinter` library for the graphical user interface and `xml.etree.ElementTree` for XML file handling, this application offers a straightforward yet functional interface for managing quiz content.

## Class: QuizMakerApp

### Functions

#### 1. `__init__`
- **Purpose:** Initializes the main application window.
- **Details:** 
  - Sets the window title and size.
  - Calls `create_widgets` and `populate_quiz_list` for UI setup and quiz list population.

#### 2. `create_widgets`
- **Purpose:** Creates and arranges widgets in the main application window.
- **Widgets:**
  - `self.quiz_listbox`: Displays quizzes.
  - `self.add_quiz_button`: Triggers the creation of a new quiz.
- **Event Binding:** Binds the listbox selection to the `on_quiz_selected` function.

#### 3. `populate_quiz_list`
- **Purpose:** Populates the listbox with quiz files.
- **Functionality:** Checks and creates the `QUIZZES_DIR` directory, then populates it with `.qqz` quiz files.

#### 4. `on_quiz_selected`
- **Purpose:** Handles quiz selection from the listbox.
- **Functionality:** Retrieves and passes the selected quiz file to `edit_quiz`.

#### 5. `create_quiz`
- **Purpose:** Manages the creation of a new quiz.
- **Functionality:** Prompts for a quiz name, checks for existing quizzes, and creates a new XML file if unique.

#### 6. `edit_quiz`
- **Purpose:** Opens the quiz editor for the selected quiz.
- **Functionality:** Creates an instance of `QuizEditor` with the selected quiz file.

## Class: QuizEditor



### Functions

#### 1. `__init__`
- **Purpose:** Initializes the quiz editor window.
- **Functionality:** Stores the quiz path and sets up the UI and quiz loading through `create_widgets` and `load_quiz`.

#### 2. `create_widgets`
- **Purpose:** Creates and arranges widgets in the quiz editor window.
- **Widgets:**
  - `self.question_listbox`: Displays quiz questions.
  - `self.add_question_button`: Adds new questions.
  - `self.edit_area`: A frame for question editing options.
- **Event Binding:** Binds the question listbox selection to `on_question_selected`.

#### 3. `load_quiz`
- **Purpose:** Loads the quiz from the specified XML file.
- **Functionality:** Calls `populate_question_list` to display questions in the listbox.

#### 4. `populate_question_list`
- **Purpose:** Populates the listbox with questions from the quiz XML.
- **Functionality:** Clears and repopulates the question listbox.

#### 5. `on_question_selected`
- **Purpose:** Handles question selection from the listbox.
- **Functionality:** Sets `selected_question` and displays editing options with `display_question_editor`.

#### 6. `add_question`
- **Purpose:** Adds a new question to the quiz.
- **Functionality:** Prompts the user for the question text and updates the quiz XML.

#### 7. `display_question_editor`
- **Purpose:** Sets up the editing area for a selected question.
- **Functionality:** Allows editing of the question prompt and answers, including options to add and save changes.

#### 8. `add_answer_editor`
- **Purpose:** Adds an editor for an answer in the quiz.
- **Functionality:** Includes a text entry for the answer and a checkbox for correctness. Populates with existing data if provided.

#### 9. `add_new_answer_editor`
- **Purpose:** Adds a new answer editor.
- **Functionality:** Triggered by "Add Answer" button; checks for question selection before addition.

#### 10. `delete_answer`
- **Purpose:** Deletes an answer from the quiz.
- **

Functionality:** Removes the selected answer both from the XML file and the UI, triggered by the "Delete" button in each answer editor.

#### 11. `save_question`
- **Purpose:** Saves the edits made to the current question.
- **Functionality:** Updates the question prompt and answers in the XML. Shows an error message if the question text is empty.

#### 12. `save_quiz`
- **Purpose:** Writes the updated quiz content back to the file.
- **Functionality:** Refreshes the question list in the listbox to reflect changes.

## Main Execution Block

- **Execution:** When the script is run as the main program (`if __name__ == "__main__":`), it:
  - Creates an instance of `QuizMakerApp`.
  - Starts the application's main loop, making the UI interactive.

## Application Design

Each function in `QuizMakerApp` and `QuizEditor` is meticulously designed to handle specific aspects of the application, from creating and positioning UI elements to managing data operations. The effective use of the `tkinter` library for GUI components and `xml.etree.ElementTree` for XML file handling makes this application a prime example of a simple yet functional GUI application in Python. The structured and modular approach enhances maintainability and scalability.
