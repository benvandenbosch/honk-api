#!/usr/bin/env python

from config import Config
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Message, Chat
from config import Config
from flask import jsonify
from flask_testing import TestCase
import json


# Create subclass to override SQLAlchemy config and make in-memory SQLite db
class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_join_chat(self):
        u = User(username='test', email='test@email.com')
        u2 = User(username='test2', email='test2@gmail.com')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()

        c = Chat(name='chat1')
        db.session.add(c)
        db.session.commit()

        u.join_chat(c)
        u2.join_chat(c)
        db.session.commit()

        self.assertEqual(len(c.members), 2)
        self.assertTrue(u in c.members)
        self.assertTrue(u2 in c.members)

class UserSignupFlow(TestCase):

    def create_app(self):
        return create_app(TestConfig)

    def setUp(self):
        # self.app = create_app(self)
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # self.app_context.pop()

    # Test that a user can be created and proper response is returned
    def test_create_user(self):
        header = {"Content-Type": "application/json"}
        self.assertTrue(True)

        payload = json.dumps({
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })


        # Create the user
        response = self.client.post('/api/users', headers=header, data=payload)
        expected_response = User.query.filter_by(username='testuser').first().to_dict()

        # Response status code should be 201 for successful creation
        self.assertEqual(201, response.status_code)

        # Assert that response is equal to database entry
        self.assertEqual(expected_response, response.json)


if __name__ == '__main__':
    unittest.main()
