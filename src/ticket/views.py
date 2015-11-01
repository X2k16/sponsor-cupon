# encoding=utf-8

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.views import login as django_login

from ticket.forms import AuthenticationForm


def index(request):
    return redirect("login")


def login(request):
    return django_login(request, "login.html", authentication_form=AuthenticationForm)
