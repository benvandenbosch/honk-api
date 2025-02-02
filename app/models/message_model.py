from app import db
from datetime import datetime, timedelta
import uuid
from app.daos import chat_dao
from flask import g
from app.models.message_delivery_model import MessageDelivery

class Message(db.Model):

    # ID & UUID
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    uuid = db.Column(db.String(32), index=True, unique=True)

    # Foreign keys and uuids for User & Chat tables
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    author_uuid  = db.Column(db.String(32))
    chat_uuid = db.Column(db.String(32))

    # Message attributes
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String(400))

    # Relationships
    deliveries = db.relationship('MessageDelivery', back_populates='message', lazy='dynamic')
    reactions = db.relationship('Reaction', backref='message', lazy='dynamic')


    def __repr__(self):
        return('<Message {}>'.format(self.content))


    def from_dict(self, data):
        self.content = data['content']
        self.created_at = datetime.utcnow()
        self.chat = chat_dao.get_chat_by_uuid(data['chat_uuid'])
        self.author = g.current_user
        if not self.uuid:
            self.uuid = uuid.uuid4().hex



    def to_dict(self, terminating=False):
        data = {
            'uuid': self.uuid,
            'author': self.author.to_dict(),
            'created_at': str(self.created_at),
            'content': self.content,

        }

        # If relationships should be returned, Do The Right Thing
        if not terminating:
            data.update({
                'deliveries': [delivery.to_dict() for delivery in self.deliveries],
                'reactions': [reaction.to_dict() for reaction in self.reactions]
            })

        return data
