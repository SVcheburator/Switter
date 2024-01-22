from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Swits(models.Model):
    text = models.CharField(max_length=1000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    
    def _str_(self):
        return f"{self.text}"
    

# class Likes(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     swit = models.ForeignKey(Swits, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'swit')