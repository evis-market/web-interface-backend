from rest_framework import serializers

from geo_regions.models import GeoRegion


class GeoRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoRegion
        fields = ['id', 'name', 'parent_id', 'iso_code']
