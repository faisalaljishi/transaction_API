class User:
    def __init__(self):
        #self.userName = ''
        self.transactionHistory = []
        self.payers = {}
        self.totalValue = 0
        self.fundQueue = []

    def addTransaction(self, payer, value):
        payload = (payer,value, len(self.transactionHistory))
        self.transactionHistory.append(payload)
        self.fundQueue.append(payload)

        if payer in self.payers:
            self.payers[payer] += value
        else:
            self.payers[payer] = value

        self.totalValue += value

    def error(self):
        raise Exception('Error, cannot pay user negative values')

    def earn(self, payer, value):
        self.addTransaction(payer, value) if value > 0 else self.error()

    def spend(self, spend_amount):
        if self.totalValue < spend_amount:
            raise Exception('Not Enough Funds')
        new_funds = []

        def spend_helper(spendable_points, spend_amount, balance):
            spendable_points -= spend_amount
            balance -= spend_amount
            self.totalValue -= spend_amount
            payload = (payer, -spend_amount, len(self.transactionHistory))
            self.transactionHistory.append(payload)

            return spendable_points, balance

        while(self.fundQueue and spend_amount>0):
            payload = self.fundQueue.pop(0)
            payer, spendable_points, id = payload
            balance = self.payers[payer]

            if spendable_points >= spend_amount:
                spendable_points, balance = spend_helper(spendable_points, spend_amount, balance)
                if spendable_points != 0:
                    payload = (payer, spendable_points, id)
                    new_funds.append(payload)

                spend_amount = 0
            # if spendable_points < spend_amount
            else:
                spend_amount, balance = spend_helper(spend_amount, spendable_points, balance)

            self.payers[payer] = balance

        if(not self.fundQueue) and spend_amount>0:
            print('something went terribly wrong')

        new_funds += self.fundQueue
        self.fundQueue = new_funds
        print(self.totalValue)