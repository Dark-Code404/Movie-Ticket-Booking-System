# Generated by Django 5.1 on 2024-08-17 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MT_main', '0009_booking_shows_show_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Flims_Details',
            new_name='MovieDetails',
        ),
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('sid', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.IntegerField()),
                ('available_seats', models.IntegerField(default=100)),
                ('available_date', models.ManyToManyField(to='MT_main.showdate')),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cinema_show', to='MT_main.cinemas_details')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movie_show', to='MT_main.moviedetails')),
                ('time', models.ManyToManyField(to='MT_main.showtime')),
            ],
        ),
        migrations.DeleteModel(
            name='Shows_Details',
        ),
    ]
