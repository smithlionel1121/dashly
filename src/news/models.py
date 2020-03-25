from django.db import models

from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save

# Create your models here.
from datetime import datetime

User = get_user_model()

class Story(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(default='C:/Users/footb/Desktop/Coding/dashly/src/news/static/the-onion-logo.jpg')
    url = models.TextField()

    def __str__(self):
        return self.title
    

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_scrape = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}-{}".format(self.user,self.last_scrape)

def post_user_signup_receiver(sender, instance, **kwargs):
	userprofile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(post_user_signup_receiver, sender=User)