from rest_framework import serializers
from .models import Wallet, Transactions

from django.contrib.auth.models import User


class InitializeWalletSerializer(serializers.Serializer):
    customer_xid = serializers.CharField(max_length=100)

    # def validate_customer_xid(self, value):
    #     if value.


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transactions
