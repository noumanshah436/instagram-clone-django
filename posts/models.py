from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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
