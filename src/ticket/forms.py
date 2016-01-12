# encoding=utf-8

from django import forms
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm

from ticket.models import Sponsor, Ticket


class BootstrapMixins(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                pass
            else:
                field.widget.attrs["class"] = "form-control"


class AuthenticationForm(BootstrapMixins, DjangoAuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["password"].widget.attrs["placeholder"] = "Password"


class SponsorCreateForm(BootstrapMixins, forms.ModelForm):

    class Meta:
        model = Sponsor
        fields = ("name", "shimei", "email", "category", "description")


class SponsorUpdateForm(BootstrapMixins, forms.ModelForm):

    class Meta:
        model = Sponsor
        fields = ("name", "shimei", "email", "description")


class TicketCreateForm(BootstrapMixins, forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ("is_booth", )

    count = forms.IntegerField(label="枚数", min_value=0, max_value=10)

    def __init__(self, *args, **kwargs):
        self.sponsor = kwargs.pop("sponsor")
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("'commit' must be True.")

        last_ticket = self.sponsor.tickets.all().order_by("-id")[0]
        last_number = int(last_ticket.name.split(" ")[-1])

        # チケットを作成する
        tickets = []
        for i in range(self.cleaned_data["count"]):
            ticket = Ticket()
            ticket.name = "{0}様 {1}".format(self.sponsor.name, (i + 1 + last_number))
            ticket.sponsor = self.sponsor
            ticket.is_registered = False
            ticket.is_booth = self.cleaned_data["is_booth"]
            tickets.append(ticket)
        Ticket.objects.bulk_create(tickets)

        return tickets
