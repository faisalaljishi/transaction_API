from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Transaction, Payer, FundQueue, Balance
from .serializers import TransactionSerializer, PayerSerializer, UserSerializer, BalanceSerializer, FundQueueSerializer
from .db_manipulation import TransactionManager
from ..points.settings  import DEBUG

# Create your views here.
@api_view(['GET'])
def overview(request):
    api_urls = {
        'All Fields': 'http://django-points-api.herokuapp.com/api/all/',
        'Lists': '',
        'User List': 'http://django-points-api.herokuapp.com/api/users/',
        'Payer List': 'http://django-points-api.herokuapp.com/api/payers/',
        'Balance List': 'http://django-points-api.herokuapp.com/api/balances/',
        'Transaction List': 'http://django-points-api.herokuapp.com/api/transactions/',
        'FundQueue List': 'http://django-points-api.herokuapp.com/api/funds/',
        'Details': '',
        'User Detail': 'http://django-points-api.herokuapp.com/api/user-detail/<str:pk>/',
        'Payer Detail': 'http://django-points-api.herokuapp.com/api/payer-detail/<str:pk>/',
        'Balance Detail': 'http://django-points-api.herokuapp.com/api/balance-detail/<str:pk>/',
        'Transaction Detail': 'http://django-points-api.herokuapp.com/api/transaction-detail/<str:pk>/',
        'FundQueue Detail': 'http://django-points-api.herokuapp.com/api/fund-detail/<str:pk>/',
        'Filters':'',
        'Balance Filter': 'http://django-points-api.herokuapp.com/api/balance-filter/<str:pk>',
        'Transaction Filter': 'http://django-points-api.herokuapp.com/api/transaction-filter/<str:pk>',
        'FundQueue Filter': 'http://django-points-api.herokuapp.com/api/fund-filter/<str:pk>',
        'Main Functionality': '',
        'Create' : 'http://django-points-api.herokuapp.com/api/create/',
        'Deduct': 'http://django-points-api.herokuapp.com/api/deduct/',
    }
    return Response(api_urls)

@api_view(['GET'])
def allFields(request):
    user = get_list_or_404(User)
    user_serializer = UserSerializer(user, many=True)
    payer = get_list_or_404(Payer)
    payer_serializer = PayerSerializer(payer, many=True)
    balance = get_list_or_404(Balance)
    balance_serializer = BalanceSerializer(balance, many=True)
    transaction = get_list_or_404(Transaction)
    transaction_serializer = TransactionSerializer(transaction, many=True)
    fundqueue = get_list_or_404(FundQueue)
    fundqueue_serializer = FundQueueSerializer(fundqueue, many=True)
    return Response([user_serializer.data,
                    payer_serializer.data,
                    balance_serializer.data,
                    transaction_serializer.data,
                    fundqueue_serializer.data,], status=200)

class User_API:
    @api_view(['GET'])
    def userList(request):
        user = get_list_or_404(User)
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data,status=200)
    @api_view(['GET'])
    def userDetail(request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data,status=200)

class Payer_API:
    @api_view(['GET'])
    def payerList(request):
        payer = get_list_or_404(Payer)
        serializer = PayerSerializer(payer, many=True)
        return Response(serializer.data,status=200)
    @api_view(['GET'])
    def payerDetail(request, pk):
        payer = get_object_or_404(Payer, pk=pk)
        serializer = PayerSerializer(payer, many=False)
        return Response(serializer.data,status=200)

class Balance_API:
    @api_view(['GET'])
    def balanceList(request):
        balance = get_list_or_404(Balance)
        serializer = BalanceSerializer(balance, many=True)
        return Response(serializer.data,status=200)
    @api_view(['GET'])
    def balanceDetail(request, pk):
        balance = get_object_or_404(Balance, pk=pk)#Balance.objects.get(id=pk)
        serializer = BalanceSerializer(balance, many=False)
        return Response(serializer.data,status=200)
    @api_view(['GET'])
    def balanceFilter(request, pk):
        u = get_object_or_404(User, name=pk)
        balance = get_list_or_404(Balance, user=u)#Balance.objects.get(id=pk)
        serializer = BalanceSerializer(balance, many=True)
        return Response(serializer.data, status=200)

class Transaction_API:
    @api_view(['GET'])
    def transactionList(request):
        transaction = get_list_or_404(Transaction)
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data,status=200)
    @api_view(['GET'])
    def transactionDetail(request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)#Transaction.objects.get(id=pk)
        serializer = TransactionSerializer(transaction, many=False)
        return Response(serializer.data,status=200)
    @api_view(['GET'])
    def transactionFilter(request, pk):
        u = get_object_or_404(User, name=pk)
        transaction = get_list_or_404(Transaction, user=u)#Transaction.objects.get(id=pk)
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data, status=200)

    @api_view(['POST'])
    def transactionCreate(request):
        serializer = TransactionSerializer(data = request.data)
        #makes account and payer if they do not exist
        t =TransactionManager()
        t.incaseDNE(serializer)

        if serializer.initial_data['points'] <= 0:
            return Response({'Error: Create only takes positive values.'}, status=400)

        if serializer.is_valid():
            serializer.save()
            if DEBUG: print('success')
            return Response(serializer.data, status=201)
        else:
            if DEBUG: print(serializer.errors)

        return Response(serializer.errors, status=400)

    @api_view(['POST'])
    def transactionDeduct(request):
        serializer = TransactionSerializer(data = request.data)
        t =TransactionManager()
        #Could be done with validation but this is simpler for now.
        user =User.objects.get(name=serializer.initial_data['user'])
        if not user:
            return Response({'Error: User does not exist.'}, status=400)
        if serializer.initial_data['points'] >= 0:
            return Response({'Error: Deduct only takes negative values.'}, status=400)
        print(serializer.initial_data['points'], user.getBalance())
        if -serializer.initial_data['points'] > user.getBalance():
            return Response({'Error: Not enough funds to deduct this amount of points.'}, status=400)
        spent = t.deductTransaction(serializer.initial_data)
        print(spent)

        return Response(spent, status=200)

class FundQueue_API:
    @api_view(['GET'])
    def fundQueueList(request):
        fundQueue = get_list_or_404(FundQueue)
        serializer = FundQueueSerializer(fundQueue, many=True)
        return Response(serializer.data,status=200)
    @api_view(['GET'])
    def fundQueueDetail(request, pk):
        fundQueue = get_object_or_404(FundQueue, pk=pk)#FundQueue.objects.get(id=pk)
        serializer = FundQueueSerializer(fundQueue, many=False)
        return Response(serializer.data,status=200)
    @api_view(['GET'])
    def fundQueueFilter(request, pk):
        u = get_object_or_404(User, name=pk)
        fundQueue = get_list_or_404(FundQueue, user=u)#FundQueue.objects.get(id=pk)
        serializer = FundQueueSerializer(fundQueue, many=True)
        return Response(serializer.data, status=200)








#
# @api_view(['GET'])
# def userInfo_Balances(request):
#     # returning payers
#     user = User.objects.get(name=request.data['user'])
#     if not user:
#         return Response({'Error: User does not exist.'}, status=400)
#     users_balances = get_list_or_404(Balance, user=user)
#     # payers = Balance.objects.all().filter(user=user)
#     users_balances = BalanceSerializer(users_balances, many=True)
#     return Response(users_balances.data, status=201)
#
# @api_view(['GET'])
# def userInfo(request):
#     # returning payers
#     user = User.objects.get(name=request.data['user'])
#     if not user:
#         return Response({'Error: User does not exist.'}, status=400)
#
#     transaction = get_list_or_404(Transaction, user=user)  # Transaction.objects.get(id=pk)
#     serializer = TransactionSerializer(transaction, many=True)
#     users_balances = get_list_or_404(Balance, user=user)
#     # balances = Balance.objects.all().filter(user=user)
#     users_balances = BalanceSerializer(users_balances, many=True)
#
#     return Response(users_balances.data, status=201)