from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,TrainerRequest


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
