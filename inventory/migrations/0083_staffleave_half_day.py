# Generated by Django 4.2.2 on 2023-07-13 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0082_alter_staff_annual_leave_alter_staff_lieu_leave_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffleave',
            name='half_day',
            field=models.BooleanField(default=False),
        ),
    ]
