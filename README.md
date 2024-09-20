# Towel-Quiz

Here's the quiz app:
<img width="1368" alt="Screen Shot 2024-09-20 at 4 22 02 PM" src="https://github.com/user-attachments/assets/00462569-7628-488f-907d-af43859e6ca5">

## Quiz Folder Structure
The pic below shows quiz location structure, and the .txt file will give more clarity.
<img width="292" alt="Screen Shot 2024-09-20 at 4 19 23 PM" src="https://github.com/user-attachments/assets/af9c01ef-e00f-404a-a676-5e4ab00a4652">

## Overview
Towel-Quiz is a desktop quiz application that allows users to create, take, and manage quizzes. It is built using Python and tkinter for a simple and user-friendly interface.

## Requirements
- Python 3.x
- tkinter (usually comes with Python)
- PyInstaller

## Installation
1. **Clone the repository or download the files:**
   Ensure you have the `quiz.py` file and the required resources in the `Towel-Quiz` folder.

2. **Install Python 3:**
   If not already installed, download and install Python 3 from [python.org](https://www.python.org/).

3. **Install PyInstaller:**
   Open a terminal or command prompt and install PyInstaller using pip:
   ```bash
   pip install pyinstaller
   ```

## Packaging the Application

### macOS:
1. **Navigate to your project directory:**
   ```bash
   cd path/to/Towel-Quiz
   ```

2. **Run PyInstaller with the following command:**
   ```bash
   pyinstaller --onefile --windowed --icon=/Users/username/Pictures/TowelQuiz/AppIcon.icns --name Towel-Quiz quiz.py
   ```
   Replace `/Users/username/Pictures/TowelQuiz/AppIcon.icns` with the actual path to your icon.

### Windows:
1. **Navigate to your project directory:**
   ```cmd
   cd C:\Users\username\Downloads\Towel-Quiz-main
   ```

2. **Run PyInstaller with the following command:**
   ```cmd
   pyinstaller --onefile --windowed --icon=towelquizico.ico --name Towel-Quiz quiz.py
   ```
   Make sure `towelquizico.ico` is in the directory where you're running the command.

### Building the Application:
- After running the above commands based on your operating system, find the executable named `Towel-Quiz` in the `dist` directory within your project folder.

## Running the Application
After packaging, run the application by double-clicking the `Towel-Quiz` executable found in the `dist` directory.
