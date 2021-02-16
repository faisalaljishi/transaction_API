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

DEBUG = 0
# Create your views here.
@api_view(['GET'])
def overview(request):
    api_urls = {
        'All Fields': 'http://127.0.0.1:8085/api/all/',
        'Transaction List':'http://127.0.0.1:8085/api/transactions/',
        'Transaction Detail View': 'http://127.0.0.1:8085/api/transaction-detail/<str:pk>/',
        #'Filter': 'http://127.0.0.1:8085/api/transaction-filter/<str:user>',
        'Create' : 'http://127.0.0.1:8085/api/transaction-create/',
        'Deduct': 'http://127.0.0.1:8085/api/transaction-deduct/',
        # 'Detail': 'http://127.0.0.1:8085/api/payers',
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
    # @api_view(['GET'])
    # def transactionFilter(request, user):
    #     u = user.get_object_or_404(name=user)
    #     transaction = get_list_or_404(Transaction, user=u)#Transaction.objects.get(id=pk)
    #     serializer = TransactionSerializer(transaction, many=True)
    #     return Response(serializer.data, status=200)

    @api_view(['POST'])
    def transactionCreate(request):
        serializer = TransactionSerializer(data = request.data)
        #makes account and payer if they do not exist
        t =TransactionManager()
        t.incaseDNE(serializer)

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
        #makes account and payer if they do not exist
        t =TransactionManager()
        # t.incaseDNE(serializer)
        t.deductTransaction(serializer.initial_data)

        serializer.is_valid()
        return Response(serializer.data, status=201)

