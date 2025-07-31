# accounts/signals.py

from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.contrib.auth.models import Group
from .models import Profile 

@receiver(user_signed_up)
def handle_user_signup(request, user, **kwargs):

    try:
        # Assign the 'user' group
        group = Group.objects.get(name='user')
        user.groups.add(group)
     
        Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            role=group  
        )

    except Group.DoesNotExist:

        pass