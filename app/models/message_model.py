from app import db
from datetime import datetime, timedelta
import uuid

class Message(db.Model):

    # ID & UUID
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), index=True, unique=True)

    # Foreign keys for User & Chat tables
    author_uuid  = db.Column(db.String(32), db.ForeignKey('user.uuid'))
    chat_uuid = db.Column(db.String(32), db.ForeignKey('chat.uuid'))

    # Message attributes
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String(140))

    # Relationships
    deliveries = db.relationship('MessageDelivery', back_populates='message', lazy='dynamic')
    reactions = db.relationship('Reaction', backref='message', lazy='dynamic')

    
    def __repr__(self):
        return('<Message {}>'.format(self.content))

    def from_dict(self, data):
        self.content = data['content']

    def to_dict(self):
        data = {
            'uuid': self.uuid,
            'chat': self.chat.name,
            'author': self.author.username,
            'created_at': self.created_at,
            'content': self.content
        }

        return data
