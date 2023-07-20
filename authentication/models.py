from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
from location_field.models.plain import PlainLocationField
from django.urls import reverse


def path_and_rename(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = f'User_Profile_Pictures/{instance.pk}.{ext}'
    return os.path.join(upload_to, filename)


class Profile(models.Model):
    # creating a relationship with user class (not inheriting)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    company = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    location = PlainLocationField(based_fields=['city'], zoom=7)

    # adding additional attributes
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    photo = models.ImageField(upload_to=path_and_rename, verbose_name="Profile Picture", blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
