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
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), unique = True)
    token_expiration = db.Column(db.DateTime)
    apns = db.Column(db.String(200))

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
        return self.chats.filter(memberships.c.chat_id==chat.id).count() > 0

    def join_chat(self, chat):
        if not self.is_member(chat):
            self.chats.append(chat)

    def is_subscribed(self, community):
        return self.subscriptions.filter_by(community_id=community.id, is_active=1).count() > 0

    def update(self, data):
        for field in ['email', 'apns']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod # (Belongs to class rather than specific instance)
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    # Represent as a JSON object
    def to_dict(self):
        data = {
            'uuid': self.uuid,
            'username': self.username,
            'email': self.email,
            'apns': self.apns
        }

        return data

    # Convert from JSON object to Python object
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])
        if 'apns' in data:
            self.apns = data['apns']
