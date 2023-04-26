from dataclasses import dataclass
import requests
from omega.node.BlockchainUtils import BlockchainUtils

@dataclass
class LoginMessage:

    def __init__(self, name, data) -> None:
        self.name = name
        self.data = data

class BlockchainInterface:
     
    def __init__(self) -> None:
          self.status = None
        
    def broadcast_login_request(self):
        pass

class UserModel:
     
    def __init__(self) -> None:
            self.username = None
            self.password = None
            self.public_key = None
        

def verification_request(website_name, user_name, url="http://localhost:5000/api/verify"):
        data = requests.get(url).json()
        message_data = website_name + user_name + str(data[current_token])
        message = Message(name=website_name, data=message_data)
        package = {'transaction': BlockchainUtils.encode(message)}
        request = requests.post(url, json=package)


