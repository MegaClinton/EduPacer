from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
import hashlib
import webbrowser

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key
app.config["MONGO_URI"] = "mongodb+srv://clinton3122003:hacksmu123@learningapp.31wtb.mongodb.net/LearningApp?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hash_password(password)
    
    user = mongo.db.users.find_one({"username": username, "password": hashed_password})
    
    if user:
        session['username'] = username
        return redirect(url_for('menu'))
    else:
        flash("Incorrect username or password", "danger")
        return redirect(url_for('home'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hash_password(password)

    try:
        mongo.db.users.insert_one({"username": username, "password": hashed_password})
        flash("Registration successful!", "success")
    except Exception as e:
        flash("Username already exists! Please choose a different username.", "danger")
    return redirect(url_for('home'))

@app.route('/menu')
def menu():
    return render_template('menu.html', username=session['username'])

@app.route('/video_choice/<subject>')
def video_choice(subject):
    video_details = {
        "Math": ("Math Basics - Adding and Subtracting", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        "Science": ("Science 101 - Basic Chemistry", "https://www.youtube.com/watch?v=abcd1234"),
        "Programming": ("Intro to Programming - Python Basics", "https://www.youtube.com/watch?v=xyz5678")
    }
    
    video_title, video_url = video_details[subject]
    
    return render_template('video_choice.html', video_title=video_title, video_url=video_url, subject=subject)

@app.route('/questions/<subject>', methods=['GET', 'POST'])
def questions(subject):
    questions_data = {
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
    
    if request.method == 'POST':
        user_answers = request.form.to_dict()
        return render_template('questions.html', subject=subject, questions=questions_data[subject], user_answers=user_answers)

    return render_template('questions.html', subject=subject, questions=questions_data[subject])

if __name__ == '__main__':
    app.run(debug=True)
