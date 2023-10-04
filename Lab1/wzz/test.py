import re
from ua_pool import UAPool
import random
import time
from bs4 import BeautifulSoup
import requests
import json


class Spider:
    def __init__(self):
        self.prefix_url = 'https://movie.douban.com/subject/{}/'
        self.headers = {}
        self.user_agent_pool = UAPool()
        self.id_list = []

    def get_head(self) -> dict:
        self.headers['User-Agent'] = self.user_agent_pool.pop_pool()
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
        text = response.text.encode('UTF-8')
        status_code = response.status_code
        return text, status_code


class Movie(Spider):

    def __init__(self, movie_id_path):
        super(Movie, self).__init__()
        self.movie_id_list = self.get_id_list(movie_id_path)
        self.movie_id_path = movie_id_path
        self.error = []
        self.all_info = {}
        self.count = 0

    def parse_text(self, text, movie_id):
        # 这里应当维护一个字典 info ，包含了需要爬取的有效信息，结构应当为
        # {'name': ' ', 'type': ' ', 'director': ' ', 'characters': ['', '', '', ...], ...}
        info = {}
        soup = BeautifulSoup(text, 'html.parser')
        """
            提取影片名
        """
        name = soup.find('span', {'property': 'v:itemreviewed'})
        if name is None:
            error_msg = movie_id + "没有名称\n"
            print(error_msg)
            self.error.append(error_msg)
            info['name'] = ''
        else:
            info['name'] = name.text

        favor = soup.find('a',{'href':"https://movie.douban.com/subject/{}/comments?status=P".format(movie_id)})
        if favor is None:
            error_msg = movie_id + "没有想看人数的信息\n"
            print(error_msg)
            self.error.append(error_msg) 
            info['favor'] = ''
        else:
            info['favor'] = favor.text

        watched = soup.find('a',{'href':"https://movie.douban.com/subject/{}/comments?status=F".format(movie_id)})
        if watched is None:
            error_msg = movie_id + "没有看过人数的信息\n"
            print(error_msg)
            self.error.append(error_msg) 
            info['watched'] = ''
        else:
            info['watched'] = watched.text

        """
            提取包括导演，主演等信息
        """
        main_info = soup.find('div', {'id': 'info'})
        if main_info is None:
            error_msg = movie_id + "没有导演等主要信息\n"
            print(error_msg)
            self.error.append(error_msg)
            return None
        match_list = {'导演: ': '', '编剧: ': '', '主演: ': '', '类型: ': '', '制片国家/地区: ': '', '语言: ': '',
                      '上映日期: ': '', '片长: ': '', '又名: ': '', 'IMDb: ': ''}

        for item in match_list.keys():
            match = re.search(item + r'(.*)$', main_info.text, re.M)  # re.M 表示用行匹配
            if match:
                match_list[item] = match.group(1)
            else:
                error_msg = movie_id + "中'" + item + "'没有对应匹配\n"
                print(error_msg)
                self.error.append(error_msg)
                match_list[item] = ''
        info['director'] = match_list['导演: '].split(' / ')
        info['characters'] = match_list['主演: '].split(' / ')
        info['playwright'] = match_list['编剧: '].split(' / ')
        info['type'] = match_list['类型: '].split(' / ')
        info['country_or_region'] = match_list['制片国家/地区: '].split(' / ')
        info['language'] = match_list['语言: '].split(' / ')
        info['release_date'] = match_list['上映日期: '].split(' / ')  # 可能不同地区有多个上映日期
        info['film_length'] = match_list['片长: '].split(' / ')  # 可能有加长版
        info['alias'] = match_list['又名: '].split(' / ')
        info['IMDb'] = match_list['IMDb: ']
        """
            提取简要介绍
        """
        intro = soup.find('span', {'class': 'all hidden'})
        intro = soup.find('span', {'property': 'v:summary'}) if intro is None else intro
        if intro is None:
            error_msg = movie_id + "没有介绍\n"
            print(error_msg)
            self.error.append(error_msg)
            info['intro'] = ''
        else:
            intro_text = intro.text.replace('\n', '').replace('\r', '')  # Windows下两个要同时去除
            intro_text = intro_text.replace('　', '').strip()  # 注意这里是 全角空格
            intro_text = intro_text.replace('  ', '')  # 尽量去除中间的空格, 最终只会留下最多一个空格
            info['intro'] = intro_text

        return info

    def save_all_info_to_json(self):
        index = self.movie_id_path.rfind('/')
        save_path = self.movie_id_path[0:index] + '/Movie_info1.json' if index != -1 else 'Movie_info1.json'
        with open(save_path, 'w', encoding='UTF-8') as f:
            json.dump(self.all_info, f, indent=4, ensure_ascii=False)

    def save_error_message(self):
        index = self.movie_id_path.rfind('/')
        save_path = self.movie_id_path[0:index] + '/Movie_error1.txt' if index != -1 else 'Movie_error1.txt'
        with open(save_path, 'w') as f:
            f.writelines(self.error)

    def run(self):
        for movie_id in self.movie_id_list:
            self.count += 1
            print(self.count, ". 正在爬取id为 {} 的电影的信息".format(movie_id))
            movie_url = self.get_url(movie_id)
            text, status_code = self.get_html(movie_url)
            if status_code == 404:
                print("id: {} 的资源不存在!".format(movie_id))
                self.error.append(movie_id + '\n')
            else:
                self.all_info[movie_id] = self.parse_text(text, movie_id)
            print("    id为 {} 的电影的信息爬取完毕\n".format(movie_id))
            if self.count % 20 == 0:
                print("   ", time.ctime())
            time.sleep(random.uniform(0.5, 1))  # 休眠 0.5 ~ 1s
        self.save_all_info_to_json()
        self.save_error_message()


if __name__ == '__main__':
    movie_path = '../Dataset/Movie_id_tmp1.csv'
    movie_spider = Movie(movie_path)
    movie_spider.run()
