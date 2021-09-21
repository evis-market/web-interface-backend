from django.db import models


class LanguageManager(models.Manager):
    def get_all(self):
        return self.model.objects.all()
