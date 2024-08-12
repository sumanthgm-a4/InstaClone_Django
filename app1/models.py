from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user_obj = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="media", null=False)
    caption = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user_obj.username