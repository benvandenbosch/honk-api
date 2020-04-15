from app import db
from datetime import datetime, timedelta
from daos import user_dao, chat_dao


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id  = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer, db.ForeinKey('chat.id'))

    def from_dict(self, data):
        self.content = data['content']
        author_id = user_dao.get_user_by_id(data['sender']).id
        chat_id = chat_dao.get_chat_by_id(data['chat']).id


    def __repr__(self):
        return('<Message {}>'.format(self.content))
