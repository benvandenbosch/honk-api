from app import db
from datetime import datetime, timedelta

"""
This table describes the relationship between a message and its recipients. It
is a many to many table.
"""

class MessageDelivery(db.Model):

    # ID & UUID
    id = db.Column(db.Integer, primary_key=True, unique=True, index=True)
    uuid = db.Column(db.String(32), unique=True, index=True)

    # Foreign keys with User and Message tables
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    recipient_uuid = db.Column(db.String(32))
    message_uuid = db.Column(db.String(32))

    # Track whether the message has been successfully delivered
    is_delivered = db.Column(db.Boolean, default=False)

    # Relationship with user
    recipient = db.relationship("User", back_populates="message_deliveries")

    # Relationship with message
    message = db.relationship("Message", back_populates="deliveries")

    def __repr__(self):
        return('<MessageDelivery {}>'.format(self.content))

    def to_dict(self):
        data = {
            'is_delivered': self.is_delivered,
            'uuid': self.uuid,
            'recipient': self.recipient.to_public_dict()
        }

        return data
