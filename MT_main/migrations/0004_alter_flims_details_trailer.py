# Generated by Django 5.1 on 2024-08-15 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MT_main', '0003_alter_cinemas_details_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flims_details',
            name='trailer',
            field=models.URLField(default='null', max_length=300),
        ),
    ]
