# Generated by Django 3.2.6 on 2023-05-11 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0058_auto_20230511_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='valid_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
