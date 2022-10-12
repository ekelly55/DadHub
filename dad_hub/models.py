
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.
# we'll need blurbs, profile, response

class Blurb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user, self.content, self.id

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    blurb = models.ForeignKey(Blurb, on_delete=models.CASCADE, default=12)
    response = models.ManyToManyField('self')
    content = models.TextField(max_length=1000, default=1)
    def __str__(self):
        return self.user, self.content, self.blurb.content

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    picture = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5)
    children_age = ArrayField(models.CharField(max_length=20))
    interests = ArrayField(models.CharField(max_length=20))
    bio = models.TextField(max_length=300)
    
    def __str__(self):
        return self.user

 
            