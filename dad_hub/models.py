
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField



# Create your models here.
# we'll need blurbs, profile, response

class Blurb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField(max_length=1000)
    image = models.CharField(max_length=200, blank=True, default="")
    link = models.URLField(max_length=200, blank=True, default="")
    tags = ArrayField(models.CharField(max_length=20, blank=True), default=list)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user, self.content, self.id

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    blurb = models.ForeignKey(Blurb, on_delete=models.CASCADE, default=12)
    response = models.ManyToManyField('self')
    content = models.TextField(max_length=1000, default=1)
    def __st__(self):
        return self.user.username, self.content, self.blurb.content

class Bio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default = 1)
    picture = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=20)
    zip = models.CharField(max_length=5)
    kids_ages = ArrayField(models.CharField(max_length=2))
    interests = ArrayField(models.CharField(max_length=20))
    bio = models.TextField(max_length=200)

    def __str__(self):
        return self.user