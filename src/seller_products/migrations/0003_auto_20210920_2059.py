# Generated by Django 3.2.7 on 2021-09-20 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller_products', '0002_auto_20210919_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerproduct',
            name='price_per_usage_descr',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Purchase method description'),
        ),
        migrations.AlterField(
            model_name='sellerproductarchive',
            name='price_per_usage_descr',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Purchase method description'),
        ),
    ]