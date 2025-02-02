from app import create_app, db
from app.models.user_model import User
from app.models.message_model import Message
from app.models.chat_model import Chat
from app.models.community_model import Community
from app.models.subscription_model import Subscription
from app.models.membership_model import Membership
from app.models.reaction_model import Reaction
from app.models.message_delivery_model import MessageDelivery
from app.models.reaction_delivery_model import ReactionDelivery
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
    return {'db': db, 'User': User, 'Message': Message, 'Community':Community,
            'Chat': Chat, 'Subscription': Subscription, 'Membership': Membership,
            'Reaction': Reaction, 'MessageDelivery': MessageDelivery,
            'ReactionDelivery': ReactionDelivery}
