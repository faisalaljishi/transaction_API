from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
#Ryan test

#Contains the name of the user, as well as the total balance coresspnding to all the user's payers
#AbstractUser might be a better approach here for authentication if full stack development with django.
class User(models.Model):
    name    = models.CharField(max_length=200, help_text='Name of user', unique=True, primary_key=True)
    totalBalance = models.IntegerField(default=0)

    def getBalance(self):
        return self.totalBalance
    def updateBalance(self, points):
        self.totalBalance +=points
    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)


#Contains the company, and all the balances it maintains for each user.
class Payer(models.Model):
    name    = models.CharField(max_length=200, help_text='Name of payer', unique=True, primary_key=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)

def keyCreate(payer, user):
    return ', '.join([str(payer), str(user)])

#Helper class to store all the balances of users for each company
class Balance(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT, null=False)
    payer = models.ForeignKey('Payer', on_delete=models.PROTECT, null=False)
    key = models.CharField(max_length=200, help_text='Balance key: (Payer.name, User.name)', primary_key=True, default=('(Payer.name, User.name)'))
    balance = models.IntegerField(default=0)

    def getBalance(self):
        return self.balance

    def updateBalance(self, points):
        self.balance +=points

    def overwriteBalance(self, points):
        self.balance = points
    class Meta:
        ordering = ['user']

    def __str__(self):
        return str(self.key)

#contains all Transactions the server has seen, can be sorted/filtered by user
class Transaction(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT, null=False)
    payer   = models.ForeignKey('Payer', on_delete=models.PROTECT, null=False)
    points  = models.IntegerField()
    date    = models.DateTimeField(auto_now=False, auto_now_add=True)

    def value(self):
        return self.points

    class Meta:
        ordering = ['user','date']

    def __str__(self):
        return ', '.join([str(self.payer), str(self.points), str(self.date)])

#Contains the current fund spending order for each user.
class FundQueue(models.Model):
    user = models.ForeignKey('User', on_delete=models.PROTECT, null=False)
    payer   = models.ForeignKey('Payer', on_delete=models.PROTECT, null=False)
    points  = models.IntegerField()
    date    = models.DateTimeField(auto_now=False, auto_now_add=True)

    def value(self):
        return self.points

    def overwriteValue(self, points):
        self.points =points

    class Meta:
        ordering = ['user', 'date']

    def __str__(self):
        return ', '.join([str(self.payer), str(self.points), str(self.date)])
