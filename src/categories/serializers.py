from rest_framework import serializers

from categories.models import Category, RecommendedFor


class RecommendedForSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendedFor
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    recommended_for = RecommendedForSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['id', 'parent_id', 'name', 'descr', 'logo_url', 'slug', 'sort_id', 'recommended_for']
