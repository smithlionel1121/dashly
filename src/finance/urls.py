from django.urls import re_path
from .views import dash, dash_ajax

urlpatterns = [
 re_path('^_dash-', dash_ajax),
 re_path('^', dash),
]