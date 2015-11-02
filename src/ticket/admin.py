# coding=utf-8
from django.contrib import admin

from ticket.models import Sponsor, Ticket


class TicketInlineAdmin(admin.TabularInline):
    model = Ticket


class SponsorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "shimei")
    inlines = (TicketInlineAdmin, )

admin.site.register(Sponsor, SponsorAdmin)
