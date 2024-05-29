from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # make one to one relationship b/w Profile and User Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="avatar.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"
