# Generated by Django 3.2.6 on 2023-04-26 06:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0055_rename_out_sale'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Sale',
        ),
    ]
