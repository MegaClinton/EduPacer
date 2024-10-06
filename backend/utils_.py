import hashlib
import jwt
import datetime

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_points_to_users(db):
    users_collection = db["users"]
    # Update all users to add a new points field if it doesn't exist
    result = users_collection.update_many(
        {"points": {"$exists": False}},  # Only update users who don't have the points field
        {"$set": {"points": 0}}  # Set points to 0
    )
    return result

def generate_jwt(username, secretkey):
    payload = {
        'username': str(username),
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=10)  # Token expires in 10 hour
    }
    return jwt.encode(payload, secretkey, algorithm='HS256')

def validate_jwt_n_get_username(token, secret_key):
    try:
        # Decode the token and verify the signature and expiration
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        username = decoded_token.get('username')  # Extract the username or other data
        return username  # Return the username or relevant user data
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")