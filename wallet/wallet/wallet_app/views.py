from rest_framework.response import Response
from .utils import success_response
from rest_framework import permissions
from rest_framework.views import APIView
from .models import Wallet, Transactions
from .serializers import InitializeWalletSerializer, TransactionSerializer, WalletSerializer
from .services import initialize_user_and_customer, enable_wallet, disable_wallet


class InitializeWalletView(APIView):
    serializer_class = InitializeWalletSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        customer_xid = serializer.validated_data['customer_xid']
        token = initialize_user_and_customer(customer_xid)
        return success_response({"token": token})


class WalletStatusChangeView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        customer = user.customer
        wallet = enable_wallet(customer)
        serializer = WalletSerializer(wallet)
        return success_response(serializer.data)

    def patch(self, request, *args, **kwargs):
        user = request.user
        customer = user.customer
        wallet = disable_wallet(customer)
        serializer = WalletSerializer(wallet)
        return success_response(serializer.data)


class WalletBalance(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class WalletTransactions(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        transactions = Transactions.objects.filter(wallet=wallet)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class AddMoney(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        wallet = Wallet.objects.get(user=request.user)
        amount = request.data['amount']
        wallet.balance += amount
        wallet.save()
        transaction = Transactions(wallet=wallet, amount=amount)
        transaction.save()
        return Response({'status': 'success'})


class Usemoney(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        wallet = Wallet.objects.get(user=request.user)
        amount = request.data['amount']
        if wallet.balance < amount:
            return Response({'status': 'Insufficient Balance'})
        wallet.balance -= amount
        wallet.save()
        transaction = Transactions(wallet=wallet, amount=-amount)
        transaction.save()
        return Response({'status': 'success'})


class Disablewallet(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=request.user)
        wallet.delete()
        return Response({'status': 'Disabled'})












