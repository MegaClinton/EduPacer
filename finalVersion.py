import tkinter as tk
from tkinter import messagebox
import hashlib
import webbrowser
from pymongo import MongoClient

def init_db():
    # Initializes the MongoDB database connection

    # Returns:
        # MongoClient: The connected MongoClient instance
    try:
        uri = "mongodb+srv://clinton3122003:hacksmu123@learningapp.31wtb.mongodb.net/?retryWrites=true&w=majority&appName=LearningApp"
        client = MongoClient(uri)
        db = client["LearningApp"]
        print("Connected to MongoDB Atlas!")
        return db
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to MongoDB: {e}")
        return None


# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function for logging in users
def login(db, username, password):
    users_collection = db["users"]
    hashed_password = hash_password(password)
    user = users_collection.find_one({"username": username, "password": hashed_password})
    return user

# Function for registering new users
def register(db, username, password):
    users_collection = db["users"]
    hashed_password = hash_password(password)
    
    # Check if the username already exists
    existing_user = users_collection.find_one({"username": username})
    
    if existing_user:
        messagebox.showwarning("Registration", "Username already exists. Please choose a different username.")
        return

    try:
        # Insert new user document with points initialized to 0
        users_collection.insert_one({
            "username": username,
            "password": hashed_password,
            "points": 0  # Initialize points to 0
        })
        messagebox.showinfo("Registration", "Registration successful!")
    except Exception as e:
        messagebox.showwarning("Registration", f"Error: {e}")

def add_points_to_users(db):
    users_collection = db["users"]
    # Update all users to add a new points field if it doesn't exist
    result = users_collection.update_many(
        {"points": {"$exists": False}},  # Only update users who don't have the points field
        {"$set": {"points": 0}}  # Set points to 0
    )
    print(f"Modified {result.modified_count} documents.")

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
            if db["users"].find_one({"username": username}):
                messagebox.showwarning("Login", "Incorrect username or password")
            else:  
                messagebox.showwarning("Login", "You must be registered to login.")

    def try_register():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            register(db, username, password)
            # Call login again to allow the user to log in after registration
            login_window.destroy()
            user_login(db)
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
        show_video_choice(subject, username)  # Pass username to the next function

    for subject in subjects:
        tk.Button(menu_window, text=subject, command=lambda s=subject: pick_subject(s)).pack()

# Function to show video choice
def show_video_choice(subject, username):
    choice_window = tk.Toplevel(root)
    choice_window.title(f"{subject} Video Choice")

    video_details = {
        "Math": ("Math Basics - Adding and Subtracting", "https://www.youtube.com/watch?v=7J1OkxuyLD0&pp=ygUkYmFzaWMgbWF0aCBhZGRpdGlvbiBhbmQgc3VidHJhY3Rpb24g"),
        "Science": ("Science 101 - Basic Chemistry", "https://www.youtube.com/watch?v=k3rRrl9J2F4&pp=ygUVc2NpZW5jZSAxMDEgY2hlbWlzdHJ5"),
        "Programming": ("Intro to Programming - Python Basics", "https://www.youtube.com/watch?v=I-k-iTUMQAY")
    }

    video_title, video_url = video_details[subject]

    tk.Label(choice_window, text=f"Video Title: {video_title}").pack()
    
    def watch_video():
        webbrowser.open(video_url)
        choice_window.destroy()
        ask_questions(subject, username)  # Pass username to the questions function

    tk.Button(choice_window, text="Watch Video", command=watch_video).pack()
    tk.Button(choice_window, text="Answer Questions", command=lambda: (choice_window.destroy(), ask_questions(subject, username))).pack()

# Function to ask questions
def ask_questions(subject, username):
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

    correct_answers = 0  # Track correct answers
    
    def submit_answer(correct_answer, user_answer):
        nonlocal correct_answers  # Use nonlocal to modify outer scope variable
        if user_answer == correct_answer:
            correct_answers += 1
        tk.Label(question_window, text=f"You answered: {user_answer}. Correct answer was: {correct_answer}").pack()

    def finish_quiz(username):
        points_earned = assign_points(correct_answers)
        # Update points in the database
        users_collection = db["users"]
        users_collection.update_one({"username": username}, {"$inc": {"points": points_earned}})
        messagebox.showinfo("Quiz Complete", f"You earned {points_earned} points.")
        question_window.destroy()

    for q in questions[subject]:
        tk.Label(question_window, text=q["question"]).pack()
        selected_answer = tk.StringVar(value=0)  # Initialize to None for each question

        # Create radiobuttons for the current question
        for option in q["options"]:
            rb = tk.Radiobutton(question_window, text=option, variable=selected_answer, value=option)
            rb.pack(anchor='w')

        tk.Button(question_window, text="Submit Answer", 
                  command=lambda correct_answer=q["answer"], var=selected_answer: submit_answer(correct_answer, var.get())).pack()

    tk.Button(question_window, text="Finish Quiz", command=lambda: finish_quiz(username)).pack()

# Function to assign points based on correct answers
def assign_points(correct_answers):
    points_per_answer = 10
    return correct_answers * points_per_answer

# Initialize the database
db = init_db()

# Create the root window but do not call mainloop yet
root = tk.Tk()
root.withdraw()  # Hide the root window initially

# Start the login process only if the database connection was successful
if db is not None:
    add_points_to_users(db)  # This will add a points field to all users without it
    user_login(db)
    
# Run the app
root.mainloop()
