# Generated by Django 5.1 on 2024-08-21 18:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MT_main', '0004_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='show_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='MT_main.screening'),
        ),
    ]
