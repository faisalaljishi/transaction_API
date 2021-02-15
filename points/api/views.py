from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Transaction, Payer, FundQueue
from .serializers import TransactionSerializer, PayerSerializer
from .db_manipulation import TransactionManager

DEBUG = 0
# Create your views here.
@api_view(['GET'])
def overview(request):
    api_urls = {
        # 'List': 'http://127.0.0.1:8085/api/all/',
        # 'Detail': 'http://127.0.0.1:8085/api/payers',
        'List':'http://127.0.0.1:8085/api/transactions/',
        'Detail View' : 'http://127.0.0.1:8085/api/transaction-detail/<str:pk>/',
        'Create' : 'http://127.0.0.1:8085/api/transaction-create/',
        'Deduct': 'http://127.0.0.1:8085/api/transaction-deduct/',

    }
    return Response(api_urls)

class Transaction_API:
    @api_view(['GET'])
    def transactionList(request):
        transaction = Transaction.objects.all()
        serializer = TransactionSerializer(transaction, many=True)
        return Response(serializer.data)
    @api_view(['GET'])
    def transactionDetail(request, pk):
        transaction = get_object_or_404(Transaction, pk=pk)#Transaction.objects.get(id=pk)
        serializer = TransactionSerializer(transaction, many=False)
        return Response(serializer.data)

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
        t.incaseDNE(serializer)
        t.deductTransaction(serializer.initial_data)

        serializer.is_valid()
        return Response(serializer.data, status=201)

