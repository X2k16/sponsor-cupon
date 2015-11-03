# encoding=utf-8

import random
import string
import traceback
import time
from tempfile import NamedTemporaryFile

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management.base import BaseCommand
from django.conf import settings

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
            last_name = ""  # FIXME:
            first_name = ""  # FIXME:

            account = Account(
                last_name=last_name,
                first_name=first_name
                email=email,
                password=password,
                is_registered=True
            )

            peatix = Peatix()
            peatix.create_account(email, password, name)
            peatix.buy_ticket(
                settings.PTX_EVENT_ID, settings.PTX_TICKET_ID,
                last_name, first_name, 1,
                settings.PTX_CUPON_CODE
            )
            img = peatix.get_ticket(settings.PTX_EVENT_ID)
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
