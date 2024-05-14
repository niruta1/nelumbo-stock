# Generated by Django 4.2.2 on 2023-07-19 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0096_alter_staffleave_leave_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffleave',
            name='leave_type',
            field=models.CharField(choices=[('ANNUAL_LEAVE', 'annual'), ('SICK_LEAVE', 'sick'), ('LIEU_LEAVE', 'lieu')], max_length=100),
        ),
    ]
