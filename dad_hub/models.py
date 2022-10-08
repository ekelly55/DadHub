from django.db import models

# Create your models here.
# we'll need blurbs, profile, response

class Blurb(models.Model):
    name = models.CharField(max_length=250)
    #user = models.CharField(max_length=250)
    content = models.TextField(max_length=1000)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name