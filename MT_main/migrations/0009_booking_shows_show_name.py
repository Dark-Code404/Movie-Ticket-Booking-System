# Generated by Django 5.1 on 2024-08-16 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MT_main', '0008_remove_booking_shows_total_amt'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_shows',
            name='show_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
