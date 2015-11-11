# encoding=utf-8

from django import forms
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm

from ticket.models import Sponsor


class BootstrapMixins(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
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
