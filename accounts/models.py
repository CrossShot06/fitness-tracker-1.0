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
    
class StepEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    steps = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.steps}"

class Appointments(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('REJECTED', 'Rejected'),
    ]
    trainee = models.ForeignKey(User,on_delete=models.CASCADE,related_name='appointments_as_trainee',)
    trainer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='appointments_as_trainer', )
    created_at = models.DateTimeField(auto_now_add=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDING')
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.trainee.username} → {self.trainer.username} on {self.start_datetime.strftime('%Y-%m-%d %H:%M')}"

class Workouts(models.Model):

    choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ]
 
    trainee = models.ForeignKey(User,on_delete=models.CASCADE,related_name='trainee',)
    trainer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='trainer', )
    created_at = models.DateTimeField(auto_now_add=True)   
    description = models.CharField(max_length=100,null=True)
    workout_name = models.CharField(max_length=100)
    workout_image = models.ImageField(null=True,blank=True)
    reps = models.IntegerField()
    sets = models.IntegerField()
    day = models.CharField(max_length=100,choices=choices,default='Monday')

    def __str__(self):
        return f"{self.trainee.username} → {self.trainer.username} - {self.created_at}"

class DailyEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    calories = models.PositiveIntegerField(null=True, blank=True)
    steps = models.PositiveIntegerField(null=True, blank=True)
    heartrate = models.PositiveBigIntegerField(null=True,blank=True)
    sleep = models.PositiveBigIntegerField(null=True,blank=True)
    water = models.PositiveBigIntegerField(null=True,blank=True)
    workout_data = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Target(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calories = models.PositiveIntegerField(null=True, blank=True)
    steps = models.PositiveIntegerField(null=True, blank=True)
    water = models.PositiveIntegerField(null=True, blank=True)
    sleep = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"      