from app import db
from datetime import datetime, timedelta

"""
This table describes the relationship between a reaction and its recipients. It
is a many to many table.
"""

class ReactionDelivery(db.Model):

    # ID
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)

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

    def to_dict(self):
        data = {
            'recipient_uuid': self.recipient_uuid,
            'recipient_username': self.recipient.username,
            'is_delivered': self.is_delivered
        }

        return data
