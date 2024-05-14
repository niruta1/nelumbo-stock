# Generated by Django 3.2.6 on 2023-06-08 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0061_medicine_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='issued_to',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='unit',
            field=models.CharField(choices=[('pcs', 'pcs'), ('pc', 'pc'), ('box', 'box'), ('boxes', 'boxes')], max_length=100, null=True),
        ),
    ]
