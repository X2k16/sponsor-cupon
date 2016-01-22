# encoding=utf-8

import random
import string
import traceback
import time
from tempfile import NamedTemporaryFile

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management.base import BaseCommand
from django.conf import settings

from ticket.models import Account
from ticket.models import Ticket
from ptx import Ptx


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            ticket = Ticket.objects.filter(is_registered=False).order_by("updated_at")[0]
        except IndexError:
            time.sleep(5)
            return

        try:
            suffix = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(10)])
            email = settings.TICKET_EMAIL_FORMAT.format(ticket.id, suffix)
            password = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(18)])
            last_name = "スポンサー"
            first_name = "チケット"
            if ticket.is_booth:
                first_name = "ブース"

            account = Account(
                name="{0}({1})".format(ticket.name, ticket.sponsor.get_category_display()),
                email=email,
                password=password,
                is_registered=True
            )

            ptx = Ptx()
            ptx.create_account(account.email, account.password, account.name)
            ptx.buy_ticket(
                settings.PTX_EVENT_ID, settings.PTX_TICKET_ID,
                last_name, first_name, 1,
                settings.PTX_CUPON_CODE
            )
            img = ptx.get_ticket(settings.PTX_EVENT_ID)
            qr_code = InMemoryUploadedFile(
                img, None, "qr_{0}.png".format(ticket.id),
                "image/png", len(img.getvalue()), None
            )

            account.save()
            ticket.account = account
            ticket.qr_code = qr_code
            ticket.is_registered = True
        except:
            traceback.print_exc()

        ticket.save()
