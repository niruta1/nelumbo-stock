# Generated by Django 3.2.6 on 2023-05-14 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0059_alter_medicine_valid_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='remarks',
            field=models.CharField(blank='True', max_length=100, null='True'),
            preserve_default='True',
        ),
    ]
