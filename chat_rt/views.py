from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import GroupMessage, ChatGroup
# Create your views here.
@login_required(login_url='login')
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='private_chat')
    messages = chat_group.chat_messages.all()
    user = request.user
    context = {
        'messages': messages,
        'user': user,
    }
    return render(request, 'chat_rt/chat.html' , context)