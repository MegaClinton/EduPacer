from flask import Blueprint, jsonify, request, current_app
from pymongo.errors import DuplicateKeyError, ConnectionFailure

from utils_ import hash_password
auth_bp = Blueprint('auth', __name__)
# Helper function to serialize the user object
def serialize_user(user):
    # Create a new dictionary with serialized values
    serialized_user = {
        "id": str(user["_id"]),  # Convert ObjectId to string
        "username": user["username"],
        # Add other fields as necessary, but avoid sensitive data like password
    }
    return serialized_user

@auth_bp.route('/login', methods=['POST']) #as login info is sensitive
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "username and password fields are required"}), 400
    
    db = current_app.db
    user = db.users.find_one({"username": username})
    if not user:
        return jsonify({"error": "the user not exists"}), 401
    print(user)
    # Ensure the user has the salt key
    if "password" not in user:
        return jsonify({"error": "the password info not exists in DB"}), 404

    hashed_password = hash_password(password)  # Hash the provided password with the stored salt

    if hashed_password == user["password"]:
        serialized_user = serialize_user(user)  # Serialize the user object
        return jsonify({"message": "User logged in successfully" , "User": serialized_user}), 200
    else:
        return jsonify({"error": "Incorrect password"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "username and password fields are required"}), 400

    db = current_app.db
    # Check if the username already exists
    existing_user = db.users.find_one({"username": username})
    if existing_user:
        return jsonify({"error": "Username already exists"}), 409

    # Create a new data dictionary to hold the user info
    user_data = {
        "username": username,
        "password": hash_password(password)  # Store the password directly (not recommended without hashing)
    }

    try:
        # Attempt to insert the user data into the database
        result = db.users.insert_one(user_data)
        return jsonify({"message": "User registered successfully", "_id": str(result.inserted_id)}), 201
    except DuplicateKeyError:
        return jsonify({"error": "Username already exists"}), 400
    except ConnectionFailure:
        return jsonify({"error": "Database connection failed"}), 500
    except Exception as e:
        # Handle any other exceptions
        return jsonify({"error": str(e)}), 500