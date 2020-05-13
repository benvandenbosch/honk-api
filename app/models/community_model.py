from app import db
from datetime import datetime, timedelta
import uuid
from app.daos import chat_dao
from flask import g

class Community(db.Model):

    # ID & UUID
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    uuid = db.Column(db.String(32), index=True, unique=True)

    # Community profile
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    chats = db.relationship("Chat", backref="community", lazy="dynamic")
    subscriptions = db.relationship("Subscription", back_populates="community")

    def to_dict(self, terminating=False):
        admins = []
        for subscription in self.subscriptions:
            if subscription.priveleges == 1:
                admins.append(subscription.subscriber.to_dict())

        # Only return chats a user is allowed to see
        chats = chat_dao.get_by_user_and_community(user=g.current_user, community=self)

        data = {
            'uuid': self.uuid,
            'name': self.name,
            'about': self.description,
            'created_at': str(self.created_at),
            'subscribers': [subscription.subscriber.to_dict() for subscription in self.subscriptions],
            'chats': [chat.to_dict(terminating=True) for chat in chats]
        }

        if not terminating:
            data.update({
                'chats': [chat.to_dict() for chat in chats]
            })

        return data

    def from_dict(self, data):
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])
        self.last_updated = datetime.utcnow()
        if not self.uuid:
            self.uuid = uuid.uuid4().hex
