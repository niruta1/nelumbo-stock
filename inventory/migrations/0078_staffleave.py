# Generated by Django 4.2.2 on 2023-07-05 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0077_remove_leavebalance_annual_leave_balance_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.CharField(max_length=100)),
                ('to_date', models.CharField(blank=True, max_length=100, null=True)),
                ('leave_type', models.CharField(choices=[('annual', 'Annual Leave'), ('sick', 'Sick Leave'), ('lieu', 'Lieu Leave')], max_length=10)),
                ('reason', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.staff')),
            ],
        ),
    ]