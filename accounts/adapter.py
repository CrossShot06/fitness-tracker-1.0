from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_auto_signup_allowed(self, request, sociallogin):
        print("--- Checking is_auto_signup_allowed ---") 

        return True

    def populate_user(self, request, sociallogin, data):
        print("--- Running populate_user ---") 
        user = super().populate_user(request, sociallogin, data)
        
        email = data.get('email')
        if email:
            username = email.split('@')[0]
            
            original_username = username
            count = 1
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{count}"
                count += 1
            
            print(f"--- Generated username: {username} ---") 
            user.username = username
            
        return user