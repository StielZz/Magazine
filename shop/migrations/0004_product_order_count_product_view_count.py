# Generated by Django 4.2.1 on 2023-05-07 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_product_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='order_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
