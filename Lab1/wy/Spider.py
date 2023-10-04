from typing import List, Any
import requests


class Spider:
    def __init__(self, pre_url, spider_path, header):
        self.pre_url = pre_url
        self.spider_path = spider_path
        self.id_list = []
        self.header = header
        self.url = []

    def get_id_list(self):
        with open(self.spider_path, "r") as f:
            id = f.readlines()
            self.id_list = [id_single.strip() for id_single in id]

    def create_url(self):
        for id_ in self.id_list:
            self.url.append(self.pre_url + id_)

    def get_response(self, request_url: str):
        respond = requests.get(url=request_url, headers=self.header)
        return respond.text, respond.status_code
