# Generated by Django 3.2.6 on 2023-06-15 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0075_alter_staffleave_to_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annual_leave_balance', models.IntegerField(default=18)),
                ('sick_leave_balance', models.IntegerField(default=12)),
                ('lieu_leave_balance', models.IntegerField(default=3)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.staff')),
            ],
        ),
    ]
