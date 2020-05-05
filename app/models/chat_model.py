from app import db
from datetime import datetime, timedelta
import uuid


class Chat(db.Model):

    # ID & UUID
    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    uuid = db.Column(db.String(32), index=True, unique=True)

    # Foreign key for parent community and foreign uuid
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))
    community_uuid = db.Column(db.String(32))

    # Chat profile
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    messages = db.relationship('Message', backref='chat', lazy='dynamic')
    memberships = db.relationship('Membership', back_populates='chat', lazy='dynamic')

    def from_dict(self, data):
        self.name = data['name']
        self.created_at = datetime.utcnow()
        self.uuid = uuid.uuid4().hex


    def to_dict(self, terminating=False):
        data = {
            'uuid': self.uuid,
            'name': self.name,
            'created_at': str(self.created_at)

            }

        if not terminating:
            data.update({
                'members': [membership.member.to_dict() for membership in self.memberships],
                'messages': [message.to_dict() for message in self.messages]
            })

        return data
