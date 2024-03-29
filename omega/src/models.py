from flaskext.mysql import MySQL
import hashlib

from omega.node.Node import Node
#from omega.src.blockchain_interaction import Message
from omega.node.Message import Message
from omega.node.BlockchainUtils import BlockchainUtils

class User:

    def __init__(self, username, password_hash, location=None):
        self.username = username
        self.password_hash = password_hash
        self.location = location

    def create_keys(self):
        self.private_key = None
        self.public_key = None

    def authenticate(self, password):
        pass

class Website:

    def __init__(self, app):
        self.app = app
        self.users = []

        self.mysql = MySQL(app, host="localhost", user="root", password="Jakob@multiplii2021", db="geeklogin", autocommit=True)
        self.mysql.init_app(app)

    def create_account(self, username, password, email):
        cursor = self.mysql.get_db().cursor()
        cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
        self.mysql.connect().commit()

    def check_login(self, username, password):
        cursor = self.mysql.get_db().cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        return account
    
    def check_account(self, username):
        cursor = self.mysql.get_db().cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        return account
    
    def broadcast_signup_request(self, username):
        payload = Message('public-key', {'username': username, 'password': 'passwordhash'})


class WebsiteBlockchainInterface:

    def __init__(self) -> None:
        self.status = None
        self.node = Node('localhost', 10050)
        self.node.startP2P()
        self.node.startAPI(5050)
        print(f"Started Interface at ports 10050 and 5050.")

    def _update_status(self):
        pass

    def broadcast_request(self):
        message = Message(self.p2p.socketConnector, 'BLOCKCHAINREQUEST', None)
        self.node.p2p.broadcast(BlockchainUtils.encode(message))

    def inbound_message(self):
        pass
