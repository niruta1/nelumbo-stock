# Generated by Django 3.2.6 on 2023-06-12 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0068_rename_medicine_id_dispense_medicine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='location_id',
        ),
        migrations.DeleteModel(
            name='Dispense',
        ),
        migrations.DeleteModel(
            name='Medicine',
        ),
    ]
