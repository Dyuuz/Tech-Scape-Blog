from datetime import timedelta
from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from Blog import settings

# Create your models here.
class Client(AbstractUser):
    account_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, default='Welcome')
    image = models.ImageField(default='test.jpg', blank=True)
    # slug = models.SlugField()

    def __str__(self) -> None:
        return self.name

class Newsletter(models.Model):
    subscribe = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subscribe_list', on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, default='empty')
    
    def __str__(self) -> None:
        return self.user.username
    
class Blog(models.Model):
    title = models.CharField(max_length=75)
    username = models.CharField(max_length=20, default='anon', null=True)
    body = models.TextField()
    slug = models.SlugField()
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(default='test.jpg', blank=True)
    dp = models.ImageField(default='test.jpg', blank=True)
    likes = models.ManyToManyField(User, related_name='like_post', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmark_post', blank=True)
    dislikes = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)
    mins_read = models.IntegerField(default=5)
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE, default=2)
    
    def __str__(self):
        return self.title

class Comments(models.Model):
    name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Blog,  related_name='comms', on_delete=models.CASCADE, default=0)
    # slug = models.SlugField()

    def __str__(self) -> None:
        return self.name
    
class PasswordReset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='token_list', on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    time = models.DateTimeField(auto_now_add=True)
    
    def is_valid(self):
        # Token expires after 15 minutes
        return self.time + timedelta(minutes=15) > timezone.now()
    
    def __str__(self):
        return f"{self.user.username} - {self.token}"