from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from .models import ChatGroup
from .forms import MessageForm

@login_required(login_url='login')
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='private_chat')
    messages = chat_group.chat_messages.all()
    user = request.user
    form = MessageForm()

    if request.htmx:
        form = MessageForm(request.POST)
        if form.is_valid():
            Message = form.save(commit=False)
            Message.author = request.user.profile
            Message.group = chat_group
            Message.save()
            return render(request, 'chat_rt/partials/chat_message_p.html', {
                'message': Message,
                'user': user,
            })
        
        return HttpResponse("")  

    context = {
        'messages': messages,
        'user': user,
        'form': form,
    }
    return render(request, 'chat_rt/chat.html', context)