# Generated by Django 5.1.5 on 2025-01-30 08:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg', '0016_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_login_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
