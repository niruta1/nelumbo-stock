# Generated by Django 4.0.4 on 2022-07-13 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0045_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category_id',
        ),
        migrations.RemoveField(
            model_name='item',
            name='department_id',
        ),
        migrations.RemoveField(
            model_name='item',
            name='purpose_id',
        ),
        migrations.DeleteModel(
            name='Medicine',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]