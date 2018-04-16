__author__ = 'yeti'

import requests
from bs4 import BeautifulSoup
from django.conf import settings


class ONCRClient(object):
    URLS = {
        "login_form": "https://www.oncr.ro/login",
        "login_check": "https://www.oncr.ro/login_check",
        "membru_info": "https://www.oncr.ro/%s.json",
    }

    def __init__(self, user=None, password=None, **kwargs):
        self.user = user if user else settings.ONCR_USER
        self.password = password if password else settings.ONCR_PASSWORD
        self.session = requests.session()
        self.logged_in = False

    def do_login(self):
        r_auth = self.session.get(self.URLS.get("login_form"))

        soup = BeautifulSoup(r_auth.text, "html.parser")
        csrf_value = soup.find("input", {"name": "_csrf_token"}).attrs.get("value")
        login_data = {"_username": self.user,
                      "_password": self.password,
                      "_csrf_token": csrf_value}

        r_login = self.session.post(self.URLS.get("login_check"), login_data)
        if "Datele introduse sunt incorecte!" in r_login.text:
            self.logged_in = False
        elif r_login.history:
            for resp in r_login.history:
                if resp.status_code == 302 and resp.headers['location'] == "https://www.oncr.ro/":
                    self.logged_in = True

        return self.logged_in

    def python_date_to_mysql(self, date):
        return date.strftime("%Y-%m-%d")

    def get_membru_json(self, oncr_id):
        r_data = self.session.get(self.URLS.get("membru_info") % oncr_id)
        if r_data.status_code != 200:
            raise Exception("wrong response for RPC")

        return r_data.json()