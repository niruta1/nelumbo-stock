# Generated by Django 4.0.4 on 2022-06-20 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_camp_department_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('camp_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.camp')),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.department')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.location')),
            ],
        ),
    ]
