import mptt.models as mptt_models
from django.db import models
from django.utils.text import slugify

from categories.managers import CategoryManager


class RecommendedFor(models.Model):
    name = models.CharField('For whom is recommended', max_length=120, db_index=True, unique=True)

    class Meta:
        db_table = 'recommended_for'
        verbose_name = 'Recommended for'
        verbose_name_plural = 'Recommended for'

    def __str__(self):
        return self.name


class Category(mptt_models.MPTTModel):
    name = models.CharField('Name', max_length=190, db_index=True, unique=True)
    descr = models.TextField('Description', blank=True, null=False, default='')
    logo_url = models.URLField('Logo URL', blank=True, null=False, default='')
    slug = models.SlugField('Slug', max_length=190, blank=True, db_index=True, unique=True)
    sort_id = models.PositiveIntegerField('Ordering', blank=True, default=2147483647)
    parent = mptt_models.TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    recommended_for = models.ManyToManyField(
        RecommendedFor, blank=True, related_name='categories', verbose_name='For whom category is recommended',
    )
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
            super().save(*args, **kwargs)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('sort_id', 'name')
