# coding=utf-8

import os
from tempfile import NamedTemporaryFile
import subprocess
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from PIL import Image


TICKET_TEMPLATE_PATH = "{0}/templates/ticket.pdf".format(os.path.dirname(__file__))


def _register_fonts():
    fonts = ["GenShinGothic-Regular", "GenShinGothic-Light"]

    for font in fonts:
        pdfmetrics.registerFont(TTFont(font, "{0}/fonts/{1}.ttf".format(os.path.dirname(__file__), font)))

_register_fonts()


def drawCenteredString(page, fontname, size, x, y, text):
    page.setFont(fontname, size)
    x -= (pdfmetrics.stringWidth(text, fontName=fontname, fontSize=size) / 2.0)
    page.drawString(x, y, text)


def drawLeftString(page, fontname, size, x, y, text):
    page.setFont(fontname, size)
    page.drawString(x, y, text)


def drawRightString(page, fontname, size, x, y, text):
    page.setFont(fontname, size)
    x -= pdfmetrics.stringWidth(text, fontName=fontname, fontSize=size)
    page.drawString(x, y, text)


def generate_ticket_pdf(ticket, f):

    # 印字内容の生成
    buffer = NamedTemporaryFile(suffix=".pdf", delete=True)
    page = canvas.Canvas(buffer, pagesize=A4)

    # 印字ここから
    drawCenteredString(page, "GenShinGothic-Light", 15, 105 * mm, 190 * mm, "{0}スポンサー".format(ticket.sponsor.get_category_display()))
    drawCenteredString(page, "GenShinGothic-Regular", 25, 105 * mm, 165 * mm, "{0} 様".format(ticket.sponsor.name))

    if ticket.shimei:
        drawCenteredString(page, "GenShinGothic-Light", 10, 78 * mm, 138 * mm, "{0} 様".format(ticket.shimei))

    drawRightString(page, "GenShinGothic-Light", 10, 200 * mm, 10 * mm + 11, ticket.name)
    drawRightString(page, "GenShinGothic-Light", 10, 200 * mm, 10 * mm, "No. {0:03d}".format(ticket.id))

    if ticket.is_booth:
        page.setFillColorRGB(1, 0, 0)
        drawCenteredString(page, "GenShinGothic-Regular", 15, 105 * mm, 10 * mm, "ブース担当者様")
        drawCenteredString(page, "GenShinGothic-Regular", 15, 105 * mm, 287 * mm, "ブース担当者様")

    qr = ImageReader(ticket.qr_code)
    page.drawImage(qr, 146 * mm, 106 * mm, 32 * mm, 32 * mm)

    page.showPage()
    page.save()
    buffer.seek(0)

    output = NamedTemporaryFile(suffix=".pdf", delete=True)
    subprocess.call(["pdftk", buffer.name, "multistamp", TICKET_TEMPLATE_PATH, "output", output.name])

    output.seek(0)

    f.write(output.read())

    output.close()
    buffer.close()

    return f


def generate_tickets_pdf(tickets, f):
    buffers = []
    for ticket in tickets:
        buffer = NamedTemporaryFile(suffix=".pdf", delete=True)
        generate_ticket_pdf(ticket, buffer)
        buffers.append(buffer)

    output = NamedTemporaryFile(suffix=".pdf", delete=True)
    cmd = ["pdftk"]
    cmd += [buffer.name for buffer in buffers]
    cmd += ["output", output.name]
    subprocess.call(cmd)

    output.seek(0)

    f.write(output.read())
    output.close()
    for buffer in buffers:
        buffer.close()

    return f
