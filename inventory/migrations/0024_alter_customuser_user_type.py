# Generated by Django 4.0.4 on 2022-06-23 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0023_alter_item_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('1', 'HOD'), ('2', 'CHEE'), ('3', 'DCEC')], default=1, max_length=50),
        ),
    ]