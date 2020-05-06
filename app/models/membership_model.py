from app import db
from datetime import datetime, timedelta

"""
This table describes the relationship between a user and a chat (called a "Membership").
It is a many to many relationship
"""

class Membership(db.Model):

    # ID
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)

    # Foreign keys and uuids for User and Chat tables
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    user_uuid = db.Column(db.String(32))
    chat_uuid = db.Column(db.String(32))

    # Track validity timeframes of this Membership
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deactivated_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Track who added the person to the chat (username)
    inviter = db.Column(db.String(64))

    # Relationships with User & Chat models
    member = db.relationship('User', back_populates='memberships')
    chat = db.relationship('Chat', back_populates='memberships')
