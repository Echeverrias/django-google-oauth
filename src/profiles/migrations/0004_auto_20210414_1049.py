# Generated by Django 3.2 on 2021-04-14 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_has_registered_with_this_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_registered_with_this_app',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='has_registered_with_this_app',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
