from django.db.models import Q

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,  # build custom atributes for User model
)
from django.contrib.auth.models import (
    BaseUserManager,  # to override default user functionality like  while creating superuser.
)
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from MAuthentication.models import User
from timezone_field import TimeZoneField


#Retuen messages by user
class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    #sender
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    #receiver
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    class Meta:
        unique_together = ['first_person', 'second_person']

    def __str__(self):
        return f'S:{self.first_person} | R: {self.second_person}'


#there is a thread in which first_person sends the message and it is recieved by second_person. Both can send message.
class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    #whos sent the message?
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    posted_on =  models.DateTimeField(default=timezone.now)


 #  In home.html line 72
 #  <p>{{ thread.chatmessage_thread.last }} </p>
    def __str__(self):
        return f"{self.message}"

    class Meta:
        ordering =("timestamp",)    
