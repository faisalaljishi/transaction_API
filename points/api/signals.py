from django.db.models import signals
from django.dispatch import receiver
from .models import User, Transaction, Payer, FundQueue, Balance, keyCreate
from .db_manipulation import TransactionManager
from django.db.models.signals import pre_save, post_save

DEBUG = 0
# pre_save method signal
@receiver(signals.pre_save, sender=Transaction)
def createTransactionPre(sender, instance, **kwargs):

    t = TransactionManager()
    if instance.points > 0:
        t.addTransaction(instance)
    # else:
    #     raise Exception('Error, cannot pay user negative values')




# post_save method
@receiver(signals.post_save, sender=Transaction)
def createTransactionPost(sender, instance, created, **kwargs):
    if DEBUG: print("Save method is done")