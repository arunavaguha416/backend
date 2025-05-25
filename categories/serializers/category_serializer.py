from rest_framework import serializers
from categories.models.category import Category
from django.utils.translation import gettext_lazy as _

class CategorySerializer(serializers.ModelSerializer):
    created_at = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    class Meta(object):
        model = Category
        fields = ('id', 'title', 'description', 'created_at', 'updated_at', 'published_at')