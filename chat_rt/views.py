from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,render,redirect
from django.http import HttpResponse,Http404
from .models import ChatGroup
from accounts.models import Profile
from .forms import MessageForm
from django.urls import reverse

@login_required(login_url='login')
def chat_view(request, chatroom_name):
    chat_group = ChatGroup.objects.get(group_name=chatroom_name)
    messages = chat_group.chat_messages.all()
    user = request.user
    form = MessageForm()

    if request.user.profile not in chat_group.members.all():
        raise Http404
    for member in chat_group.members.all():
        if member!=request.user.profile:
            other_user = member
            break

    context = {
        'messages': messages,
        'user': user,
        'form': form,
        'other_user':other_user,
        'chatroom_name':chatroom_name,
    }
    return render(request, 'chat_rt/chat.html', context)

@login_required(login_url='login')
def get_or_create_chatroom(request,username):
    if request.user.username == username:
        return redirect('login')
    
    other_user = Profile.objects.get(username=username)
    my_chatrooms = request.user.profile.chat_group.all()

    if my_chatrooms.exists():
        for chatroom in my_chatrooms :
            if other_user in chatroom.members.all():
                return redirect(reverse('chatroom', kwargs={'chatroom_name': chatroom.group_name}))
    
    chatroom = ChatGroup.objects.create()
    chatroom.members.add(other_user,request.user.profile)

    return redirect(reverse('chatroom', kwargs={'chatroom_name': chatroom.group_name}))
