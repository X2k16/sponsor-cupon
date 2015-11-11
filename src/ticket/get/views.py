# coding=utf-8

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from ticket.models import Sponsor
from ticket.models import Ticket
from ticket.get.forms import TicketFormSet
from ticket.pdf import generate_tickets_pdf


def index(request, token):
    sponsor = get_object_or_404(Sponsor, token=token)
    tickets = sponsor.tickets.all()

    formset = TicketFormSet(queryset=tickets)
    if request.method == "POST":
        formset = TicketFormSet(request.POST, queryset=tickets)
        if formset.is_valid():
            formset.save()

            return redirect("get_ticket", token=token)

    context = {
        "sponsor": sponsor,
        "formset": formset,
        "is_in_preparation": sponsor.is_in_preparation
    }
    return render(request, "get/index.html", context)


def download(request, token):
    sponsor = get_object_or_404(Sponsor, token=token)
    tickets = sponsor.tickets.all()
    response = HttpResponse(content_type='application/pdf')
    generate_tickets_pdf(tickets, response)
    return response
