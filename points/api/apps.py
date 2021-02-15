from django.apps import AppConfig
from django.db.models.signals import pre_save, post_save
from django.utils.translation import ugettext_lazy as _

class ApiConfig(AppConfig):
    name = 'api'
    def ready(self):
        import api.signals
# class UserConfig(AppConfig):
#     name = 'User'
#
#     def ready(self):
#         import User.signals
#
class TransactionConfig(AppConfig):
    name = 'transaction'
    verbose_name = _('Transaction')

    def ready(self):
        from . import signals
        from . import models
        #transaction = self.get_model('Transaction')
        # pre_save.connect(signals.createTransactionPre, sender=models.Transaction)

# class ProductConfig(AppConfig):
#     name = 'product'
#
#     def ready(self):
#         import product.signals
#
# class ProductConfig(AppConfig):
#     name = 'product'
#
#     def ready(self):
#         import product.signals
#
# class ProductConfig(AppConfig):
#     name = 'product'
#
#     def ready(self):
#         import product.signals

