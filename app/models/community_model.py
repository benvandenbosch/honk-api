from app import db
from datetime import datetime, timedelta


class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    chats = db.relationship("Chat", backref="community", lazy="dynamic")
    subscriptions = db.relationship("Subscription", back_populates="community")

    def to_dict(self):
        admins = []
        for subscription in self.subscriptions:
            if subscription.priveleges == 1:
                admins.append(subscription.user.username)
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'subscribers': [subscription.user.username for subscription in self.subscriptions],
            'admins': admins,
            'chats': [chat.name for chat in self.chats]
        }

        return data

    def from_dict(self, data):
        self.name = data['name']
        self.description = data['description']
