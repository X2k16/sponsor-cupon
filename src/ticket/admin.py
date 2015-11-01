# coding=utf-8
from django.contrib import admin

from ticket.models import Sponsor


class SponsorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "shimei")

admin.site.register(Sponsor, SponsorAdmin)
