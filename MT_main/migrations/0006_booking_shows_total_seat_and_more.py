# Generated by Django 5.1 on 2024-08-16 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MT_main', '0005_booking_shows_cinema_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_shows',
            name='total_seat',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='booking_shows',
            name='total_price',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
