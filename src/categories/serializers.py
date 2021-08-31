from rest_framework import serializers

from categories.models import Category, RecommendedFor


class RecommendedForSerializer(serializers.ModelSerializer):
    def to_representation(self, value):
        return value.for_whom

    class Meta:
        model = RecommendedFor
        fields = ['for_whom']


class CategorySerializer(serializers.ModelSerializer):
    recommended_for = RecommendedForSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = ['id', 'parent_id', 'name', 'descr', 'logo_url', 'slug', 'sort_id', 'recommended_for']
