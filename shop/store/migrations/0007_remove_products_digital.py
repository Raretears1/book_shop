# Generated by Django 3.1.6 on 2021-03-10 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_products_digital'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='digital',
        ),
    ]
