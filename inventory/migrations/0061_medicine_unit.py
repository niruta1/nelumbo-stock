# Generated by Django 3.2.6 on 2023-05-14 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0060_medicine_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='unit',
            field=models.CharField(choices=[('pcs', 'pcs'), ('pc', 'pc'), ('box', 'box')], max_length=100, null=True),
        ),
    ]
