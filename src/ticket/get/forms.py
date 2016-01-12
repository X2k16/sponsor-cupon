# coding=utf-8
from django import forms
from ticket.models import Ticket
from ticket.forms import BootstrapMixins


class TicketForm(BootstrapMixins, forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ("shimei", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["shimei"].required = True

TicketFormSet = forms.modelformset_factory(Ticket, TicketForm, extra=0)
