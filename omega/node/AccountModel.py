from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from omega.node.Transaction import Transaction
class AccountModel():

    def __init__(self):
        self.accounts = []
        self.balances = {}
        self.messages = {}

    def toJson(self):
        account_placeholders = [f'Account{number}' for number in range(len(self.accounts))]
        #To make sure dictionary ordering is consistent
        balances_list = [self.balances[index] for index in self.accounts]
        messages_list = [self.messages[index] for index in self.accounts]

        return {'accounts': {placeholder: account for (placeholder, account) in zip(account_placeholders, self.accounts)},
                'balances': {placeholder: balance for (placeholder, balance) in zip(account_placeholders, balances_list)},
                'messages': {placeholder: message for (placeholder, message) in zip(account_placeholders, messages_list)}}

    def handleMessage(self, transaction: "Transaction"):
        pass

    def addAccount(self, publicKeyString):
        if not publicKeyString in self.accounts:
            self.accounts.append(publicKeyString)
            self.balances[publicKeyString] = 0
            self.messages[publicKeyString] = []

    def getBalance(self, publicKeyString):
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        return self.balances[publicKeyString]
    
    def getMessage(self, publicKeyString):
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        return self.messages[publicKeyString]
    
    def addMessage(self, publicKeyString, message):
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        self.messages[publicKeyString].append(message)

    def removeMessage(self, publicKeyString, message):
        self.messages[publicKeyString].remove(message)

    def updateBalance(self, publicKeyString, amount):
        if publicKeyString not in self.accounts:
            self.addAccount(publicKeyString)
        self.balances[publicKeyString] += amount
