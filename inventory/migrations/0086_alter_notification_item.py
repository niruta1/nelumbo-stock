# Generated by Django 4.2.2 on 2023-07-16 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0085_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item'),
        ),
    ]