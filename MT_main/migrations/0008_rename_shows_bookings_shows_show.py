# Generated by Django 5.1 on 2024-08-21 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MT_main', '0007_bookings_shows'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookings',
            old_name='shows',
            new_name='shows_show',
        ),
    ]
