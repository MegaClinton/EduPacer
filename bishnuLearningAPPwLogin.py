import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import webbrowser

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Database to store user login and progress
def init_db():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function for logging in users
def login(username, password):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

# Function for registering new users
def register(username, password):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showwarning("Registration", "Username already exists.")
    finally:
        conn.close()

# Prompt for user login or registration
def user_login():
    login_window = tk.Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="Username").grid(row=0)
    tk.Label(login_window, text="Password").grid(row=1)

    username_entry = tk.Entry(login_window)
    password_entry = tk.Entry(login_window, show="*")
    username_entry.grid(row=0, column=1)
    password_entry.grid(row=1, column=1)

    def try_login():
        username = username_entry.get()
        password = password_entry.get()
        user = login(username, password)
        if user:
            messagebox.showinfo("Login", "Login successful!")
            login_window.destroy()
            show_menu(username)
        else:
            messagebox.showwarning("Login", "Incorrect username or password")

    def try_register():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            register(username, password)
            messagebox.showinfo("Register", "Registration successful!")
            login_window.destroy()
            show_menu(username)
        else:
            messagebox.showwarning("Register", "Please enter a username and password")

    tk.Button(login_window, text="Login", command=try_login).grid(row=2, column=0)
    tk.Button(login_window, text="Register", command=try_register).grid(row=2, column=1)

# Function to display the menu
def show_menu(username):
    menu_window = tk.Toplevel(root)
    menu_window.title("Pick a Subject")
    
    subjects = ["Math", "Science", "Programming"]
    
    tk.Label(menu_window, text=f"Welcome, {username}! Pick a subject:").pack()
    
    def pick_subject(subject):
        menu_window.destroy()
        show_video(subject)

    for subject in subjects:
        tk.Button(menu_window, text=subject, command=lambda s=subject: pick_subject(s)).pack()

# Function to display the video
def show_video(subject):
    video_url = {
        "Math": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Example links
        "Science": "https://www.youtube.com/watch?v=abcd1234",  
        "Programming": "https://www.youtube.com/watch?v=xyz5678"
    }[subject]
    
    # Open the video in the default web browser
    webbrowser.open(video_url)
    
    # After the video, prompt multiple-choice questions
    ask_questions(subject)

# Function to ask questions
def ask_questions(subject):
    question_window = tk.Toplevel(root)
    question_window.title(f"{subject} Questions")

    tk.Label(question_window, text="Answer the following questions:").pack()

    questions = {
        "Math": [
            {"question": "What is 2+2?", "options": ["3", "4", "5"], "answer": "4"},
            {"question": "What is the square root of 16?", "options": ["2", "3", "4"], "answer": "4"}
        ],
        "Science": [
            {"question": "What is the chemical symbol for water?", "options": ["H2O", "CO2", "O2"], "answer": "H2O"},
            {"question": "What planet is closest to the Sun?", "options": ["Earth", "Mars", "Mercury"], "answer": "Mercury"}
        ],
        "Programming": [
            {"question": "What is a variable?", "options": ["A storage location", "A function", "A loop"], "answer": "A storage location"},
            {"question": "What does HTML stand for?", "options": ["HyperText Markup Language", "HighText Machine Language", "HyperText Machine Language"], "answer": "HyperText Markup Language"}
        ]
    }

    user_answers = []
    
    for q in questions[subject]:
        tk.Label(question_window, text=q["question"]).pack()
        selected_answer = tk.StringVar()

        for option in q["options"]:
            rb = tk.Radiobutton(question_window, text=option, variable=selected_answer, value=option)
            rb.pack(anchor='w')

        # Button to submit the answer for this question
        tk.Button(question_window, text="Submit Answer", command=lambda: submit_answer(q["answer"], selected_answer.get())).pack()

    def submit_answer(correct_answer, user_answer):
        user_answers.append(user_answer)
        tk.Label(question_window, text=f"You answered: {user_answer}. Correct answer was: {correct_answer}").pack()

    tk.Button(question_window, text="Finish", command=question_window.destroy).pack()

# Root window for the app
root = tk.Tk()
root.title("Learning Tool")
root.geometry("300x200")

# Initialize the database
init_db()

# Start the login process
user_login()

# Run the app
root.mainloop()
