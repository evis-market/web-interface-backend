# Generated by Django 3.2.7 on 2021-11-02 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0005_alter_seller_logo_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seller',
            old_name='logo_url',
            new_name='logo',
        ),
    ]