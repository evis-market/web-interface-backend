from django.db import models


class CategoryManager(models.Manager):

    def get_all_children(self, pk):
        category = self.model.objects.get(pk=pk)
        return category.get_descendants()
