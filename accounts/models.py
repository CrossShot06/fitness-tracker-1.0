from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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
    profile_pic = models.ImageField(default="default.png",null=True,blank=True)
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class TrainerRequest(models.Model):
    STATUS = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    ]
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    message = models.TextField(null=True)
    status = models.CharField(max_length=100,choices=STATUS,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}/5"