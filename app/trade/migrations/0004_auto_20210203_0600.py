# Generated by Django 3.1.5 on 2021-02-03 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0003_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='order',
            name='insert_time',
        ),
        migrations.RemoveField(
            model_name='product',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='product',
            name='insert_time',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='create_time',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='insert_time',
        ),
    ]