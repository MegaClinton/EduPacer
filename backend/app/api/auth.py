from flask import Blueprint, jsonify, request, current_app

users_bp = Blueprint('auth', __name__)

@users_bp.route('/login', methods=['POST']) #as login info is sensitive
def get_users():
    users = list(current_app.db.users.find())  # Fetch all users
    return jsonify(users)

@users_bp.route('/register', methods=['POST'])
def create_user():
    data = request.json
    result = current_app.db.users.insert_one(data)  # Insert new user
    return jsonify({"_id": str(result.inserted_id)}), 201
