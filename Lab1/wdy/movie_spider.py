import os
from urllib import request as re
import requests
from lxml import etree
import json


class Spider:
    def get_head(self) -> dict:
        headers = {
            "User-Agent": "",
            "Coockie": ""
        }
        return headers

    def get_id_list(self, file_path) -> list:
        with open(file_path, "r") as f:
            id_list_n = f.readlines()  # 有换行符
            id_list = []
            [id_list.append(line.strip()) for line in id_list_n]
            return id_list


class Movie(Spider):
    def __init__(self, file_path):
        self.urls = self.get_id_list(file_path)
        self.file_path = file_path

    def get_html(self, url):
        response = requests.get(url=url, headers=self.get_head())
        content = response.content.decode('UTF-8')
        return etree.HTML(content)

    def parse_html(self, html) -> dict:
        # 这里应当返回一个字典 info ，包含了需要爬取的有效信息，结构应当为
        # {'name': ' ', 'type': ' ', 'director': ' ', 'characters': ['', '', '', ...], ...}
        pass

    def save_html_to_json(self, info):
        save_path = self.file_path[:self.file_path.rfind('/')] + '/Movie_info.json'
        with open(save_path, 'w') as f:
            json.dump(info, f, indent=4)


if __name__ == '__main__':
    file_path = 'aaa'
    movie_spider = Movie(file_path)
