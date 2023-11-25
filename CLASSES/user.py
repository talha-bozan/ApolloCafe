from flask import jsonify
from google.cloud import firestore

class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def save(self):
        db = firestore.Client()
        user_ref = db.collection('users').document(self.id)
        user_ref.set(self.to_dict())

    @staticmethod
    def get_all():
        db = firestore.Client()
        users_ref = db.collection('users')
        users = [doc.to_dict() for doc in users_ref.stream()]
        return jsonify(users)
