# Generated by Django 3.2.6 on 2023-04-26 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0052_out'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('amount_received', models.IntegerField(blank=True, default=0, null=True)),
                ('issued_to', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_price', models.IntegerField(blank=True, default=0, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
            ],
        ),
        migrations.DeleteModel(
            name='Out',
        ),
    ]
