from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,TrainerRequest,Review,StepEntry,Appointments,Workouts,DailyEntry,Target



ROLES = [
    ('user', 'User'),
    ('trainer', 'Trainer'),
    ('admin', 'Admin'),
]

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        }

        fields=['username','email','password1','password2']

class UpdateUserForm(ModelForm):
    
    class Meta:
        model = Profile
        fields = ['username','role','first_name','last_name','age','gender','phone_number','whatsapp_number','email','address','profile_pic']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age'}),
            'phone_number': forms.NumberInput(attrs={'placeholder': 'Phone Number'}),
            'whatsapp_number': forms.NumberInput(attrs={'placeholder': 'WhatsApp Number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
            'gender' : forms.Select(),
            'role': forms.TextInput(attrs={'disabled': 'disabled'}),
        }

class TrainerRequestForm(ModelForm):

    class Meta :
        model = TrainerRequest
        fields = ['message']
        widgets = {
            
            'message': forms.TextInput(attrs={'rows':5,'placeholder':'Why Do You Want To Be A Trainer?'})
        }

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }


class StepEntryForm(forms.ModelForm):
    class Meta:
        model = StepEntry
        fields = ['date', 'steps']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ['start_datetime','end_datetime','description']
        widgets = {
            'start_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class WorkoutForm(forms.ModelForm):
    class Meta:
        model=Workouts
        fields=['trainee','workout_name','workout_image','reps','sets','day']
        widgets = {
            'workout_name': forms.TextInput(attrs={
                'placeholder': 'Enter workout name'
            }),
            'workout_image': forms.ClearableFileInput(attrs={
                'placeholder': 'Upload workout image'
            }),
            'reps': forms.NumberInput(attrs={
                'placeholder': 'Number of reps'
            }),
            'sets': forms.NumberInput(attrs={
                'placeholder': 'Number of sets'
            }),
        }
        
        labels = {
            'trainee': 'Select Trainee',
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['trainee'].queryset=User.objects.filter(profile__role='user')

class DailyEntryForm(forms.ModelForm):
    class Meta:
        model = DailyEntry
        fields = ['calories', 'steps','heartrate']

class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ['calories','steps','water','sleep']