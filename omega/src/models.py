import hashlib

class User:

    def __init__(self, username, password_hash, location=None):
        self.username = username
        self.password_hash = password_hash
        self.location = location

    def create_keys(self):
        self.private_key = None
        self.public_key = None

    def authenticate(self, password):


class Website:

    def __init__(self):
        self.users = []

    def generate_key(self):
        return 1

class Node:

    def __init__(self):
        pass

    def authenticate(self):
        pass

    def create_blocK(self):
        pass

class Network:

    def __init__(self):
