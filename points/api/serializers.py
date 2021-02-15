from rest_framework import serializers
from .models import User, Payer, Balance, Transaction, FundQueue


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payer
        fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class FundQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundQueue
        fields = '__all__'
