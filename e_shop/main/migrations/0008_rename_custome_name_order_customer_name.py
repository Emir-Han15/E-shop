# Generated by Django 5.1.1 on 2024-11-10 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='custome_name',
            new_name='customer_name',
        ),
    ]
