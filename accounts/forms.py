from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
