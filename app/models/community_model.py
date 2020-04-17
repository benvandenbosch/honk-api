from app import db
from datetime import datetime, timedelta


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Many to many relationship with user (Subscription as association object)
    subscribers = db.relationship("Subscription", backref="community", lazy='dynamic')

    # One to many relationship with chats
    chats = db.relationship("Chat", backref='community', lazy='dynamic')


    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'subscribers': [subscriber.username for subscriber in subscribers]
        }

    def from_dict(self, data):
        name = data['name']
        description = data['description']
