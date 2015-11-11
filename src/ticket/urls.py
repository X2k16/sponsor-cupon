"""ticket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login
from ticket import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^sponsors/$', views.sponsor_list, name='sponsor_list'),
    url(r'^sponsors/add/$', views.sponsor_add, name='sponsor_add'),
    url(r'^sponsors/(\d+)/$', views.sponsor_detail, name='sponsor_detail'),
    url(r'^sponsors/(?P<pk>\d+)/edit/$', views.sponsor_edit, name='sponsor_edit'),
    url(r'^get/', include("ticket.get.urls")),
    url(r'^nativeadmin/', include(admin.site.urls)),
]
