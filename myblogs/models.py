from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()  
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='posts')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Comment(models.Model):
    title = models.CharField(max_length=50)
    author_name = models.ForeignKey(User, on_delete=models.CASCADE)
    author_email = models.EmailField(max_length=100)
    content = models.TextField()
    
    
    
class Profile(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='profile_images/',blank=True,null = True)
    bio = HTMLField()