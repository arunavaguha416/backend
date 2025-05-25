from rest_framework import serializers
from budgets.models.budget import Budget
from django.utils.translation import gettext_lazy as _

class BudgetSerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta(object):
        model = Budget
        fields = ('id', 'amount', 'month', 'created_at', 'updated_at')