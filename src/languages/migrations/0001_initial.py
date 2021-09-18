# Generated by Django 3.2.7 on 2021-09-18 09:49

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
                ('name_native', models.CharField(db_index=True, max_length=150, unique=True, verbose_name='Native language name')),
                ('name_en', models.CharField(db_index=True, max_length=150, unique=True, verbose_name='Language name in english')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'db_table': 'languages',
                'ordering': ('name_en',),
            },
        ),
    ]
