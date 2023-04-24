import rsa

def encrypt_object(object, public_key):
    if type(object) == dict:
        return {key: rsa.encrypt(value.encode('utf8'), public_key) for (key,value) in object.items()}


def decryp_object(object, private_key):
    if type(object) == dict:
        return {key: rsa.decrypt(value, private_key).decode('utf8') for (key,value) in object.items()}

