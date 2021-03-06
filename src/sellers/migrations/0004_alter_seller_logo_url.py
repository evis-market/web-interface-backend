# Generated by Django 3.2.7 on 2021-10-27 07:05

import django.core.validators
from django.db import migrations, models
from django.db.transaction import atomic

from sellers.models import Seller


"""
Note: Migrations includes data migration that set to null logo_url field for currently existing records.  
Logo_url field would be change to FileField type in this migration

"""


def clear_seller_logo_url(apps, schema_editor):
    with atomic():
        for seller in Seller.objects.all():
            seller.logo_url = None
            seller.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0003_auto_20211012_1929'),
    ]

    operations = [
        migrations.RunPython(clear_seller_logo_url, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='seller',
            name='logo_url',
            field=models.FileField(blank=True, help_text='Logo', max_length=1000, null=True, upload_to='', verbose_name='Logo'),
        ),
    ]
