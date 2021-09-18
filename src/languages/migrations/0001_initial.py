# Generated by Django 3.2.7 on 2021-09-18 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_native', models.CharField(db_index=True, max_length=150, unique=True, verbose_name='name_native')),
                ('name_en', models.CharField(db_index=True, max_length=150, unique=True, verbose_name='name_en')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='slug')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'db_table': 'languages',
                'ordering': ('name_en',),
            },
        ),
    ]
