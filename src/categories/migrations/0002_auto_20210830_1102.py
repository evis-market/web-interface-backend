# Generated by Django 3.2.6 on 2021-08-30 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='descr',
            field=models.TextField(blank=True, default='', verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='category',
            name='logo_url',
            field=models.URLField(blank=True, default='', verbose_name='Logo URL'),
        ),
    ]