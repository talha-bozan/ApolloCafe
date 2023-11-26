from flask import jsonify
from google.cloud import firestore

class User:
    def __init__(self, id, email, roles=None):
        self.id = id
        self.email = email
        self.roles = roles if roles else []

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'roles': self.roles
        }

    def is_admin(self):
        return 'admin' in self.roles
if __name__ == '__main__':
    user = User('123', 'th@g', ['admin'])
    print(user.to_dict())