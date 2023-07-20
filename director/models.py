from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from location_field.models.plain import PlainLocationField


# Create your models here.

class CameraModel(models.Model):
    camera_name = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    location = PlainLocationField(based_fields=['city'], zoom=10)
    web_address = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.camera_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.web_address)
        super().save(*args, **kwargs)

