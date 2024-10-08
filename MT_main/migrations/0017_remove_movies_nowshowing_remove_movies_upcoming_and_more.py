# Generated by Django 5.1 on 2024-08-24 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MT_main', '0016_remove_movies_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movies',
            name='nowshowing',
        ),
        migrations.RemoveField(
            model_name='movies',
            name='upcoming',
        ),
        migrations.AddField(
            model_name='screening',
            name='nowshowing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='screening',
            name='upcoming',
            field=models.BooleanField(default=False),
        ),
    ]
