from datetime import timedelta
from django.utils import timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Client(AbstractUser):
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(max_length=500, default='Welcome')
    image = CloudinaryField('image')
    dp = CloudinaryField('image', default="project-management_gqhk75")
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
    body = CKEditor5Field("Body", config_name="default")
    slug = models.SlugField(max_length=255,unique=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image')
    dp = CloudinaryField('image')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post', blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmark_post', blank=True)
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
    
class VerifyUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.token)
    
    def activate_verification(self):
        self.user.is_verified = True
        self.user.save()
