from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[
        ('user', 'User'),
        ('trainer', 'Trainer'),
        ('admin', 'Admin')
    ])
    username = models.CharField(max_length=200,null=True)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    age = models.IntegerField(max_length=3,null=True)
    gender = models.CharField(max_length=10, null=True,choices=[
        ('male', 'Male'),
        ('female', 'Female'),
    ])
    phone_number = models.IntegerField(max_length=15,null=True)
    whatsapp_number = models.IntegerField(max_length=15,null=True)
    email = models.CharField(max_length=200,null=True)
    address = models.CharField(max_length=200,null=True)
    def __str__(self):
        return f"{self.user.username} - {self.role}"
