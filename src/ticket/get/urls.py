# coding=utf-8
from django.conf.urls import include, url
from ticket.get import views

urlpatterns = [
    url(r'^(?P<token>[^/]+)/$', views.index, name='get_index'),
    url(r'^(?P<token>[^/]+)/download/$', views.download, name='get_ticket'),
]
