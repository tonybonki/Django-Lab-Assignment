# Generated by Django 4.2.5 on 2023-10-02 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mikeshop', '0003_product_on_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='on_sale',
        ),
    ]