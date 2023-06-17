import json

import requests


class Http:

    def __init__(self, web_url: str = 'https://ptsv3.com/t/injaxn/'):
        self.ulr = web_url

    def post(self, data=None):
        if data:
            return requests.post(self.ulr, json.dumps(data))
        else:
            return requests.post(self.ulr)

    def get(self):
        return requests.get(self.ulr)


def main():
    http_obj = Http()
    http_obj.get()

if __name__ == '__main__':
    main()
