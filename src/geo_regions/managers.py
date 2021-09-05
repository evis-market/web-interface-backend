from django.db import models


class GeoRegionManager(models.Manager):

    def get_all_children(self, pk):
        geo_region = self.model.objects.get(pk=pk)
        return geo_region.get_descendants()
