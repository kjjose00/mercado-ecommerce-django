# Generated by Django 4.2.1 on 2023-06-15 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_cartcopy'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.TextField(null=True),
        ),
    ]
