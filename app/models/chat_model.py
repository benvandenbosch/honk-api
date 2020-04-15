from app import db
from datetime import datetime, timedelta
from app.models.user_model import User

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)
    messages = db.relationship('Message', backref='chats', lazy='dynamic')


    def from_dict(self, data):
        self.name = data['name']
        self.created_at = datetime.utcnow()

    def to_dict(self):
        members = [member.username for member in self.members]
        data = {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'members': self.members
            }

        return data
