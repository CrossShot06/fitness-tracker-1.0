from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


ROLES = [
    ('user', 'User'),
    ('trainer', 'Trainer'),
    ('admin', 'Admin'),
]

class CreateUserForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLES, widget=forms.Select(attrs={
        'placeholder': 'I am a…'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        }

        fields=['username','email','role','password1','password2']

class UpdateUserForm(ModelForm):
    
    class Meta:
        model = Profile
        fields = ['username','role','first_name','last_name','age','gender','phone_number','whatsapp_number','email','address']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'age': forms.NumberInput(attrs={'placeholder': 'Age'}),
            'phone_number': forms.NumberInput(attrs={'placeholder': 'Phone Number'}),
            'whatsapp_number': forms.NumberInput(attrs={'placeholder': 'WhatsApp Number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
            'role': forms.TextInput(attrs={'placeholder': 'Role'}),
        }