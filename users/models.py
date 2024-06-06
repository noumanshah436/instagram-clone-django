from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    # make one to one relationship b/w Profile and User Model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="avatar.png", upload_to="profile_pics")
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

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


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='followed_users', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='following_users', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')

    def __str__(self):
        return f"{self.follower} follows {self.followee}"


# Add the following methods to the User model
def is_following(self, user):
    return Follow.objects.filter(follower=self, followee=user).exists()


def followers(self):  # to get people, that are following us
    return User.objects.filter(followed_users__followee=self)


def followees(self):  # to get people, user is following
    return User.objects.filter(following_users__follower=self)


User.add_to_class("is_following", is_following)
User.add_to_class("followers", followers)
User.add_to_class("followees", followees)
