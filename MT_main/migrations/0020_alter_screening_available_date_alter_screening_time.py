# Generated by Django 5.1 on 2024-08-25 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MT_main', '0019_alter_movies_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screening',
            name='available_date',
            field=models.ManyToManyField(blank=True, null=True, to='MT_main.showdate'),
        ),
        migrations.AlterField(
            model_name='screening',
            name='time',
            field=models.ManyToManyField(blank=True, null=True, to='MT_main.showtime'),
        ),
    ]
