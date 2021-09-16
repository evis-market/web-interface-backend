from django.db import models
from mptt.managers import TreeManager


class CategoryManager(TreeManager):

    def get_all_children(self, pk):
        category = self.model.objects.get(pk=pk)
        return category.get_descendants()
