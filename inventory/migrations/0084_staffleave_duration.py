# Generated by Django 4.2.2 on 2023-07-13 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0083_staffleave_half_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffleave',
            name='duration',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4),
        ),
    ]