# Generated by Django 3.2.7 on 2021-10-15 21:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller_products', '0006_auto_20211007_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerproduct',
            name='price_by_request',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Price by request'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='price_per_month',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Price per month'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='price_per_one_time',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Price per one time usage'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='price_per_usage',
            field=models.BooleanField(blank=True, default=0, verbose_name='Price per usage True/False'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='price_per_usage_descr',
            field=models.TextField(blank=True, default=0, verbose_name='Purchase method description'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='price_per_year',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Price per year'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='rating',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='sellerproduct',
            name='total_reviews_cnt',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Total count of reviews'),
        ),
        migrations.AlterField(
            model_name='sellerproductarchive',
            name='price_by_request',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Price by request'),
        ),
        migrations.AlterField(
            model_name='sellerproductarchive',
            name='price_per_month',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Price per month'),
        ),
        migrations.AlterField(
            model_name='sellerproductarchive',
            name='price_per_one_time',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Price per one time usage'),
        ),
        migrations.AlterField(
            model_name='sellerproductarchive',
            name='price_per_usage',
            field=models.BooleanField(blank=True, default=0, verbose_name='Price per usage True/False'),
        ),
        migrations.AlterField(
            model_name='sellerproductarchive',
            name='price_per_usage_descr',
            field=models.TextField(blank=True, default=0, verbose_name='Purchase method description'),
        ),
        migrations.AlterField(
            model_name='sellerproductarchive',
            name='price_per_year',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Price per year'),
        ),
        migrations.AlterField(
            model_name='sellerproductarchive',
            name='rating',
            field=models.FloatField(blank=True, default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='sellerproductarchive',
            name='total_reviews_cnt',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0.0)], verbose_name='Total count of reviews'),
        ),
    ]