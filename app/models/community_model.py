from app import db
from datetime import datetime, timedelta
import uuid

class Community(db.Model):

    # ID & UUID
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    uuid = db.Column(db.String(32), index=True, unique=True)

    # Community profile
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    chats = db.relationship("Chat", backref="community", lazy="dynamic")
    subscriptions = db.relationship("Subscription", back_populates="community")

    def to_dict(self):
        admins = []
        for subscription in self.subscriptions:
            if subscription.priveleges == 1:
                admins.append(subscription.subscriber.to_public_dict())
        data = {
            'uuid': self.uuid,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at,
            'subscribers': [subscription.subscriber.to_public_dict() for subscription in self.subscriptions],
            'admins': admins,
            'chats': [chat.to_dict() for chat in self.chats]
        }

        return data

    def from_dict(self, data):
        self.name = data['name']
        self.description = data['description']
        self.uuid = uuid.uuid4().hex
