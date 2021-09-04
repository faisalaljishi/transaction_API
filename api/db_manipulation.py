from .models import User, Transaction, Payer, FundQueue, Balance, keyCreate
from django.shortcuts import get_object_or_404,get_list_or_404
from points.settings import DEBUG

class TransactionManager:

    #Creates user, payer and balance if they do not exist
    def incaseDNE(self, serializer):
        user, pay = serializer.initial_data.get('user'), serializer.initial_data.get('payer')
        if DEBUG: print(user, pay)
        print(user, pay)
        #Creates new user and payer if they do not exist
        #b1,b2 are True if obj exists, we are creating, we know they dont
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
        balanceObj, boolean3 = Balance.objects.get_or_create(key=bal_key, user= userObj, payer= payerObj)

        if DEBUG:  print(userObj, payerObj, balanceObj)
        if DEBUG: print(boolean1, boolean2, boolean3)
        if DEBUG: print(userObj.getBalance(), balanceObj.getBalance())

        #adds points to current balance
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
        #formatted as -x, meaning we want to deduct x amount of points
        if int(instance['points']) >= 0:
            raise Exception('Error, cannot deduct a positive value or 0')

        thisUser, points = instance['user'], int(instance['points'])

        # get the fundq for that user, the object, and turn points positive
        # fundq is ordered from oldest to newest by Django
        fundq = FundQueue.objects.all().filter(user=thisUser)
        thisUserObj = User.objects.get(name=thisUser)
        points = -points

        if thisUserObj.getBalance() < points:
            raise Exception('Not Enough Funds')

        spent = []
        # This is the Q of the available funds to be spent in order
        for fq in fundq:
            # if the points left is less than 0, we are done
            if points < 0:
                break

            # from fq, produce the payer and the points available

            # get the balance corresponding to the balance of the user for this specific payer

            currPayer, currPoints = fq.payer, fq.points
            currPayerObj = Payer.objects.get(name=currPayer)
            currBalance = Balance.objects.get(key=keyCreate(fq.payer, thisUser)).getBalance()

            def points_update(user_points, points_to_deduct, user_balance=currBalance):
                user_points -= points_to_deduct
                user_balance -= points_to_deduct
                spent.append({"payer": currPayer.name, "points": -points_to_deduct})
                thisUserObj.updateBalance(-points_to_deduct)
                thisUserObj.save()

                # this is the permanent transaction history that is written only, never modified/deleted
                t = Transaction.objects.create(user=thisUserObj,
                                               payer=currPayerObj,
                                               points=-points_to_deduct)
                t.save()

                return user_points, user_balance

            # if the current transaction on the Q will completely cover the remaining point amount
            if currPoints >= points:
                # deduct the points from the transaction and payers+user balance, and update the users total
                currPoints, currBalance = points_update(currPoints, points)

                # if the transaction on the Q is zero, we can discard it completely,
                # otherwise we need to keep it there until it is depleted
                if currPoints != 0:
                    # This will be the new front of the Q,
                    # update its value to itself minus the points we just spent
                    fq.overwriteValue(currPoints)
                    fq.save()
                else:
                    # if we dont delete this, the front of the Q would be 0 points
                    fq.delete()

            # if currPoints < points
            else:
                # we are going to use up currPoints completely, as it smaller than the points we want to spend
                currPoints, currBalance = points_update(points, currPoints)

                # we will remove the funds we just spent from
                fq.delete()

            # finally we need to update the (payer, user) balance
            # this line will  always occur
            p = Balance.objects.get(key=keyCreate(fq.payer, thisUser))
            p.overwriteBalance(currBalance)
            p.save()

        return spent





