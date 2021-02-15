from .models import User, Transaction, Payer, FundQueue, Balance
from datetime import datetime
class TransactionManager:
    #protected methods
    # def _userCheck(self, name):
    #     try:
    #         acc_obj = User.objects.get(name=name)
    #     except User.DoesNotExist:
    #         acc_obj = User(name=name)
    #     return acc_obj
    #
    # def _payerCheck(self, name, user, points):
    #     try:
    #         pay_obj = Payer.objects.get(name=name)
    #         bal_obj = self.balanceCheck(user, pay_obj, points)
    #     except Payer.DoesNotExist:
    #         pay_obj = Payer(name=name)
    #         bal_obj = Balance(user=user, payer=pay_obj, balance=points)
    #     return pay_obj, bal_obj
    #
    # def _balanceCheck(self, user, payer, points):
    #     try:
    #         bal_obj = Balance.objects.get(user=user)
    #         bal_obj.updateBalance(points)
    #     except Balance.DoesNotExist:
    #         bal_obj = Balance(user=user, payer=payer, balance=points)
    #     return bal_obj

    #public methods
    #Adds a transaction to the history and fundsqueue, creates user, payer+balance if they do not exist
    def createTransaction(self, new):
        if new['points'] <= 0:
            raise Exception('Error, cannot pay user negative values') #figure out how to raise error correctly
        user, payer, points = new['user'], new['payer'], new['points']#, new['date'], new['id']
        userObj = User.objects.get_or_create(name=new.user)
        payerObj= Payer.objects.get_or_create(name=payer)
        balanceObj = Balance.objects.get_or_create(user=user, payer=payer)

        User.objects.update_or_create(name=new.user, totalBalance=userObj.totalBalance + points)
        Balance.objects.update_or_create(user=userObj, payer= payerObj, balance=balanceObj.balance + points)

        Transaction.objects.create(user=user,
                    payer=payer,
                    points=points,
                    date=datetime.now())

        FundQueue.objects.create(user=user,
                  payer=payer,
                  points=points,
                  date=datetime.now())
        user.updateBalance(points)









{
        "id": 2,
        "points": 200,
        "date": "2021-02-15T01:34:17Z",
        "user": "Joe Schmoe",
        "payer": "DANNON"
    }