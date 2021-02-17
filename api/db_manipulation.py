from .models import User, Transaction, Payer, FundQueue, Balance, keyCreate
from django.shortcuts import get_object_or_404,get_list_or_404

DEBUG = 0
class TransactionManager:

    #Creates user, payer and balance if they do not exist
    def incaseDNE(self, serializer):
        user, pay = serializer.initial_data['user'], serializer.initial_data['payer']
        if DEBUG: print(user, pay)

        #Creates new user and payer if they do not exist
        #b1,b2 are True if they do exist, False if corresponding obj does not
        userObj, b1 = User.objects.get_or_create(name=user)
        payerObj, b2 = Payer.objects.get_or_create(name=pay)

        if DEBUG: print(userObj, payerObj)
        if DEBUG: print('user,payer are:', b1, b2)

        #saves changes
        userObj.save()
        payerObj.save()

    def addTransaction(self, instance):
        user, payer, points = instance.user, instance.payer, instance.points
        if DEBUG: print(user, payer, points)

        # User and payer will always exist because incaseDNE is called before addTransaction, but balance may or may not exist.
        userObj, boolean1 = User.objects.get_or_create(name=user)
        payerObj, boolean2 = Payer.objects.get_or_create(name=payer)
        balanceObj, boolean3 = Balance.objects.get_or_create(key=keyCreate(payer, user))

        if DEBUG:  print(userObj, payerObj, balanceObj)
        if DEBUG: print(boolean1, boolean2, boolean3)
        if DEBUG: print(userObj.getBalance(), balanceObj.getBalance())

        #adds points to current balance
        userObj.updateBalance(points)
        balanceObj.updateBalance(points)

        if DEBUG: print(userObj.getBalance(), balanceObj.getBalance())

        #saves changes
        userObj.save()
        payerObj.save()
        balanceObj.save()

        fq = FundQueue.objects.create(user=user,
                                      payer=payer,
                                      points=points)

    def deductTransaction(self, instance):
        #expect the value to be formatted as -x, meaning we want to deduct x amount of points
        if instance['points'] >= 0:
            raise Exception('Error, cannot deduct a positive value or 0')
        thisUser, points = instance['user'], instance['points']

        #get the fundq for that user, the object, and turn points positive
        #fundq is automatically ordered from oldest to newest
        fundq = FundQueue.objects.all().filter(user=thisUser)
        thisUserObj = User.objects.get(name=thisUser)
        points= -points

        #total balance does not cover
        if thisUserObj.getBalance() < points:
            raise Exception('Not Enough Funds')

        spent =[]
        #This is the Q of the available funds in order to be spent
        for fq in fundq:
            #if the points left is less than 0, we are done
            if points < 0:
                break

            #from fq, produce the payer and the points available
            currPayer, currPoints = fq.payer, fq.points
            currPayerObj = Payer.objects.get(name=currPayer)

            #get the balance corresponding to the balance of the user for this specific payer
            currBalance = Balance.objects.get(key=keyCreate(fq.payer, thisUser)).getBalance()

            #if the current transaction on the Q will completely cover the remaining point amount
            if currPoints >= points:

                #deduct the points from the transaction and payers+user balance, and update the users total
                currPoints  -=points
                currBalance -=points
                spent.append({"payer": currPayer.name, "points": -points})
                thisUserObj.updateBalance(-points)
                thisUserObj.save()

                #if the transaction on the Q is zero, we can discard it completely,
                #otherwise we need to keep it there until it is depleted
                if currPoints != 0:
                    #This will be the new front of the Q,
                    # update its value to itself minus the points we just spent
                    fq.overwriteValue(currPoints)
                    fq.save()
                else:
                    #if we dont delete this, the front of the Q would be 0 points
                    fq.delete()

                # this is the permanent transaction history that is written only, never modified/deleted
                t = Transaction.objects.create(user=thisUserObj,
                                               payer=currPayerObj,
                                               points=-points)
                t.save()
                #points were completely covered, so we can set it to -inf to spot errors easily if they ever occur
                points = float('-inf')
            # could just be an else, but elif for readability
            elif currPoints < points:
                #we are going to use up currPoints completely, as it smaller than the points we want to spend
                points      -= currPoints
                currBalance -= currPoints
                spent.append({"payer": currPayer.name, "points": -currPoints})
                thisUserObj.updateBalance(-currPoints)
                thisUserObj.save()
                t = Transaction.objects.create(user=thisUserObj,
                                               payer=currPayerObj,
                                               points=-currPoints)
                t.save()
                #we will remove the funds we just spent from
                fq.delete()

            #finally we need to update the (payer, user) balance
            #this line will occur regardless of which if else occured
            p = Balance.objects.get(key=keyCreate(fq.payer, thisUser))
            p.overwriteBalance(currBalance)
            p.save()

        return spent





