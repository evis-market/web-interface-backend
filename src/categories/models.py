import mptt.models as mptt_models
from django.db import models
from django.utils.text import slugify

from categories.managers import CategoryManager


class Category(mptt_models.MPTTModel):
    name = models.CharField('Name', max_length=190, db_index=True, unique=True)
    slug = models.SlugField('Slug', max_length=190, blank=True, db_index=True, unique=True)
    sort_id = models.PositiveIntegerField('Ordering', blank=True, default=2147483647)
    parent = mptt_models.TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    objects = CategoryManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
            super().save(*args, **kwargs)

    def get_all_children(self):
        children = [self]
        try:
            child_list = self.children.all()
        except AttributeError:
            return children
        for child in child_list:
            children.extend(child.get_all_children())
        return children

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'
        ordering = ('sort_id', 'name')
