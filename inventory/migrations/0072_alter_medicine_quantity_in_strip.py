# Generated by Django 3.2.6 on 2023-06-12 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0071_rename_quantity_instrip_medicine_quantity_in_strip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='quantity_in_strip',
            field=models.IntegerField(default=0),
        ),
    ]
