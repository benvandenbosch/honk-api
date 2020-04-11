from app import honk, db
from app.models import User, Message
"""
Start the application by importing honk from the app directory.
By importing the app package, the __init__ script is run, which
makes honk (the Flask app) availabe publicly
"""

# Add database instance and models to flask shell session
@honk.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message}
