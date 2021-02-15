from rest_framework import serializers
from .models import Transaction, Payer

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class PayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payer
        fields = '__all__'