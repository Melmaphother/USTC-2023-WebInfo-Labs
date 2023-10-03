import os
import requests
from lxml import etree
import json


class Spider:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }
    id_list = []

    def get_head(self) -> dict:
        return self.headers

    def get_id_list(self, spider_file_path) -> list:
        with open(spider_file_path, "r") as f:
            id_list_n = f.readlines()  # 有换行符
            [self.id_list.append(line.strip()) for line in id_list_n]  # 无换行符
            return self.id_list


class Movie(Spider):
    def __init__(self, movie_path):
        self.urls = self.get_id_list(movie_path)
        self.movie_path = movie_path

    def get_html(self, url):
        response = requests.get(url=url, headers=self.get_head())
        content = response.content.decode('UTF-8')
        return etree.HTML(content)

    def parse_html(self, html) -> dict:
        # 这里应当返回一个字典 info ，包含了需要爬取的有效信息，结构应当为
        # {'name': ' ', 'type': ' ', 'director': ' ', 'characters': ['', '', '', ...], ...}
        pass

    def save_html_to_json(self, info):
        save_path = self.movie_path[0:self.movie_path.rfind('/')] + '/Movie_info.json'
        with open(save_path, 'w') as f:
            json.dump(info, f, indent=4)

    def run(self):
        pass


if __name__ == '__main__':
    movie_path = '../Dataset/Movie_id.csv'
    movie_spider = Movie(movie_path)

