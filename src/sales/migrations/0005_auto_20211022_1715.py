# Generated by Django 3.2.7 on 2021-10-22 17:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_sale_buyer_not_seller'),
    ]
    operations = [
        migrations.DeleteModel(
            name='SaleProduct',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='id',
        ),
        migrations.AlterField(
            model_name='sale',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]
