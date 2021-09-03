# Generated by Django 3.2.6 on 2021-09-03 21:07

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=190, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('logo_url', models.URLField(blank=True, help_text='URL link to logo', max_length=1000, verbose_name='Logo URL')),
                ('wallet_for_payments_erc20', models.CharField(blank=True, max_length=42, verbose_name='ERC-20 wallet')),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5.0)], verbose_name='Rating')),
                ('seller_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Seller', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Sellers',
                'db_table': 'sellers',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.IntegerField(verbose_name='Contact types')),
                ('value', models.CharField(max_length=190, verbose_name='Value')),
                ('comment', models.CharField(blank=True, default='', max_length=190, verbose_name='Comment')),
                ('seller_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Contact', to='sellers.seller')),
            ],
            options={
                'verbose_name_plural': 'Seller contacts',
                'db_table': 'seller_contacts',
                'ordering': ('type_id',),
            },
        ),
    ]
