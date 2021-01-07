from rest_framework import serializers
from .models import CategoryName


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryName
        fields = ['id', 'name']
