# Generated by Django 4.0.4 on 2022-07-11 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0042_delete_medicine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=1)),
                ('unit', models.CharField(max_length=100)),
                ('expiry_date', models.DateField()),
                ('days_remaining', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.location')),
            ],
        ),
    ]
