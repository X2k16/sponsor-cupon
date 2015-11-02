# encoding=utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView

from django.contrib.auth.views import login as django_login

from ticket.forms import AuthenticationForm
from ticket.forms import SponsorCreateForm, SponsorUpdateForm
from ticket.models import Sponsor


def index(request):
    if request.user.is_authenticated():
        return redirect("sponsor_list")
    return redirect("login")


def login(request):
    return django_login(request, "login.html", authentication_form=AuthenticationForm)


def sponsor_list(request):
    sponsors = Sponsor.objects.all()
    context = {
        "sponsors": sponsors
    }
    return render(request, "sponsor_list.html", context)


def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, id=pk)
    context = {
        "sponsor": sponsor
    }
    return render(request, "sponsor_detail.html", context)


class SponsorCreateFormView(CreateView):
    template_name = 'sponsor_form.html'
    form_class = SponsorCreateForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SponsorUpdateFormView(UpdateView):
    model = Sponsor
    template_name = 'sponsor_form.html'
    form_class = SponsorUpdateForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
