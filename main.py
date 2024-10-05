import tkinter as tk
from tkinter import messagebox
import hashlib
import webbrowser
from pymongo import MongoClient

# Function to initialize the MongoDB database
def init_db():
    try:
        # Replace with your actual MongoDB password
        uri = "mongodb+srv://clinton3122003:hacksmu123@learningapp.31wtb.mongodb.net/?retryWrites=true&w=majority&appName=LearningApp"
        client = MongoClient(uri)
        db = client["LearningApp"]  # Replace with your actual database name
        print("Connected to MongoDB Atlas!")
        return db
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to MongoDB: {e}")
        return None


# Function to hash passwords
def hash_password(password):
    if salt is None:
        salt = os.urandom(16)  # Generate a new salt if not provided
    salted_password = salt + password.encode()  # Add salt to the password
    hashed_password = hashlib.sha256(salted_password).hexdigest()  # Hash the salted password
    return hashed_password, salt

# Function for logging in users
def login(db, username, password):
    users_collection = db["users"]
    hashed_password = hash_password(password)
    user = users_collection.find_one({"username": username, "password": hashed_password})
    if user:
        salt = user["salt"]  # Get the stored salt from the database
        hashed_password, _ = hash_password(password, salt)  # Hash the provided password with the stored salt
        if hashed_password == user["password"]:
            return user
    return None

# Function for registering new users
def register(db, username, password):
    users_collection = db["users"]
    if users_collection.find_one({"username": username}):
        messagebox.showwarning("Registration", "Username already exists!")
        return
    hashed_password, salt = hash_password(password)  # Hash password with a new salt
    try:
        # Insert new user document with salt and hashed password
        users_collection.insert_one({"username": username, "password": hashed_password, "salt": salt})
        messagebox.showinfo("Registration", "Registration successful!")
    except Exception as e:
        messagebox.showwarning("Registration", f"Error: {e}")

# Prompt for user login or registration
def user_login(db):
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
        user = login(db, username, password)
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
            register(db, username, password)
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
db = init_db()

# Start the login process
if db is not None:
    user_login(db)

# Run the app
root.mainloop()
