# Generated by Django 3.2.7 on 2021-10-22 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller_products', '0007_auto_20211015_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerproduct',
            name='price_by_request',
            field=models.BooleanField(blank=True, default=False, verbose_name='Price by request True/False'),
        ),
        migrations.AlterField(
            model_name='sellerproductarchive',
            name='price_by_request',
            field=models.BooleanField(blank=True, default=False, verbose_name='Price by request True/False'),
        ),
    ]