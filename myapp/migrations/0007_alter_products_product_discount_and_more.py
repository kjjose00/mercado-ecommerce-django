# Generated by Django 4.1.6 on 2023-05-10 05:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_discount',
            field=models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='products',
            name='product_image',
            field=models.ImageField(blank=True, upload_to='uploads/'),
        ),
    ]
