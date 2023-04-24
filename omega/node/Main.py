"""
Main module.

Arguments passed as follows:
IP address
Port number: Must be greater than 10000.
API Port number: For example 5000, 5001, 5002, ...

FIRST NODE MUST HAVE RECEIVING PORT 10001
"""

from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
import pprint
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from Node import Node
import sys

if __name__ == '__main__':
    ip = sys.argv[1]
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])
    keyFile = None
    if len(sys.argv) > 4:
        keyFile = sys.argv[4]

    node = Node(ip, port, keyFile)
    node.startP2P()
    node.startAPI(apiPort)
 