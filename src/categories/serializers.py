from rest_framework import serializers

from categories.models import Category, RecommendedFor


class RecommendedForSerializer(serializers.ModelSerializer):
    """ Class representing recommendation for serializer """
    class Meta:
        """ Meta class for class representing recommendation for serializer

        Attributes:
            model (models.Model): data model
            fields (list): class fields list
        """
        model = RecommendedFor
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    """ Class representing category serializer

    Attributes:
        recommended_for (serializers.ModelSerializer): recommendation for serializer
    """
    recommended_for = RecommendedForSerializer(read_only=True, many=True)

    class Meta:
        """ Meta class for class representing category serializer

        Attributes:
            model (models.Model): data model
            fields (list): class fields list
        """
        model = Category
        fields = ['id', 'parent_id', 'name', 'descr', 'logo_url', 'slug', 'sort_id', 'recommended_for']
