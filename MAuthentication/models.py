from distutils.command.upload import upload
from email.policy import default
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,  # build custom atributes for User model
)
from django.contrib.auth.models import (
    BaseUserManager,  # to override default user functionality like  while creating superuser.
)
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class User(AbstractUser):
    image = models.ImageField(upload_to='userprofiles', default='images/profile.png')
    is_email_verified = models.BooleanField(default=False)
    address = models.CharField(max_length=50, null=True, blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self):
        return reverse("user-detail-view", kwargs={"pk": self.id})

