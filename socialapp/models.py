from distutils.command.upload import upload
from email.mime import image
from email.policy import default
from enum import auto
from turtle import title
from django.db import models
from django.db.models import Count

# Create your models here.

from django.contrib.auth.models import User
from django.forms import CharField

class Posts(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    # description=models.CharField(max_length=200)
    date=models.DateField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name="like")

    @property
    def fetch_comments(self):
        comment=self.comments_set.all().annotate(up_count=Count('like')).order_by('-like')
        return comment

    def __str__(self):
        return self.title

class Comments(models.Model):
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name="likes")
    def __str__(self):
        return self.comment

class UserProfile(models.Model):
    profile_pic=models.ImageField(upload_to="images",null=True,blank=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(max_length=150)
    phone=models.PositiveIntegerField()
    bio=models.CharField(max_length=120)
    profession=models.CharField(max_length=100)

    
