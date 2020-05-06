from app import db
from datetime import datetime, timedelta
import uuid

"""
This table describes the relationship between a reaction and its recipients. It
is a many to many table.
"""

class ReactionDelivery(db.Model):

    # ID
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    uuid = db.Column(db.String(32), unique=True, index=True, default=uuid.uuid4().hex)

    # Foreign keys and uuids with User and Reaction tables
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reaction_id = db.Column(db.Integer, db.ForeignKey('reaction.id'))
    recipient_uuid = db.Column(db.String(32))
    reaction_uuid = db.Column(db.String(32))

    # Track whether reaction has been successfully delivered
    is_delivered = db.Column(db.Boolean, default=False)

    # Relationship with user
    recipient = db.relationship("User", back_populates="reaction_deliveries")

    # Relationship with reaction
    reaction = db.relationship("Reaction", back_populates="deliveries")

    def __repr__(self):
        return('<ReactionDelivery {}>'.format(self.content))

    def to_dict(self, terminating=False):
        data = {
            'is_delivered': self.is_delivered,
            'uuid': self.uuid
        }

        if not terminating:
            data.update({
                'recipient': self.recipient.to_dict()
            })

        return data
