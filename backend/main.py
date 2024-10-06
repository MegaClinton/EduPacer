from app import create_app

# Create a Flask application instance
app = create_app()

if __name__ == '__main__':
    # Run the app with debug enabled
    init_db()

    app.run(host='0.0.0.0', port=5000, debug=True)
