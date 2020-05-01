from app import db
from datetime import datetime, timedelta

"""
This table describes the relationship between a message and its recipients. It
is a many to many table.
"""

class MessageDelivery(db.Model):

    # Foregin keys with User and Message tables
    recipient_uuid = db.Column(db.String(32), db.ForeignKey('user.uuid'), primary_key=True)
    message_uuid = db.Column(db.String(32), db.ForeignKey('message.uuid'), primary_key=True)

    # Track whether the message has been successfully delivered
    is_delivered = db.Column(db.Boolean, default=False)

    # Relationship with user
    recipient = db.relationship("User", back_populates="message_deliveries")

    # Relationship with message
    message = db.relationship("Message", back_populates="deliveries")
