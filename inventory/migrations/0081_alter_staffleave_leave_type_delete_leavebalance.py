# Generated by Django 4.2.2 on 2023-07-11 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0080_alter_staffleave_leave_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffleave',
            name='leave_type',
            field=models.CharField(choices=[('annual leave', 'Annual Leave'), ('sick leave', 'Sick Leave'), ('lieu leave', 'Lieu Leave')], max_length=100),
        ),
        migrations.DeleteModel(
            name='LeaveBalance',
        ),
    ]