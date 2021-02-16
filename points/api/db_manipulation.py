from .models import User, Transaction, Payer, FundQueue, Balance, keyCreate
from django.shortcuts import get_object_or_404,get_list_or_404

DEBUG = 0
class TransactionManager:

    #Creates user, payer and balance if they do not exist
    def incaseDNE(self, serializer):
        user, pay = serializer.initial_data['user'], serializer.initial_data['payer']
        if DEBUG: print(user, pay)
        userObj, b1 = User.objects.get_or_create(name=user)
        payerObj, b2 = Payer.objects.get_or_create(name=pay)
        if DEBUG: print(userObj, payerObj)
        if DEBUG: print('user,payer are:', b1, b2)
        userObj.save()
        payerObj.save()

    def addTransaction(self, instance):
        user, payer, points = instance.user, instance.payer, instance.points
        if DEBUG: print(user, payer, points)
        # User and payer will always exist because incaseDNE is called before addTransaction, but balance may or may not exist.
        userObj, boolean1 = User.objects.get_or_create(name=user)
        payerObj, boolean2 = Payer.objects.get_or_create(name=payer)
        balanceObj, boolean3 = Balance.objects.get_or_create(user=userObj, payer=payerObj, key=keyCreate(payer, user))

        if DEBUG:  print(userObj, payerObj, balanceObj)
        if DEBUG: print(boolean1, boolean2, boolean3)
        if DEBUG: print(userObj.getBalance(), balanceObj.getBalance())

        userObj.updateBalance(points)
        balanceObj.updateBalance(points)

        if DEBUG: print(userObj.getBalance(), balanceObj.getBalance())

        userObj.save()
        payerObj.save()
        balanceObj.save()

        fq = FundQueue.objects.create(user=user,
                                      payer=payer,
                                      points=points)

    def deductTransaction(self, instance):
        if instance['points'] >= 0:
            raise Exception('Error, cannot deduct a positive value')
        thisUser, points = instance['user'], instance['points']

        fundq = FundQueue.objects.all().filter(user=thisUser)
        thisUserObj = User.objects.get(name=thisUser)
        # thisPayerObj = Payer.objects.get(name=thisPayer)
        points= -points

        if thisUserObj.getBalance() < points:
            raise Exception('Not Enough Funds')

        for fq in fundq:
            if points < 0:
                break
            currPayer, currPoints = fq.payer, fq.points
            currPayerObj = Payer.objects.get(name=currPayer)

            currBalance = Balance.objects.get(key=keyCreate(fq.payer, thisUser)).getBalance()
            if currPoints >= points:
                currPoints  -=points
                currBalance -=points
                thisUserObj.updateBalance(-points)
                thisUserObj.save()
                if currPoints != 0:
                    print('These are the curr:', currPoints)
                    fq.overwriteValue(currPoints)
                    fq.save()
                    t = Transaction.objects.create(user=thisUserObj,
                                                   payer=currPayerObj,
                                                   points=-points)
                    t.save()
                points = float('-inf')
            elif currPoints < points:   #for readablity
                points      -= currPoints
                currBalance -= currPoints
                thisUserObj.updateBalance(-currPoints)
                thisUserObj.save()
                t = Transaction.objects.create(user=thisUserObj,
                                               payer=currPayerObj,
                                               points=-currPoints)
                t.save()
                fq.delete()

            p = Balance.objects.get(key=keyCreate(fq.payer, thisUser))
            p.overwriteBalance(currBalance)
            p.save()







