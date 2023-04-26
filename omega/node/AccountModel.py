class AccountModel():

    def __init__(self):
        self.accounts = []
        self.balances = {}
        self.messages = {}

    def toJson(self):
        return {'accounts': self.accounts,
                'balances': self.balances,
                'messages': self.messages}

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
