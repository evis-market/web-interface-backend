# Generated by Django 3.2.7 on 2021-09-05 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Data Type',
                'verbose_name_plural': 'Data Types',
                'db_table': 'data_types',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='DataFormat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=190, unique=True, verbose_name='Name')),
                ('data_type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='DataFormat', to='product_data_types.datatype')),
            ],
            options={
                'verbose_name': 'Data Format',
                'verbose_name_plural': 'Data Formats',
                'db_table': 'data_format',
                'ordering': ('name',),
            },
        ),
    ]