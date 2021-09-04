from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Transaction, Payer, FundQueue, Balance
from .serializers import TransactionSerializer, PayerSerializer, UserSerializer, BalanceSerializer, FundQueueSerializer
from .db_manipulation import TransactionManager
from points.settings import DEBUG

def home(request):
    return render(request, 'home.html')

# Landing /api/ page
@api_view(['GET'])
def overview(request):
    api_urls = {
        'All Fields': f'http://{domain}/api/all/',
        'Users': '',
        'User List': f'http://{domain}/api/users/',
        'User Detail': f'http://{domain}/api/user-detail/<str:pk>/',
        'Payers': '',
        'Payer List': f'http://{domain}/api/payers/',
        'Payer Detail': f'http://{domain}/api/payer-detail/<str:pk>/',
        'Balances': '',
        'Balance List': f'http://{domain}/api/balances/',
        'Balance Detail': f'http://{domain}/api/balance-detail/<str:pk>/',
        'Balance Filter': f'http://{domain}/api/balance-filter/<str:pk>',
        'Transactions': '',
        'Transaction List': f'http://{domain}/api/transactions/',
        'Transaction Detail': f'http://{domain}/api/transaction-detail/<str:pk>/',
        'Transaction Filter': f'http://{domain}/api/transaction-filter/<str:pk>',
        'Funds':'',
        'FundQueue List': f'http://{domain}/api/funds/',
        'FundQueue Detail': f'http://{domain}/api/fund-detail/<str:pk>/',
        'FundQueue Filter': f'http://{domain}/api/fund-filter/<str:pk>',
        'Main Functionality': '',
        'Create' : f'http://{domain}/api/create/',
        'Deduct': f'http://{domain}/api/deduct/',
    }
    return Response(api_urls)

@api_view(['GET'])
def allFields(request):
    user = User.objects.all()
    user_serializer = UserSerializer(user, many=True)
    payer = Payer.objects.all()
    payer_serializer = PayerSerializer(payer, many=True)
    balance = Balance.objects.all()
    balance_serializer = BalanceSerializer(balance, many=True)
    transaction = Transaction.objects.all()
    transaction_serializer = TransactionSerializer(transaction, many=True)
    fundqueue = FundQueue.objects.all()
    fundqueue_serializer = FundQueueSerializer(fundqueue, many=True)

    respond_list = [user_serializer.data,
                    payer_serializer.data,
                    balance_serializer.data,
                    transaction_serializer.data,
                    fundqueue_serializer.data,]
    allFalse = not any(respond_list)
    if allFalse:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(respond_list, status=200)

class User_API:
    @api_view(['GET'])
    def userList(request):
        print(User)
        user = get_list_or_404(User)
        print(user)
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

        if int(serializer.initial_data['points']) <= 0:
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
        user =User.objects.get(name=serializer.initial_data.get('user'))
        if not user:
            return Response({'Error: User does not exist.'}, status=400)
        if int(serializer.initial_data['points']) >= 0:
            return Response({'Error: Deduct only takes negative values.'}, status=400)
        print(serializer.initial_data['points'], user.getBalance())
        if -int(serializer.initial_data['points']) > user.getBalance():
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
