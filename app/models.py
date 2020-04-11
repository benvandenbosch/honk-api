from app import db
from datetime import datetime


"""
This file is where database models will be held. SQLAlchemy automatically performs
the translation from raw data in a table to an object based on the models in
this file. Each table should have a corresponding model in this file.
"""

# Argument "db.Model" is base for all data models in Flask-SQLAlchemy
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Message', backref='sender', lazy='dynamic')

    # Tell Python how to print objects of this class
    def __repr__(self):
        return('<User {}>'.format(self.username))


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return('<Message {}>'.format(self.content))
