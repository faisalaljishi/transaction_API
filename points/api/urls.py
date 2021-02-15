from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name='overview'),
]


#transaction
urlpatterns +=[
path('transaction-list/', views.Transactions.transactionList, name='transaction-list'),
    path('transaction-detail/<str:pk>/', views.Transactions.transactionDetail, name='transaction-detail'),
    path('transaction-create/', views.Transactions.transactionCreate, name='transaction-create'),
    path('transaction-update/<str:pk>/', views.Transactions.transactionUpdate, name='transaction-update'),
    path('transaction-delete/<str:pk>/', views.Transactions.transactionDelete, name='transaction-delete'),
]
#Payer
urlpatterns +=[
    path('payer-list/', views.Payer.payerList, name='payer-list'),
    path('payer-detail/<str:pk>/', views.Payer.payerDetail, name='payer-detail'),
    path('payer-create/', views.Payer.payerCreate, name='payer-create'),
    path('payer-update/<str:pk>/', views.Payer.payerUpdate, name='payer-update'),
    path('payer-delete/<str:pk>/', views.Payer.payerDelete, name='payer-delete'),
]