# Sample Data Structures (In-memory for now)
users = []
videos = []
quizzes = {}

# 1. Register User
def register_user(name, email, password):
    user = {
        "id": len(users) + 1,  # Simple ID generation
        "name": name,
        "email": email,
        "password": password,  # In production, hash the password
        "progress": {},  # Stores the score for quizzes
        "points": 0  # Points earned from completed quizzes
    }
    users.append(user)
    return user

# 2. Login User
def login_user(email, password):
    for user in users:
        if user['email'] == email and user['password'] == password:
            return user
    return None

# 3. Add Video (Admin Logic)
def add_video(title, description, url):
    video = {
        "id": len(videos) + 1,
        "title": title,
        "description": description,
        "url": url
    }
    videos.append(video)
    return video

# 4. Add Quiz for a Video (Admin Logic)
def add_quiz(video_id, questions, correct_answers):
    quiz = {
        "video_id": video_id,
        "questions": questions,
        "correct_answers": correct_answers  # Correct answers for scoring
    }
    quizzes[video_id] = quiz
    return quiz

# 5. Get Quiz for a Video
def get_quiz(video_id):
    return quizzes.get(video_id, None)

# 6. Submit Quiz and Calculate Score
def submit_quiz(user_id, video_id, user_answers):
    quiz = quizzes.get(video_id)
    if not quiz:
        return "Quiz not found"
    
    # Calculate score
    correct_answers = quiz['correct_answers']
    score = sum([1 for i in range(len(correct_answers)) if user_answers[i] == correct_answers[i]])

    # Update user progress
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        user['progress'][video_id] = score
        user['points'] += score  # Increase user's points
        return f"Quiz submitted successfully. Score: {score}"
    return "User not found"

# 7. Issue Certificate (Dummy Logic for now)
def issue_certificate(user_id, course_id):
    # Placeholder for certificate issuing logic
    return f"Certificate issued for user {user_id} on course {course_id}"

