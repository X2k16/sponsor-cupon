# coding=utf-8
from django.contrib import admin

from ticket.models import Sponsor, Ticket, Account


class TicketInlineAdmin(admin.TabularInline):
    model = Ticket


class SponsorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "shimei")
    inlines = (TicketInlineAdmin, )

admin.site.register(Sponsor, SponsorAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")

admin.site.register(Account, AccountAdmin)
