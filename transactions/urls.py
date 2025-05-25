from django.urls import path
from transactions.views.transaction_view import *

urlpatterns = [
    path('add/', TransactionAdd.as_view(), name='transaction-add'),
    path('list/', TransactionList.as_view(), name='transaction-list'),
    path('details/', TransactionDetails.as_view(), name='transaction-details'),
    path('update/', TransactionUpdate.as_view(), name='transaction-update'),
    path('delete/<int:transaction_id>/', TransactionDelete.as_view(), name='transaction-delete'),
    path('summary/', FinancialSummary.as_view(), name='financial-summary'),
]