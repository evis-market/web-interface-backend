from rest_framework import serializers

from languages.models import Language


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name_native', 'name_en', 'slug']
