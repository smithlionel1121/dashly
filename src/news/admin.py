from django.contrib import admin

# Register your models here.
from .models import Story, UserProfile

admin.site.register(Story)
admin.site.register(UserProfile)