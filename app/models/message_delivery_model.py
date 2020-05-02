from app import db
from datetime import datetime, timedelta

"""
This table describes the relationship between a message and its recipients. It
is a many to many table.
"""

class MessageDelivery(db.Model):

    # Foreign keys with User and Message tables
    recipient_uuid = db.Column(db.String(32), db.ForeignKey('user.uuid'), primary_key=True)
    message_uuid = db.Column(db.String(32), db.ForeignKey('message.uuid'), primary_key=True)

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
            'recipient_uuid': self.recipient_uuid,
            'recipient_username': self.recipient.username,
            'is_delivered': self.is_delivered,
        }

        return data
