# Generated by Django 4.0.4 on 2022-07-18 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0047_medicine_item'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Medicine',
        ),
    ]