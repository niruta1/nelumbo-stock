# Generated by Django 4.2.2 on 2023-08-01 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0101_alter_dispense_issued_to'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dispense',
            old_name='issued_to',
            new_name='staff_id',
        ),
    ]