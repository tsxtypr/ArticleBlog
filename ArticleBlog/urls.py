"""ArticleBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', views.about),
    path('index/',views.index),
    path('listpic/',views.listpic),
    path('newslistpic/',views.newslistpic),
    re_path('newslistpic/(?P<type>\w+)/(?P<page>\d+)',views.newslistpic),
    path('base',views.base),
    re_path('articledetails/(?P<id>\d+)/',views.articledetails),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('register/',views.register),
    path('login/',views.login),
    path('logout/',views.logout),
    path('admin_base/',views.admin_base),
    path('admin_index/',views.admin_index),
    path('admin_all_article/',views.admin_all_article),
    re_path('admin_all_article/(?P<page>\d+)/',views.admin_all_article),
    path('admin_add/',views.admin_add),
]
