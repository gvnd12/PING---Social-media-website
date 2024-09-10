from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
import datetime

mobile_no_validator=RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
now = datetime.datetime.now()
# Create your models here.
class User(AbstractUser):
    profile_pic=models.ImageField(upload_to='images/' ,default='images\default dp.jpg')
    mobile_no=models.CharField(validators=[mobile_no_validator], max_length=17, blank=True)
    date_of_birth=models.DateField(default=None, null=True)
    gender=models.CharField(max_length=10)
    account_privacy=models.CharField(max_length=10, default='Public')

class Post(models.Model):
    Post_description=models.CharField(max_length=100)
    Post_image=models.ImageField(upload_to='post_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

class Pings(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='ping')
    content=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class PingReply(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='replyuser')
    ping=models.ForeignKey(Pings, on_delete=models.CASCADE, related_name='replyping')
    content=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    content=models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Follow(models.Model):
    follower=models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following=models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post= models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)