# Generated by Django 4.2.13 on 2024-07-05 15:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_order_estimated_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='estimated_delivery_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
