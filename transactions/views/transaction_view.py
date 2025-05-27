from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.db.models import Q
from transactions.serializers.transaction_serializer import *
from transactions.models.transaction import Transaction
from django.core.paginator import Paginator
import datetime
import django.db.models as models

class TransactionAdd(APIView):
    """
    API View for adding a new transaction. Only accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Handle POST request to add a new transaction.
        """
        try:
            serializer = TransactionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({
                    'status': True,
                    'message': 'Transaction added successfully',
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
                'message': 'An error occurred while adding the transaction',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class TransactionList(APIView):
    """
    API View for listing transactions. Accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Handle POST request to list transactions with optional filtering and pagination.
        """
        try:
            search_data = request.data
            page = search_data.get('page')
            page_size = search_data.get('page_size', 10)
            category_id = search_data.get('category', '')
            transaction_date = search_data.get('date', '')
            transaction_type = search_data.get('transaction_type', '')
            amount_min = search_data.get('amount_min', '')
            amount_max = search_data.get('amount_max', '')

            query = Q(user=request.user)
            if category_id:
                query &= Q(category__id=category_id)
            if transaction_date:
                query &= Q(date=transaction_date)
            if transaction_type:
                query &= Q(transaction_type=transaction_type)
            if amount_min and amount_max:
                query &= Q(amount__range=(amount_min, amount_max))

            transactions = Transaction.objects.filter(query).order_by('-created_at')

            if transactions.exists():
                if page is not None:
                    paginator = Paginator(transactions, page_size)
                    paginated_transactions = paginator.get_page(page)
                    serializer = TransactionSerializer(paginated_transactions, many=True)

                    return Response({
                        'status': True,
                        'count': paginator.count,
                        'num_pages': paginator.num_pages,
                        'records': serializer.data
                    }, status=status.HTTP_200_OK)

                else:
                    serializer = TransactionSerializer(transactions, many=True)
                    return Response({
                        'status': True,
                        'count': transactions.count(),
                        'records': serializer.data
                    }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'status': False,
                    'message': 'Transactions not found'
                }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetails(APIView):
    """
    API View for retrieving details of a specific transaction. Only accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Handle POST request to get details of a specific transaction.
        """
        try:
            transaction_id = request.data.get('id')

            if transaction_id:
                transaction = Transaction.objects.filter(id=transaction_id, user=request.user).first()

                if transaction:
                    serializer = TransactionSerializer(transaction)
                    return Response({
                        'status': True,
                        'records': serializer.data
                    }, status=status.HTTP_200_OK)

                else:
                    return Response({
                        'status': False,
                        'message': 'Transaction not found'
                    }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'status': False,
                    'message': 'Please provide transactionId'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': False,
                'message': 'An error occurred while fetching transaction details',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class TransactionUpdate(APIView):
    """
    API View for updating an existing transaction. Only accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        """
        Handle PUT request to update a transaction.
        """
        try:
            transaction_id = request.data.get('id')

            transaction = Transaction.objects.filter(id=transaction_id, user=request.user).first()

            if transaction:
                serializer = TransactionSerializer(transaction, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status': True,
                        'message': 'Transaction updated successfully'
                    }, status=status.HTTP_200_OK)

                return Response({
                    'status': False,
                    'message': 'Invalid data',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': False,
                'message': 'Transaction not found'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'status': False,
                'message': 'An error occurred while updating the transaction',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class TransactionDelete(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, transaction_id):
        try:
            transaction = Transaction.objects.filter(id=transaction_id, user=request.user).first()

            if transaction:
                transaction.soft_delete()
                return Response({
                    'status': True,
                    'message': 'Transaction deleted successfully'
                }, status=status.HTTP_200_OK)

            return Response({
                'status': False,
                'message': 'Transaction not found'
            }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

class FinancialSummary(APIView):
    """
    API View for retrieving financial summary. Accessible by authenticated users.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Handle GET request to retrieve financial summary for the user.
        """
        try:
            transactions = Transaction.objects.filter(user=request.user)
            total_income = transactions.filter(transaction_type='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
            total_expenses = transactions.filter(transaction_type='expense').aggregate(models.Sum('amount'))['amount__sum'] or 0
            balance = total_income - total_expenses

            return Response({
                'status': True,
                'records': {
                    'total_income': total_income,
                    'total_expenses': total_expenses,
                    'balance': balance
                }
            }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)