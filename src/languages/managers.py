from django.db import models


class LanguageManager(models.Manager):

    def get_all_children(self, pk):
        language = self.model.objects.get(pk=pk)
        return language.get_descendants()
