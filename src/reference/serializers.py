from rest_framework import serializers

from reference.models import GeoRegion


class GeoRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoRegion
        fields = ['id', 'name', 'parent_id', 'iso_code']
