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
    def validate_points(self, points):
        # if points <= 0:
        #     raise Exception('Error, cannot pay user negative values')
        return points

    def validate_payer(self, payer):
        return payer

    def validate_user(self, user):
        return user

    class Meta:
        model = Transaction
        fields = ['user', 'payer', 'points', 'date', 'id']
        extra_kwargs = {'points': {'validators': []},'payer': {'validators': []}, 'user': {'validators': []},'date': {'required': False}, 'id': {'required': False}}
        validators = []

class FundQueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundQueue
        fields = '__all__'
