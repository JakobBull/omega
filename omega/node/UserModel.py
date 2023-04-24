import rsa



class User:
    def __init__(self):
        (self.public_key, self._private_key) = rsa.newkeys(512)
