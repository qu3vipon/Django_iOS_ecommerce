# Generated by Django 2.2.12 on 2020-04-06 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurly', '0004_auto_20200406_1702'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['-sales', '-discount_rate', '-created_at', '-stock'], name='kurly_produ_sales_5a2953_idx'),
        ),
    ]
