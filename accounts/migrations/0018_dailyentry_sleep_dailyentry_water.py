# Generated by Django 5.2.1 on 2025-07-17 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailyentry',
            name='sleep',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='dailyentry',
            name='water',
            field=models.PositiveBigIntegerField(blank=True, null=True),
        ),
    ]
