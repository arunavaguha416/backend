from django.urls import path
from budgets.views.budget_view import *

urlpatterns = [
    path('add/', BudgetAdd.as_view(), name='budget-add'),
    path('list/', BudgetList.as_view(), name='budget-list'),
    path('details/', BudgetDetails.as_view(), name='budget-details'),
    path('update/', BudgetUpdate.as_view(), name='budget-update'),
    path('delete/<int:budget_id>/', BudgetDelete.as_view(), name='budget-delete'),
]