from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.db.models import Q
from budgets.serializers.budget_serializer import *
from budgets.models.budget import Budget
from django.core.paginator import Paginator
import datetime

class BudgetAdd(APIView):
    """
    API View for adding a new budget. Only accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Handle POST request to add a new budget.
        """
        try:
            serializer = BudgetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({
                    'status': True,
                    'message': 'Budget added successfully',
                    'records': serializer.data
                }, status=status.HTTP_200_OK)

            return Response({
                'status': False,
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': False,
                'message': 'An error occurred while adding the budget',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class BudgetList(APIView):
    """
    API View for listing budgets. Accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Handle POST request to list budgets with optional filtering and pagination.
        """
        try:
            search_data = request.data
            page = search_data.get('page')
            page_size = search_data.get('page_size', 10)
            search_month = search_data.get('month', '')

            query = Q(user=request.user)
            if search_month:
                query &= Q(month=search_month)

            budgets = Budget.objects.filter(query).order_by('-created_at')

            if budgets.exists():
                if page is not None:
                    paginator = Paginator(budgets, page_size)
                    paginated_budgets = paginator.get_page(page)
                    serializer = BudgetSerializer(paginated_budgets, many=True)

                    return Response({
                        'status': True,
                        'count': paginator.count,
                        'num_pages': paginator.num_pages,
                        'records': serializer.data
                    }, status=status.HTTP_200_OK)

                else:
                    serializer = BudgetSerializer(budgets, many=True)
                    return Response({
                        'status': True,
                        'count': budgets.count(),
                        'records': serializer.data
                    }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'status': False,
                    'message': 'Budgets not found'
                }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

class BudgetDetails(APIView):
    """
    API View for retrieving details of a specific budget. Only accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Handle POST request to get details of a specific budget.
        """
        try:
            budget_id = request.data.get('id')

            if budget_id:
                budget = Budget.objects.filter(id=budget_id, user=request.user).first()

                if budget:
                    serializer = BudgetSerializer(budget)
                    return Response({
                        'status': True,
                        'records': serializer.data
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({
                        'status': False,
                        'message': 'Budget not found'
                    }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'status': False,
                    'message': 'Please provide budgetId'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': False,
                'message': 'An error occurred while fetching budget details',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class BudgetUpdate(APIView):
    """
    API View for updating an existing budget. Only accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        """
        Handle PUT request to update a budget.
        """
        try:
            budget_id = request.data.get('id')

            budget = Budget.objects.filter(id=budget_id, user=request.user).first()

            if budget:
                serializer = BudgetSerializer(budget, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status': True,
                        'message': 'Budget updated successfully'
                    }, status=status.HTTP_200_OK)

                return Response({
                    'status': False,
                    'message': 'Invalid data',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': False,
                'message': 'Budget not found'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': False,
                'message': 'An error occurred while updating the budget',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class BudgetDelete(APIView):
    """
    API View for deleting a budget. Only accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def delete(self, request, budget_id):
        """
        Handle DELETE request to soft delete a budget.
        """
        try:
            budget = Budget.objects.filter(id=budget_id, user=request.user).first()

            if budget:
                budget.soft_delete()
                return Response({
                    'status': True,
                    'message': 'Budget deleted successfully'
                }, status=status.HTTP_200_OK)

            return Response({
                'status': False,
                'message': 'Budget not found'
            }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)