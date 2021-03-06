# Generated by Django 3.2.7 on 2021-10-15 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller_products', '0007_auto_20211015_2104'),
        ('sales', '0002_auto_20211012_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleproduct',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_product', to='sales.sale'),
        ),
        migrations.AlterField(
            model_name='saleproduct',
            name='seller_product_archive_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sale_product', to='seller_products.sellerproductarchive'),
        ),
    ]
