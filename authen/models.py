from django.db import models
from django.contrib.auth.models import User

class ProfilePic(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    pimage = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )