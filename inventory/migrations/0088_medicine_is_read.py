# Generated by Django 4.2.2 on 2023-07-17 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0087_delete_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
