from django.shortcuts import render, redirect

from .forms import NoteModelForm
from .models import Note

def base(request):
	return render(request, 'notepad/base.html')

from django.urls import path, include

urlpatterns = [
    path('', base, name='base'),
]
