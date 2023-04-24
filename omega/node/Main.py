"""
Main module.

Arguments passed as follows:
IP address
Port number: Must be greater than 10000.
API Port number: For example 5000, 5001, 5002, ...

FIRST NODE MUST HAVE RECEIVING PORT 10001
"""

from omega.node.Transaction import Transaction
from omega.node.Wallet import Wallet
from omega.node.TransactionPool import TransactionPool
from omega.node.Block import Block
from omega.node.Blockchain import Blockchain
import pprint
from omega.node.BlockchainUtils import BlockchainUtils
from omega.node.AccountModel import AccountModel
from omega.node.Node import Node
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
 