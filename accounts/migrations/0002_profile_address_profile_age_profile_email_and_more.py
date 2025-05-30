# Generated by Django 5.2.1 on 2025-05-27 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.IntegerField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='first_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.IntegerField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='whatsapp_number',
            field=models.IntegerField(max_length=15, null=True),
        ),
    ]
