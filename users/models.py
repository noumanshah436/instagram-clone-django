from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    # make one to one relationship b/w Profile and User Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="avatar.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self):
        super().save()  # run save method the parent class
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            """ override the resized image and saved it in the file path"""
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
