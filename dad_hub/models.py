from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# we'll need blurbs, profile, response

class Blurb(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user, self.content

