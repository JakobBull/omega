import rsa
import time
import validators

from omega.src.block import Block, Blockchain

class Field:

    def __init__(self) -> None:
        self._status = False

    def set_status(self, status):
        self._status = status

    def get_status(self):
        return self._status


class Network:

    def __init__(self) -> None:
        self.blockchain = Blockchain()
        self.services = {}
    
    def add_key(self, key, service):
        block = Block(self.blockchain.last_block.index, str(key), time.time(),
                  self.blockchain.last_block.hash, 0)
        proof = self.blockchain.proof_of_work(block)
        self.blockchain.add_block(block, proof)

        self.services[service] = key

    def check_key(self, key):
        if key in self.services.values():
            return True
        return False


class Service:

    def __init__(self, name, url) -> None:
        self.name = name
        if validators.url(url):
            self.url = url
        else:
            raise IOError("The provided url format is incorrect for: ", url)
        self._private_key = None
        self.public_key = None
        self.generate_keys()

    def generate_keys(self):
        (self.public_key, self._private_key) = rsa.newkeys(512)

    def sign(self, message):
        message = message.encode()
        signature = rsa.sign(message, self._private_key, 'SHA-1')
        return signature


class User:

    def __init__(self) -> None:
        self.public_key = None
        self._private_key = None
        self.generate_keys()

    def generate_keys(self):
        (self.public_key, self._private_key) = rsa.newkeys(512)

    def verify(self, message, signature, sender, network):
        message = message.encode()
        outp = rsa.verify(message, signature, sender.public_key)
        registered_key = network.check_key(sender.public_key)

        if outp == 'SHA-1' and registered_key:
            return True

        return False

    def click(self, service_feature):
        # This is essentially a run.
        service_feature(self)

user1 = User()
service1 = Service("hello", "https://www.hello.com/")

network = Network()
network.add_key(service1.public_key, service1)

msg = service1.sign(str(user1.public_key))
print(user1.verify(str(user1.public_key), msg, service1, network))