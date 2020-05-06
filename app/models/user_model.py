from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import base64, os
import uuid

######################
# Classes            *
######################
# Each class represents a table in the database
# Argument "db.Model" is base for all data models in Flask-SQLAlchemy


class User(UserMixin, db.Model):

    # Id & UUID
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    uuid = db.Column(db.String(32), index=True, unique=True, default=uuid.uuid4().hex)

    # User profile
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    display_name = db.Column(db.String(64))
    biography = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Authentication
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), unique = True)
    token_expiration = db.Column(db.DateTime)

    # User Notification
    apns = db.Column(db.String(200))

    # Relationships
    memberships = db.relationship('Membership', back_populates='member', lazy='dynamic')
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    subscriptions = db.relationship('Subscription', back_populates="subscriber", lazy='dynamic')
    message_deliveries = db.relationship('MessageDelivery', back_populates='recipient', lazy='dynamic')
    reaction_deliveries = db.relationship('ReactionDelivery', back_populates='recipient', lazy='dynamic')
    reactions = db.relationship('Reaction', backref='reactor', lazy='dynamic')


    # Tell Python how to print objects of this class
    def __repr__(self):
        return('<User {}>'.format(self.username))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Issue a token to the user for API authentication
    def get_token(self, expires_in=168):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(hours=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(hours=1)

    def is_member(self, chat):
        return self.memberships.filter_by(chat_uuid=chat.uuid).count() > 0

    def is_recipient(self, message):
        return self.message_deliveries.filter_by(message_uuid=message.uuid).count() > 0

    def join_chat(self, chat):
        if not self.is_member(chat):
            self.chats.append(chat)

    def is_subscribed(self, community):
        return self.subscriptions.filter_by(community_uuid=community.uuid, is_active=True).count() > 0

    def update(self, data):
        for field in ['apns', 'display_name', 'biography']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod # (Belongs to class rather than specific instance)
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    # Represent as a JSON object with child relationships
    def to_dict(self):
        data = {
            'uuid': self.uuid,
            'username': self.username,
            'email': self.email,
            'display_name': self.display_name,
            'biography': self.biography,
            'created_at': self.created_at,
            'communities': [subscription.community.uuid for subscription in self.subscriptions],
            'chats': [membership.chat.to_dict() for membership in self.memberships],
            'apns': self.apns
        }

        return data

    # Represent as a JSON object without child relationships
    def to_summary_dict(self):
        data = {
            'uuid': self.uuid,
            'username': self.username,
            'email': self.email,
            'display_name': self.display_name,
            'biography': self.biography,
            'created_at': self.created_at,
        }

        return data

    # Return a dictionary of info that other users can see
    def to_public_dict(self):
        data = {
            'uuid': str(self.uuid),
            'username': str(self.username),
            'display_name': str(self.display_name),
            'biography': str(self.biography),
            'created_at': str(self.created_at)
        }
        return data

    # Convert from JSON object to Python object
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'display_name', 'biography', 'apns']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
        self.uuid = uuid.uuid4().hex
