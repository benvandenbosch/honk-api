from app import db
from datetime import datetime, timedelta
import uuid
from app.daos import chat_dao
from flask import g
from app.models.message_delivery_model import MessageDelivery

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
        self.uuid = uuid.uuid4().hex
        self.content = data['content']
        self.created_at = datetime.utcnow()
        self.chat = chat_dao.get_chat_by_uuid(data['chat_uuid'])
        self.author = g.current_user

        # Create message delivery objects for each recipient
        for membership in self.chat.memberships:
            member = membership.member
            # Default is_delivered should be false
            is_delivered = True if member == g.current_user else False
            delivery = MessageDelivery(
                recipient = member,
                message = self,
                is_delivered = is_delivered
            )
            self.deliveries.append(delivery)

    def to_dict(self):
        data = {
            'uuid': self.uuid,
            'chat': self.chat.name,
            'author': self.author.username,
            'author_uuid': self.author_uuid,
            'created_at': self.created_at,
            'content': self.content,
            'deliveries': [delivery.to_dict() for delivery in self.deliveries],
            'reactions': [reaction.to_dict() for reaction in self.reactions]
        }

        return data
