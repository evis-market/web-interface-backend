from django.db import models

from languages.managers import LanguageManager


class Language(models.Model):
    name_native = models.CharField('Native language name', max_length=150, db_index=True, unique=True)
    name_en = models.CharField('Language name in english', max_length=150, db_index=True, unique=True)
    slug = models.SlugField('slug', max_length=150, db_index=True, unique=True)
    objects = LanguageManager()

    def __str__(self):
        return self.name_native

    class Meta:
        db_table = 'languages'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        ordering = ('name_en',)
