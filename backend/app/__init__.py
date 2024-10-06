from flask import Flask
from pymongo import MongoClient

def init_db():
    try:
        # Replace with your actual MongoDB password
        uri = "mongodb+srv://clinton3122003:hacksmu123@learningapp.31wtb.mongodb.net/?retryWrites=true&w=majority&appName=LearningApp"
        client = MongoClient(uri)
        db = client["LearningApp"]  # Replace with your actual database name
        print("Connected to MongoDB Atlas!")
        return db
    except Exception as e:
        return None
    


def create_app():
    app = Flask(__name__)
    
    # Initialize MongoDB
    app.db = init_db()
    app.config['SECRET_KEY'] = '4f931d030d562a0f6e1352225298cd59' #actually not recommended to hardcode key
    #recommended to use os.getenv('SECRET_KEY') (which is saving key in env instead of hardcoding)
    
    # Register blueprints
    from .api.auth import auth_bp  # Update to include the 'api' subdirectory
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app