from hashlib import sha256

print(sha256('hello'.encode('utf-8')).hexdigest())

username = input("Please enter your username: ")
password = input("Please enter your password: ")

print(username, type(username), sha256(username.encode('utf-8')).hexdigest())

print(sha256((sha256(username.encode('utf-8')).hexdigest() + sha256(password.encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest())

