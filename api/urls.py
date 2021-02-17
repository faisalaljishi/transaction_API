from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name='overview'),
    path('all/', views.allFields, name='all'),
]


#Transaction
urlpatterns +=[
    path('transactions/', views.Transaction_API.transactionList, name='transactions'),
    path('transaction-detail/<str:pk>/', views.Transaction_API.transactionDetail, name='transaction-detail'),
    path('transaction-filter/<str:pk>/', views.Transaction_API.transactionFilter, name='transaction-filter'),
    path('create/', views.Transaction_API.transactionCreate, name='create'),
    path('deduct/', views.Transaction_API.transactionDeduct, name='deduct'),
]

#User
urlpatterns +=[
    path('users/', views.User_API.userList, name='users'),
    path('user-detail/<str:pk>/', views.User_API.userDetail, name='user-detail'),
]

#Payer
urlpatterns +=[
    path('payers/', views.Payer_API.payerList, name='payers'),
    path('payer-detail/<str:pk>/', views.Payer_API.payerDetail, name='payer-detail'),
]

#Balance
urlpatterns +=[
    path('balances/', views.Balance_API.balanceList, name='balances'),
    path('balance-detail/<str:pk>/', views.Balance_API.balanceDetail, name='balance-detail'),
    path('balance-filter/<str:pk>/', views.Balance_API.balanceFilter, name='balance-filter'),
]

#FundQueue
urlpatterns +=[
    path('funds/', views.FundQueue_API.fundQueueList, name='funds'),
    path('fund-detail/<str:pk>/', views.FundQueue_API.fundQueueDetail, name='fund-detail'),
    path('fund-filter/<str:pk>/', views.FundQueue_API.fundQueueFilter, name='fund-filter'),
]