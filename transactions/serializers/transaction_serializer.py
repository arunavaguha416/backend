from rest_framework import serializers
from transactions.models.transaction import Transaction
from django.utils.translation import gettext_lazy as _

class TransactionSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()
    category_name = serializers.CharField(source='category.title', read_only=True)

    class Meta(object):
        model = Transaction
        fields = ('id', 'category', 'category_name', 'amount', 'date', 'description', 'transaction_type', 'created_at', 'updated_at')