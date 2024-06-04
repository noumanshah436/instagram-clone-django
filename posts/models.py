from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timesince import timesince
from django.utils import timezone


# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=200, blank=False)
    img = models.ImageField(upload_to="posts/")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Post of {self.author.username}"

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("posts:post-detail", kwargs={"pk": self.pk})

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     im = Image.open(self.post_img.path)
    #     print(im.size)
    #     if im.height > 300:
    #         newsize = (int(im.width/4), int(im.height/4))
    #         img = im.resize(newsize)
    #         img.save(self.post_img.path)


class Comment(models.Model):
    content = models.CharField(max_length=200, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-created_at"]

    def time_diff(self):
        now = timezone.now()
        return f"{timesince(self.created_at, now)} ago"
