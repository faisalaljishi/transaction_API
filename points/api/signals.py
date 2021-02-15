from django.db.models import signals
from django.dispatch import receiver
from .models import User, Transaction, Payer, FundQueue, Balance, keyCreate
from django.db.models.signals import pre_save, post_save

DEBUG = 1
# pre_save method signal
@receiver(signals.pre_save, sender=Transaction)
def createTransactionPre(sender, instance, **kwargs):
    #Could not figure out how to make it not save the Transaction without throwing an Exception
    if instance.points <= 0:
        raise Exception('Error, cannot pay user negative values')
        #Testing code
        # print('Less than or equal to zero call')
        # return
    user, payer, points = instance.user, instance.payer, instance.points
    if DEBUG: print(user,payer,points)
    #User and payer will always exist, but balance may not.
    userObj,    boolean1  = User.objects.get_or_create(name=user)
    payerObj,   boolean2  = Payer.objects.get_or_create(name=payer)
    balanceObj, boolean3  = Balance.objects.get_or_create(user=userObj, payer=payerObj, key=keyCreate(payer, user))

    if DEBUG:  print(userObj, payerObj, balanceObj)
    if DEBUG: print(boolean1,boolean2, boolean3)
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


# post_save method
@receiver(signals.post_save, sender=Transaction)
def createTransactionPost(sender, instance, created, **kwargs):
    if DEBUG: print("Save method is done")