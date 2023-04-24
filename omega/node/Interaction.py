from omega.node.Wallet import Wallet
from omega.node.BlockchainUtils import BlockchainUtils
import requests


def postTransaction(sender, receiver, amount, type):
    transaction = sender.createTransaction(
        receiver.publicKeyString(), amount, type)
    url = "http://localhost:5000/transaction"
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)


if __name__ == '__main__':

    bob = Wallet()
    alice = Wallet()
    alice.fromKey('keys/stakerPrivateKey.pem')
    exchange = Wallet()

    #forger: genesis
    postTransaction(exchange, alice, 100, 'EXCHANGE')
    print("Done 1.")
    postTransaction(exchange, bob, 100, 'EXCHANGE')
    print("Done 2.")
    postTransaction(exchange, bob, 10, 'EXCHANGE')
    print("Done 3.")

    # forger: probably alice
    postTransaction(alice, alice, 25, 'STAKE')
    print("Done 4.")
    postTransaction(alice, bob, 1, 'TRANSFER')
    print("Done 5.")
    postTransaction(alice, bob, 1, 'TRANSFER')
    print("Done 6.")
