from django.db import models
from accounts.models import Profile
import shortuuid

# Create your models here.
class ChatGroup(models.Model):
    
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid )
    members = models.ManyToManyField(Profile, related_name="chat_group",blank=True)
    def __str__(self):
        return self.group_name

class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} : {self.body}"
    
    class Meta:
        ordering = ['created']

        