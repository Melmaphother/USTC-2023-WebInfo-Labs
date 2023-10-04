import re
import time
from bs4 import BeautifulSoup
import requests
import json


class Spider:
    def __init__(self):
        self.prefix_url = 'https://movie.douban.com/subject/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }
        self.id_list = []

    def get_head(self) -> dict:
        return self.headers

    def get_id_list(self, spider_file_path) -> list:
        with open(spider_file_path, "r") as f:
            id_list_n = f.readlines()  # 有换行符
            [self.id_list.append(line.strip()) for line in id_list_n]  # 无换行符
            return self.id_list

    def get_url(self, spider_id):
        return self.prefix_url.format(spider_id)

    def get_html(self, url):
        response = requests.get(url=url, headers=self.get_head())
        text = response.text
        status_code = response.status_code
        return text, status_code


class Movie(Spider):

    def __init__(self, movie_path):
        super(Movie, self).__init__()
        self.movie_id_list = self.get_id_list(movie_path)
        self.movie_path = movie_path
        self.error = []
        self.info = {}

    def parse_text(self, text, movie_id):
        # 这里应当维护一个字典 info ，包含了需要爬取的有效信息，结构应当为
        # {'name': ' ', 'type': ' ', 'director': ' ', 'characters': ['', '', '', ...], ...}
        soup = BeautifulSoup(text, 'html.parser')
        """
            提取影片名
        """
        name = soup.find('span', {'property': 'v:itemreviewed'})
        if name is None:
            print(movie_id, "没有名称\n")
            return None
        self.info['name'] = name.text
        """
            提取包括导演，主演等信息
        """
        main_info = soup.find('div', {'id': 'info'})
        if main_info is None:
            print(movie_id, "没有导演等主要信息\n")
            return None
        match_list = {'导演: ': '', '编剧: ': '', '主演: ': '', '类型: ': '', '制片国家/地区: ': '', '语言: ': '',
                      '上映日期: ': '', '片长: ': '', '又名: ': '', 'IMDb: ': ''}

        for item in match_list.keys():
            match = re.search(item + r'(.*)$', main_info, re.M)  # re.M 表示用行匹配
            if match:
                match_list[item] = match.group(1)
            else:
                print(movie_id, "中'", item, "'没有对应匹配\n")
                return None
        self.info['director'] = match_list['导演: '].split(' / ')
        self.info['characters'] = match_list['主演: '].split(' / ')
        self.info['playwright'] = match_list['编剧: '].split(' / ')
        self.info['type'] = match_list['类型: '].split(' / ')
        self.info['country_or_region'] = match_list['制片国家/地区: '].split(' / ')
        self.info['language'] = match_list['语言: '].split(' / ')
        self.info['release_date'] = match_list['上映日期: ']
        self.info['film_length'] = match_list['片长']
        self.info['alias'] = match_list['又名: '].split(' / ')
        self.info['IMDb'] = match_list['IMDb: ']
        """
            提取简要介绍
        """
        intro = soup.find('span', {'class': "all hidden"})
        if intro is None:
            print(movie_id, "没有介绍\n")
            return None
        intro_text = intro.text.replace('\n', '').replace('\r', '')  # Windows下两个要同时去除
        intro_text = intro_text.replace('　', '').replace(' ', '')  # 注意前面是全角空格，后面是半角空格
        self.info[intro] = intro_text

    def save_info_to_json(self, movie_id):
        index = self.movie_path.rfind('/')
        save_path = self.movie_path[0:index] + '/Movie_info.json' if index != -1 else 'Movie_info.json'
        with open(save_path, 'a+') as f:
            json.dump(self.info, f, indent=4)

    def save_error_message(self):
        index = self.movie_path.rfind('/')
        save_path = self.movie_path[0:index] + '/Movie_error.txt' if index != -1 else 'Movie_error.txt'
        with open(save_path, 'w') as f:
            f.writelines(self.error)

    def run(self):
        for movie_id in self.movie_id_list:
            print("正在爬取id为 {} 的电影的信息\n".format(movie_id))
            movie_url = self.get_url(movie_id)
            text, status_code = self.get_html(movie_url)
            if status_code == 404:
                print("id：{} 的资源不存在！\n".format(movie_id))
                self.error.append(movie_id)
            else:
                self.parse_text(text, movie_id)
                self.save_info_to_json(movie_id)

            time.sleep(2)  # 休眠 2s
        self.save_error_message()


if __name__ == '__main__':
    movie_path = '../Dataset/Movie_id_tmp.csv'
    movie_spider = Movie(movie_path)
    movie_spider.run()
