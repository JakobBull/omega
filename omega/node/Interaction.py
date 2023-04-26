from omega.node.Wallet import Wallet
from omega.node.BlockchainUtils import BlockchainUtils
import requests

def postTransaction(sender: Wallet, receiver: Wallet, amount, type, message=None):
    transaction = sender.createTransaction(
        receiver.publicKeyString(), amount, type, message=message)
    url = "http://localhost:5000/transaction"
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)


if __name__ == '__main__':

    bob = Wallet()
    alice = Wallet()
    alice.fromKey('omega/node/keys/stakerPrivateKey.pem')
    exchange = Wallet()

    #forger: genesis
    postTransaction(exchange, alice, 100, 'EXCHANGE')
    print("Done 1.")
    postTransaction(exchange, bob, 100, 'EXCHANGE')
    print("Done 2.")
    postTransaction(alice, bob, 0, 'TRANSFER', message=['Hello Bob!'])
    print("Done 3.")


    # forger: probably alice
    postTransaction(alice, alice, 25, 'STAKE')
    print("Done 4.")
    postTransaction(alice, bob, 1, 'TRANSFER')
    print("Done 5.")
    postTransaction(alice, bob, 1, 'TRANSFER')
    print("Done 6.")
