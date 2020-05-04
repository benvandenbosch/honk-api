from app import db
from datetime import datetime, timedelta
from flask import g
import uuid
from app.models.message_model import Message
from app.models.reaction_delivery_model import ReactionDelivery

"""
This table describes a reaction.
"""

class Reaction(db.Model):

    # ID and UUID within Reaction table
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    uuid = db.Column(db.String(32), index=True, unique=True)

    # Foreign keys and foreign uuids with Message & User tables
    reactor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    reactor_uuid = db.Column(db.String(32))
    message_uuid = db.Column(db.String(32))

    # Record the type of reaction
    reaction_type = db.Column(db.String(20), default="like")

    # Relationship with reaction deliveries
    deliveries = db.relationship('ReactionDelivery', back_populates='reaction', lazy='dynamic')

    def __repr__(self):
        return('<Reaction {}>'.format(self.content))

    def from_dict(self, data):
        message = Message.query.filter_by(uuid=data['message_uuid']).first()
        self.uuid = uuid.uuid4().hex
        self.reaction_type = data['reaction_type']
        self.reactor = g.current_user
        self.message = message
        self.reactor_uuid = g.current_user.uuid
        self.message_uuid = message.uuid

        # Create a reaction delivery object for each recipient
        for membership in self.message.chat.memberships:
            member = membership.member
            is_delivered = True if member == g.current_user else False
            delivery = ReactionDelivery(
                recipient = member,
                reaction = self,
                is_delivered = is_delivered,
                recipient_uuid = member.uuid,
                reaction_uuid = self.uuid,
                uuid = uuid.uuid4().hex
            )
            self.deliveries.append(delivery)

    def to_dict(self):
        data = {
            'uuid': self.uuid,
            'reactor': self.reactor.to_public_dict(),
            'reaction_type': self.reaction_type,
            'deliveries': [delivery.to_dict() for delivery in self.deliveries]
        }

        return data
