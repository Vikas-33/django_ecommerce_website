# Generated by Django 5.0.7 on 2024-08-09 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0004_product_seller_alter_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_available_count',
        ),
        migrations.AddField(
            model_name='product',
            name='available_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
