class User:
    def __init__(self):
        #self.userName = ''
        self.transactionHistory = []
        self.payers = {}
        self.totalValue = 0
        self.fundQueue = []

    #costly operation, keep track of total as you go
    def updateTotal(self):
        self.totalValue = sum(self.payers.values())

    def updateQueue(self, newFunds):
        self.fundQueue = newFunds


    def addTransaction(self, payer, value):
        payload = (payer,value, len(self.transactionHistory))
        self.transactionHistory.append(payload)
        self.fundQueue.append(payload)

        if payer in self.payers:
            self.payers[payer] += value
        else:
            self.payers[payer] = value

        self.updateTotal()

    def error(self):
        raise Exception('Error, cannot pay user negative values')

    def earn(self, payer, value):
        return self.addTransaction(payer, value) if value > 0 else self.error()

    def spend(self, value):
        if self.totalValue < value:
            raise Exception('Not Enough Funds')
        new_funds = []
        while(self.fundQueue and value>0):
            payload = self.fundQueue.pop(0)
            payer, curr, id = payload
            balance = self.payers[payer]
            if curr >= value:
                curr -=value
                balance -= value
                if curr != 0:
                    payload = (payer, curr, id)
                    new_funds.append(payload)
                payload = (payer, -value, len(self.transactionHistory))
                self.transactionHistory.append(payload)
                value = 0
            elif curr < value: #for readablity
                value -= curr
                balance -= curr
                payload = (payer, -curr, len(self.transactionHistory))
                self.transactionHistory.append(payload)

            self.payers[payer] = balance


        new_funds += self.fundQueue
        self.updateTotal()
        self.updateQueue(new_funds)