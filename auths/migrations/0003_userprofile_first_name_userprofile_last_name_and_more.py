# Generated by Django 5.1 on 2024-08-14 08:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_alter_userprofile_dob'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(blank=True, default='', null=True, upload_to='profile_images/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
