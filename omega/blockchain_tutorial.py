import copy
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import json
import uuid
import time

"""
Global utilities required for the blockchain.

methods:
hash: creates SHA256 hash of data

"""
class BlockchainUtils:

    """
    Create SHA256 hash of data.

    parameters:
    :data: data as string.

    returns: hash of data
    """
    @staticmethod
    def hash(data: str):
        dataString = json.dumps(data)
        dataBytes = dataString.encode('utf-8')
        dataHash = SHA256.new(dataBytes)
        return dataHash

"""
Transaction class for blockchain.

Instance of this class is an individual transaction on the blockchain.

parameters:
:senderPublicKey: Address of sender of transaction.
:receiverPublicKey: Address of receiver of transaction.
:amount: Amount of transaction.
:type: Transaction type.

"""
class Transaction:

    def __init__(self, senderPublicKey, receiverPublicKey, amount, type) -> None:
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex
        self.timestamp = time.time()
        self.signature = ''

    """
    Get a dictionary of class attributes.

    """
    def toJson(self):
        return self.__dict__

    """
    Set signature.

    """
    def sign(self, signature):
        self.signature = signature

    """
    Return copy of class attributes as dictionary with blank signature.

    """
    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    """
    Check if object is the same as another object by comparing id.
    """
    def equals(self, transaction):
        if self.id == transaction.id:
            return True
        else:
            return False

"""
Wallet class for blockchain.

Wallet is abstractly owned by user and transactions occur between wallets.

"""
class Wallet:

    def __init__(self) -> None:
        self.keyPair = RSA.generate(2048)

    """
    Sign some data with wallet private key.
    """
    def sign(self, data):
        dataHash = BlockchainUtils.hash(data)
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair)
        signature = signatureSchemeObject.sign(dataHash)
        return signature.hex()

    """
    Check if another wallet's signature 
    """
    @staticmethod
    def signatureValid(data, signature, publicKeyString):
        signature = bytes.fromhex(signature)
        dataHash = BlockchainUtils.hash(data)
        publicKey = RSA.import_key(publicKeyString)
        signatureSchemeObject = PKCS1_v1_5.new(publicKey)
        signatureValid = signatureSchemeObject.verify(dataHash, signature)
        return signatureValid

    def publicKeyString(self):
        publicKeyString = self.keyPair.publickey().exportKey('PEM').decode('utf-8')
        return publicKeyString

    def createTransaction(self, receiver, amount, type):
        transaction = Transaction(self.publicKeyString(), receiver, amount, type)
        signature = self.sign(transaction.payload())
        transaction.sign(signature)
        return transaction
    
    def createBlock(self, transactions, lastHash, blockCount):
        block = Block(transaction, lastHash, self.publicKeyString(), blockCount)
        signature = self.sign(block.payload())
        block.sign(signature)
        return block

class TransactionPool:

    def __init__(self) -> None:
        self.transactions = []

    """
    Add a transaction to the transaction pool.
    """
    def addTransaction(self, transaction):
        self.transactions.append(transaction)
    
    """
    Check if a transaction is already in the transaction pool.
    """
    def transactionExists(self, transaction):
        # check if this transaction exists
        for poolTransaction in self.transactions:
            if poolTransaction.equals(transaction):
                return True
        return False

"""
Single Block in the Blockchain, adding transactions from the transaction pool to the blockchain.

parameters:
:transactions: Transactions to be added to the block from the transaction pool.
:lastHash: Hash of last Block required for cryptography.
:forger: Winner of the pool who gets to add to the Blockchain. #TODO: not implemented.
:blockCount: Number of the block.

"""
class Block:

    def __init__(self, transactions, lastHash, forger, blockCount) -> None:
        self.transactions = transactions
        self.lastHash = lastHash
        self.forger = forger
        self.blockCount = blockCount
        self.timestamp = time.time()
        self.signature = ''

    """
    Get a dictionary of class attributes.

    """
    def toJson(self):
        data = {}
        data['lastHash'] = self.lastHash
        data['forger'] = self.forger
        data['blockCount'] = self.blockCount
        data['timestamp'] = self.timestamp
        data['signature'] = self.signature
        jsonTransactions = []
        for transaction in self.transactions:
            jsonTransactions.append(transaction)
        data['transactions'] = jsonTransactions
        return data
    
    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation
    
    def sign(self, signature):
        self.signature = signature
         

if __name__ == '__main__':

    sender = 'sender'
    receiver = 'receiver'
    amount = 1
    type = 'TRANSFER'
    transaction = Transaction(sender, receiver, amount, type)
    
    wallet = Wallet()
    fraudulentWallet = Wallet()
    pool = TransactionPool()

    transaction = wallet.createTransaction(receiver, amount, type)
    
    if pool.transactionExists(transaction) == False:
        pool.addTransaction(transaction)

    block = wallet.createBlock(pool.transactions, 'lastHash', 1)
    print(block.toJson())
