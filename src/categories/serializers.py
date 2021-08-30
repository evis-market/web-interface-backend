from rest_framework import serializers

from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'parent_id', 'name', 'descr', 'logo_url', 'slug', 'sort_id']
