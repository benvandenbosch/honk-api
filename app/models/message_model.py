from app import db
from datetime import datetime, timedelta
import uuid

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), index=True, unique=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String(140))
    user_uuid  = db.Column(db.Integer, db.ForeignKey('user.uuid'))
    chat_uuid = db.Column(db.Integer, db.ForeignKey('chat.uuid'))

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
