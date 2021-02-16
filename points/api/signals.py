from django.db.models import signals
from django.dispatch import receiver
from .models import User, Transaction, Payer, FundQueue, Balance, keyCreate
from .db_manipulation import TransactionManager
from django.db.models.signals import pre_save, post_save

DEBUG = 0
# pre_save method signal for Transaction
@receiver(signals.pre_save, sender=Transaction)
def createTransactionPre(sender, instance, **kwargs):

    #if we are saving a negative value, it is for history purposes only,
    # we do not want addTransaction to interfere and change any balances,
    # we already take care of it so we just want it to be written
    if instance.points > 0:
        t = TransactionManager()
        t.addTransaction(instance)
    # else:
    #     raise Exception('Error, cannot pay user negative values')




# post_save method
@receiver(signals.post_save, sender=Transaction)
def createTransactionPost(sender, instance, created, **kwargs):
    if DEBUG: print("Save method is done")