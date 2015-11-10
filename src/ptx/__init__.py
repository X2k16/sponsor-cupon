# encoding=utf-8
from selenium import webdriver
import time
import io
import base64
from django.conf import settings


class PtxError(Exception):
    pass


class Ptx(object):

    def __init__(self):
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'ja-JP'
        if settings.WEBDRIVER == "chrome":
            self.driver = webdriver.Chrome()
        elif settings.WEBDRIVER == "phantomjs":
            self.driver = webdriver.PhantomJS()
        elif settings.WEBDRIVER == "chrome-hub":
            self.driver = webdriver.Remote(settings.WEBDRIVER_URL, {'platform': 'ANY', 'browserName': 'chrome', 'version': '', 'javascriptEnabled': True})
        else:
            raise ValueError("Invalid WebDriver")

        self.driver.implicitly_wait(10)  # seconds

    def get(self, url):
        self.driver.get(url)

    def set_value(self, name, value):
        if isinstance(value, bool):
            script = "$('input[name={0}]').prop('checked', {1});".format(name, "true" if value else "false")
        else:
            script = "$('input[name={0}]').val('{1}');".format(name, value)
        self.driver.execute_script(script)

    def login(self, username, password):
        self.get("https://pea" + "tix.com/signin")
        button = self.driver.find_element_by_css_selector(".pea" + "tix-login-button")
        button.click()

        time.sleep(1)

        self.set_value("username", username)
        self.set_value("password", password)
        button = self.driver.find_element_by_name("signin_Pea" + "tix")
        button.click()

        time.sleep(1)

        if not "マイイベント" in self.driver.title:
            raise PtxError("Login error")

    def create_account(self, email, password, nickname):
        self.get("https://pea" + "tix.com/signin")

        time.sleep(1)
        self.set_value("nickname", nickname)
        self.set_value("email", email)
        self.set_value("password", password)

        button = self.driver.find_element_by_css_selector(".account-user-form .button-login")
        button.click()

        time.sleep(1)

        if not "マイイベント" in self.driver.title:
            raise PtxError("Login error")

    def buy_ticket(self, event_id, ticket_id, lastname, firstname, count, cupon_code=""):
        url = ("https://pea" + "tix.com/sales/event/{0}/tickets").format(event_id)
        self.get(url)
        self.set_value("number_of_tickets_{0}".format(ticket_id), count)

        if cupon_code:
            button = self.driver.find_element_by_id("show-promocode-link")
            button.click()
            time.sleep(1)
            self.set_value("promocode", cupon_code)

        button = self.driver.find_element_by_id("next-button")
        button.click()
        time.sleep(1)

        self.set_value("lastname", lastname)
        self.set_value("firstname", firstname)
        self.set_value("anonymous", False)
        self.set_value("follow_organizer", False)

        time.sleep(1)
        button = self.driver.find_element_by_id("confirm")
        button.click()
        time.sleep(1)

    def show_ticket(self, event_id):
        url = ("http://pea" + "tix.com/event/{0}/ticket").format(event_id)
        self.get(url)

    def get_ticket(self, event_id):
        url = ("http://pea" + "tix.com/event/{0}/ticket").format(event_id)
        self.get(url)

        img = self.driver.find_element_by_css_selector(".qr-code")
        source = img.get_attribute("src")

        script = """
        (function() {
            $("body").append($("<canvas>").attr("width", 180).attr("height", 180).attr("id", "qr_canvas"));
            var canvas = document.getElementById('qr_canvas');
            var context = canvas.getContext('2d');

            var image = new Image();
            image.src = '%s';
            image.addEventListener('load', function() {
                context.drawImage(image, 0, 0, 180, 180);
                var qrDataUrl = canvas.toDataURL("image/png");
                document.qrDataUrl = qrDataUrl;
            }, false);
        })();
        """ % source
        self.driver.execute_script(script)
        time.sleep(1)
        qr_data_url = self.driver.execute_script("return document.qrDataUrl;")

        f = io.BytesIO(base64.b64decode(qr_data_url.split(",")[-1]))
        f.seek(0)
        return f

    def __del__(self):
        self.driver.quit()
