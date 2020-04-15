from app import create_app, db
from app.models.user_model import User
from app.models.message_model import Message
"""
Start the application by importing honk from the app directory.
By importing the app package, the __init__ script is run, which
makes honk (the Flask app) availabe publicly
"""

# Create an instance of the application
app = create_app()

# Add database instance and models to flask shell session
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message}
