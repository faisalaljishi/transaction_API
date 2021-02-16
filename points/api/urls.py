from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name='overview'),
    path('all/', views.allFields, name='all'),
]


# transaction
urlpatterns +=[
    path('transactions/', views.Transaction_API.transactionList, name='transactions'),
    path('transaction-detail/<str:pk>/', views.Transaction_API.transactionDetail, name='transaction-detail'),
    path('transaction-create/', views.Transaction_API.transactionCreate, name='transaction-create'),
    path('transaction-deduct/', views.Transaction_API.transactionDeduct, name='transaction-deduct'),
]
# #Payer
# urlpatterns +=[
#     path('payer-list/', views.Payer_API.payerList, name='payer-list'),
#     path('payer-detail/<str:pk>/', views.Payer_API.payerDetail, name='payer-detail'),
#     path('payer-create/', views.Payer_API.payerCreate, name='payer-create'),
#     path('payer-update/<str:pk>/', views.Payer_API.payerUpdate, name='payer-update'),
#     path('payer-delete/<str:pk>/', views.Payer_API.payerDelete, name='payer-delete'),
# ]