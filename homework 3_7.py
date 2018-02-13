from urllib.parse import urlencode, urljoin
import requests
from pprint import pprint

AUTHORIZE_URL = "https://oauth.yandex.ru/authorize"

APP_ID = "79e7358e85e5429ebd80a28a6958243b"

auth_data = {
    "response_type": "token",
    "client_id": APP_ID
}

print("?".join((AUTHORIZE_URL, urlencode(auth_data))))

TOKEN = "AQAAAAAf417KAASCcCeKJkrDIUkXskqkkWeC980"


class YMBase:
    MANAGEMENT_URL = "https://api-metrika.yandex.ru/management/v1/"
    STAT_URL = "https://api-metrika.yandex.ru/stat/v1/data"

    def headers(self):
        return {
            "authorization": "OAuth {}".format(TOKEN),
            "content-type": "application/x-yametrika-json"
        }


class YandexMetrika(YMBase):

    def __init__(self, token):
        self.token = token

    def get_counters(self):
        url = urljoin(self.MANAGEMENT_URL, "counters")
        headers = self.headers()
        response = requests.get(url, headers=headers)
        return [Counter(self.token, counter_id["id"]) for counter_id in response.json()["counters"]]


class Counter(YMBase):

    def __init__(self, token, counter_id):
        self.token = token
        self.counter_id = counter_id

    def get_counter_info(self):
        url = urljoin(self.MANAGEMENT_URL, "counter/{}".format(counter_id))
        headers = self.headers()
        response = requests.get(url, headers=headers)
        return response.json()

    def get_counter_visits(self):
        headers = self.headers()
        params = {
            "id": self.counter_id,
            "metrics": "ym:s:visits"
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()["totals"][0]

    def get_counter_views(self):
        headers = self.headers()
        params = {
            "id": self.counter_id,
            "metrics": "ym:s:pageviews"
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()["data"][0]["metrics"][0]

    def get_counter_users(self):
        headers = self.headers()
        params = {
            "id": self.counter_id,
            "metrics": "ym:up:users"
        }
        response = requests.get(self.STAT_URL, params, headers=headers)
        return response.json()["totals"][0]


metrika_1 = YandexMetrika(TOKEN)

counters = metrika_1.get_counters()

for counter in counters:
    pprint("Количество визитов: {}".format(counter.get_counter_visits()))
    pprint("Количество просмотров: {}".format(counter.get_counter_views()))
    pprint("Количество посетителей: {}".format(counter.get_counter_users()))