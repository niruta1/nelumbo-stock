# Generated by Django 4.0.4 on 2022-06-22 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_delete_item'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_pic', models.ImageField(upload_to='media/item_pic')),
                ('item_name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.department')),
                ('location_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.location')),
                ('purpose', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inventory.purpose')),
            ],
        ),
    ]
