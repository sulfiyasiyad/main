# Generated by Django 4.2.13 on 2024-07-05 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_remove_order_estimated_delivery_date_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Order',
            new_name='Orders',
        ),
    ]
