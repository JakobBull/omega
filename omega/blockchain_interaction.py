from dataclasses import dataclass
import requests
from tutorial.BlockchainUtils import BlockchainUtils

@dataclass
class Message:

    def __init__(self, name, data) -> None:
        self.name = name
        self.data = data
        

def verification_request(website_name, user_name, url="http://localhost:5000/api/verify"):
        data = requests.get(url).json()
        message_data = website_name + user_name + str(data[current_token])
        message = Message(name=website_name, data=message_data)
        package = {'transaction': BlockchainUtils.encode(message)}
        request = requests.post(url, json=package)


