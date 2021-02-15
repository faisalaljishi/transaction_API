from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Transaction, Payer, FundQueue
from .serializers import TransactionSerializer, PayerSerializer
from .db_manipulation import TransactionManager

# Create your views here.
@api_view(['GET'])
def overview(request):
    api_urls = {
        'List': 'http://127.0.0.1:8085/api/transactions/',
        'Detail': 'http://127.0.0.1:8085/api/transactions/<str:pk>/',
        # 'List':'http://127.0.0.1:8085/api/transaction-list/',
        # 'Detail View' : 'http://127.0.0.1:8085/api/transaction-detail/<str:pk>/',
        # 'Create' : 'http://127.0.0.1:8085/api/transaction-create/',
        # 'Update': 'http://127.0.0.1:8085/api/transaction-update/<str:pk>/',
        # 'Delete': 'http://127.0.0.1:8085/api/transaction-delete/<str:pk>/',
    }
    return Response(api_urls)

@csrf_exempt
def transactions_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Transaction.objects.all()
        serializer = TransactionSerializer(snippets, many=True)
        return Response(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
@csrf_exempt
def transactions_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TransactionSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
# class Transactions:
#     @api_view(['GET'])
#     def transactionList(request):
#         transaction = Transaction.objects.all()
#         serializer = TransactionSerializer(transaction, many=True)
#         return Response(serializer.data)
#     @api_view(['GET'])
#     def transactionDetail(request, pk):
#         transaction = Transaction.objects.get(id=pk)
#         serializer = TransactionSerializer(transaction, many=False)
#         return Response(serializer.data)
#
#     @api_view(['POST'])
#     def transactionCreate(request):
#         serializer = TransactionSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#         # print(serializer)
#         # print(serializer.data)
#         t = TransactionManager()
#         t.createTransaction(serializer.data)
#         return Response(serializer.data)
#
#     @api_view(['POST'])
#     def transactionUpdate(request, pk):
#         transaction = Transaction.objects.get(id=pk)
#         serializer = TransactionSerializer(instance=transaction,  data= request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
#     @api_view(['DELETE'])
#     def transactionDelete(request, pk):
#         transaction = Transaction.objects.get(id=pk)
#         transaction.delete()
#         return Response('Item deleted')
#
#
# class Payer:
#     def payerList(request):
#         payers = Payer.objects.all()
#         serializer = PayerSerializer(payers, many=True)
#         return Response(serializer.data)
#     @api_view(['GET'])
#     def payerDetail(request, pk):
#         payer = Payer.objects.get(id=pk)
#         serializer = PayerSerializer(payer, many=False)
#         return Response(serializer.data)
#
#     @api_view(['POST'])
#     def payerCreate(request):
#         serializer = PayerSerializer(data = request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
#
#     @api_view(['POST'])
#     def payerUpdate(request, pk):
#         payer = Payer.objects.get(id=pk)
#         serializer = PayerSerializer(instance=payer,  data= request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
#     @api_view(['DELETE'])
#     def payerDelete(request, pk):
#         payer = Payer.objects.get(id=pk)
#         payer.delete()
#         return Response('Item deleted')
#
