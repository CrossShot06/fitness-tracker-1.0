# Generated by Django 5.2.1 on 2025-07-09 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_workouts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workouts',
            old_name='workout_img',
            new_name='workout_image',
        ),
    ]
