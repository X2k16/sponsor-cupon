# encoding=utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseRedirect

from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout
from django.contrib.auth.decorators import login_required

from ticket.forms import AuthenticationForm
from ticket.forms import SponsorCreateForm, SponsorUpdateForm, TicketCreateForm
from ticket.models import Sponsor, Ticket
from ticket.get.views import download


def index(request):
    if request.user.is_authenticated():
        return redirect("sponsor_list")
    return redirect("login")


def login(request):
    return django_login(request, "login.html", authentication_form=AuthenticationForm)


def logout(request):
    django_logout(request)
    return redirect("index")


@login_required
def sponsor_list(request):
    sponsors = Sponsor.objects.all()
    context = {
        "sponsors": sponsors
    }
    return render(request, "sponsor_list.html", context)


@login_required
def sponsor_detail(request, pk):
    sponsor = get_object_or_404(Sponsor, id=pk)
    print(request.META)
    context = {
        "sponsor": sponsor,
        "url": "{0}://{1}{2}".format(
            request.META["wsgi.url_scheme"],
            request.META["HTTP_HOST"],
            reverse("get_index", kwargs={"token": sponsor.token})
        )
    }
    return render(request, "sponsor_detail.html", context)


@login_required
def sponsor_ticket(request, pk):
    sponsor = get_object_or_404(Sponsor, id=pk)
    return download(request, sponsor.token)


@login_required
def sponsor_list_ticket(request, pk):
    sponsor = get_object_or_404(Sponsor, id=pk)
    tickets = sponsor.tickets.all()

    form = TicketCreateForm(sponsor=sponsor)
    if request.method == "POST":
        form = TicketCreateForm(request.POST, sponsor=sponsor)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("")

    context = {
        "sponsor": sponsor,
        "tickets": tickets,
        "form": form
    }
    return render(request, "sponsor_list_ticket.html", context)


class SponsorCreateFormView(CreateView):
    template_name = 'sponsor_form.html'
    form_class = SponsorCreateForm

    def form_valid(self, form):
        instance = form.save()

        # チケットを作成する
        tickets = []
        for i in range(instance.get_default_ticket_count()):
            ticket = Ticket()
            ticket.name = "{0}様 {1}".format(instance.name, (i + 1))
            ticket.sponsor = instance
            ticket.is_registered = False
            tickets.append(ticket)
        Ticket.objects.bulk_create(tickets)

        return super().form_valid(form)

sponsor_add = login_required(SponsorCreateFormView.as_view())


class SponsorUpdateFormView(UpdateView):
    model = Sponsor
    template_name = 'sponsor_form.html'
    form_class = SponsorUpdateForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

sponsor_edit = login_required(SponsorUpdateFormView.as_view())
