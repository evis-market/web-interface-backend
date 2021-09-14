import mptt.models as mptt_models
from django.db import models
from django.utils.text import slugify

from languages.managers import LanguageManager


class Language(mptt_models.MPTTModel):
    name_native = models.CharField('name_native', max_length=150, db_index=True, unique=True)
    name_en = models.CharField('name_en', max_length=150, db_index=True, unique=True)
    slug = models.SlugField('slug', max_length=150, db_index=True, unique=True)
    objects = LanguageManager()

    def __str__(self):
        return self.name_native

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'languages'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        ordering = ('name_en',)
