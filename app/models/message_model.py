from app import db
from datetime import datetime, timedelta


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String(140))
    user_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))

    def __repr__(self):
        return('<Message {}>'.format(self.content))

    def from_dict(self, data):
        self.content = data['content']

    def to_dict(self):
        data = {
            'id': self.id,
            'chat': self.chat.name,
            'author': self.author.username,
            'created_at': self.created_at,
            'content': self.content
        }

        return data
