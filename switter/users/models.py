from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default_avatar.png', upload_to='profile_images')

    def __str__(self):
        return self.user.username

    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)
        img.thumbnail((250, 250))
        img.save(self.avatar.path)