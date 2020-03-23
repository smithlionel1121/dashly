from django.urls import path, include

from . import views

app_name="notepad"

urlpatterns = [
    path('create/', views.create_view, name='create'),
    path('list/', views.list_view, name='list'),
    path('<id>/delete/', views.delete_view, name='delete'),
    path('<id>/update/', views.update_view, name='update'),
]
