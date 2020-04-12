from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import base64, os

"""
This file is where database models will be held. SQLAlchemy automatically performs
the translation from raw data in a table to an object based on the models in
this file. Each table should have a corresponding model below.
"""

######################
# Association Tables #
######################

# Association between chat and the users that are members of it
memberships = db.Table(
    'memberships',
    db.Column('member_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
)

######################
# Classes            *
######################
# Each class represents a table in the database
# Argument "db.Model" is base for all data models in Flask-SQLAlchemy


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Message', backref='sender', lazy='dynamic')
    token = db.Column(db.String(32), index=True, unique = True)
    token_expiration = db.Column(db.DateTime)
    chats = db.relationship(
        'Chat', secondary=memberships, backref='members', lazy='dynamic'
    )

    # Tell Python how to print objects of this class
    def __repr__(self):
        return('<User {}>'.format(self.username))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Issue a token to the user for API authentication
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    def is_member(self, chat):
        return self.chats.filter(memberships.c.chat_id == chat.id).count() > 0

    def join_chat(self, chat):
        if not self.is_member(chat):
            self.chats.append(chat)

    @staticmethod # (Belongs to class rather than specific instance)
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    # Represent as a JSON object
    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

        return data

    # Convert from JSON object to Python object
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)

    def from_dict(self, data):
        self.name = data['name']
        self.created_at = datetime.utcnow()

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name
            }

        return data

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return('<Message {}>'.format(self.content))
