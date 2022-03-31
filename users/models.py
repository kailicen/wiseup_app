from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    if_private = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f'{self.user.username} Profile'
