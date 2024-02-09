from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


# Profiles
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField('avatar', null=True, blank=True)

    def __str__(self):
        return self.user.username


# Followings
class Followings(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')