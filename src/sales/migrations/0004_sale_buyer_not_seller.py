# Generated by Django 3.2.7 on 2021-10-17 18:39

import django.db.models.expressions
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sales', '0003_auto_20211015_2104'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='sale',
            constraint=models.CheckConstraint(
                check=models.Q(('buyer', django.db.models.expressions.F('seller')), _negated=True),
                name='buyer_not_seller'),
        ),
    ]
