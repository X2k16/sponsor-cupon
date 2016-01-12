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

    count = forms.IntegerField(label="枚数")

    def __init__(self, *args, **kwargs):
        self.sponsor = kwargs.pop("sponsor")
        super().__init__(*args, **kwargs)
