"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from .views import home
from news.views import scrape
from notepad.views import create_view
from finance.views import company_article_list, ChartData, dash, dash_ajax

urlpatterns = [
    path('', include('notepad.base')),
    path('admin/', admin.site.urls),
    path('notes/', include('notepad.urls', namespace='notes')),
    path('scrape/', scrape, name='scrape'),
    path('home/', home, name='home'),
    path('home/create/', create_view, name='home-create'),
    path('companies/', company_article_list, name='companies'),
    path('api/chart/data', ChartData.as_view(), name='api-chart-data'),
    path('dash/', include('finance.urls')),
    # path('accounts/', include('allauth.urls')),
    

    #path('dash/', dash),
    # path('_dash', dash_ajax),
    # path('_dash-layout', dash_ajax), # added
    # path('_dash-dependencies', dash_ajax), # added
    # path('_dash-update-component', dash), # added
    # #path('accounts/', include('allauth.urls')),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)