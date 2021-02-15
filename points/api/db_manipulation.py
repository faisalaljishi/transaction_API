from .models import User, Transaction, Payer, FundQueue, Balance, keyCreate
from django.shortcuts import get_object_or_404,get_list_or_404

DEBUG = 0
class TransactionManager:

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
        # User and payer will always exist, but balance may not.
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
        thisUser, thisPayer, points = instance['user'], instance['payer'], instance['points']
        fundq = FundQueue.objects.all().filter(user=thisUser)
        # fundq = get_list_or_404(FundQueue, user=thisUser)
        thisUserObj = User.objects.get(name=thisUser)
        thisPayerObj = Payer.objects.get(name=thisPayer)
        # print(fundq)
        # print(points)
        # print(thisUser, thisPayer, points)
        for fq in fundq:
            if points >= 0:
                break
            currPayer, currPoints = fq.payer, fq.points
            currPayerObj = Payer.objects.get(name=currPayer)
            currBalance = Balance.objects.get(key=keyCreate(fq.payer, thisUser)).getBalance()
            if currPoints >= points:
                currPoints  -=points
                currBalance -=points
                #update total
                if currPoints != 0:
                    print('These are the curr:', currPoints)
                    fq.overwriteValue(currPoints)
                    fq.save()
                t = Transaction.objects.create(user=thisUserObj,
                                               payer=currPayerObj,
                                               points=-points)
                t.save()
                points = 0
            elif currPoints < points:   #for readablity
                points      -= currPoints
                currBalance -= currPoints
                # update total
                t = Transaction.objects.create(user=thisUserObj,
                                               payer=currPayerObj,
                                               points=-currPoints)
                t.save()
                fq.delete()

            p = Payer.objects.get(name=fq.payer)
            #p.overwriteValue(currBalance)
            p.save()







{
        "id": 2,
        "points": 300,
        "date": "2021-02-15T01:34:17Z",
        "user": "Joe Schmoe",
        "payer": "UNILEVER"
}
{
        "id": 2,
        "points": -200,
        "date": "2021-02-15T01:34:17Z",
        "user": "Joe Schmoe",
        "payer": "DANNON"
}