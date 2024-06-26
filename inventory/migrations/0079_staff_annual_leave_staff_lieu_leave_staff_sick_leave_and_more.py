# Generated by Django 4.2.2 on 2023-07-10 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0078_staffleave'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='annual_leave',
            field=models.FloatField(default=18.0),
        ),
        migrations.AddField(
            model_name='staff',
            name='lieu_leave',
            field=models.FloatField(default=3.0),
        ),
        migrations.AddField(
            model_name='staff',
            name='sick_leave',
            field=models.FloatField(default=12.0),
        ),
        migrations.AlterField(
            model_name='staffleave',
            name='leave_type',
            field=models.CharField(choices=[(12, 'Annual Leave'), (8, 'Sick Leave'), (3, 'Lieu Leave')], max_length=10),
        ),
    ]
