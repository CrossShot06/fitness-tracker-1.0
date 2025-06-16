from django import forms
from django.forms import ModelForm
from .models import ChatGroup, GroupMessage

class MessageForm(ModelForm):

    class Meta:
        model = GroupMessage
        fields = ["body"]  
        widgets = {
            "body": forms.TextInput(attrs={
                "placeholder": "Enter your message",
                "id": "chat-input",
            }),
        }