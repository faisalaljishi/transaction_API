from django.contrib import admin
from .models import User, Transaction, Payer, FundQueue, Balance
# Register your models here.

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra=0
class PayerInline(admin.TabularInline):
    model = Payer
    extra=0

class FundQueueInline(admin.TabularInline):
    model = FundQueue
    extra = 0
class BalanceInline(admin.TabularInline):
    model = Balance
    extra = 0

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'totalBalance')
    inlines = [BalanceInline, TransactionInline, FundQueueInline]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'payer', 'points', 'date')
    list_filter = ('user', 'payer', 'points', 'date')

@admin.register(Payer)
class PayerAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [TransactionInline, BalanceInline]

@admin.register(FundQueue)
class FundQueueAdmin(admin.ModelAdmin):
    list_display = ('user', 'payer', 'points', 'date')

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'payer', 'balance')
