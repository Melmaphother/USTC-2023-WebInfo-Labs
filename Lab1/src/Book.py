from Spider import Spider
from bs4 import BeautifulSoup
from typing import Dict, List, Any
import json
import re
import time
import random


class Book(Spider):
    # douban book spider
    def __init__(self, pre_url, book_id_path, header):
        super(Book, self).__init__(pre_url, book_id_path, header)
        self.book_id_list = self.get_id_list()
        self.error = []
        self.all_info = {}
        self.count = 0

    def parse_text(self, text: str, book_id: str) -> Dict:
        soup = BeautifulSoup(text, "html.parser")
        # parse book title
        book_title = soup.find('span', property='v:itemreviewed').text
        # parse book introduction
        book_intro = soup.find_all('div', attrs={'class': 'intro'})
        # solve no author or no (展开全部) condition
        if len(book_intro) >= 2:
            if book_intro[0].text.find("(展开全部)") == -1:
                book_content_intro = book_intro[0].text.replace('\n', '')
                book_author_intro = book_intro[2].text.replace('\n', '')
            else:
                if len(book_intro[1].text.rstrip()) > len(book_intro[0].text.rstrip()):
                    book_content_intro = book_intro[1].text.replace('\n', '')
                else:
                    book_content_intro = book_intro[0].text.replace('\n', '')
                book_author_intro = book_intro[2].text.replace('\n', '')
        else:
            if len(book_intro[1].text.rstrip()) > len(book_intro[0].text.rstrip()):
                book_content_intro = book_intro[1].text.replace('\n', '')
            else:
                book_content_intro = book_intro[0].text.replace('\n', '')
            book_author_intro = None
        # parse basic book info
        book_content = soup.find('div', attrs={'id': 'info'})
        single_book_dict = {"作者": "", "出版社": "", "出版年": "", "页数": "", "定价": "", "装帧": "", "ISBN": ""}
        for info in single_book_dict.keys():
            match = re.search(info + r'(.*)$', book_content.text, re.M)
            if match:
                single_book_dict[info] = match.group(1)
        book_rating = soup.find('div', attrs={'class': "rating_self clearfix"}).find(property='v:average').text.strip()
        # catch data of "want to read/ have read/ be reading"
        book_reading_data = soup.find('div', attrs={'id': 'collector'})
        book_reading_data = book_reading_data.find_all("p", class_="pl")
        number = []
        for data in book_reading_data:
            link = data.find("a")
            if link:
                text = link.get_text()
                numbers = re.search(r'\d+', text)
                number.append(numbers.group())
        # single book info dictionary
        info = {"title": book_title, "author introduction": book_author_intro,
                "content introduction": book_content_intro, "rating": book_rating,
                "publish year": single_book_dict["出版年"].split(': ')[1],
                "page num": single_book_dict["页数"].split(': ')[1],
                "price": single_book_dict["定价"].split(': ')[1],
                "wrapper": single_book_dict["装帧"].split(': ')[1],
                "ISBN": single_book_dict["ISBN"].split(': ')[1],
                "be_reading": str(number[0]), "have_read": str(number[1]), "wanna_read": str(number[2])}
        # add to one single dictionary
        self.all_info[book_id] = info
        return info

    def save_all_info_to_json(self):
        save_path = '../Result/Book_info.json'
        with open(save_path, 'w', encoding='UTF-8') as f:
            json.dump(self.all_info, f, indent=4, ensure_ascii=False)

    def save_error_message(self):
        save_path = '../Result/Book_error.csv'
        with open(save_path, 'w', encoding='UTF-8') as f:
            f.writelines(self.error)

    def run(self):
        book_url = self.create_url()
        for index, book_id in enumerate(self.book_id_list):
            self.count += 1
            print(self.count, ". 正在爬取id为 {} 的书籍的信息".format(book_id))
            (text, status_code) = self.get_response(book_url[index], self.get_headers())
            (text, status_code) = self.get_response(book_url[index], self.cookie) if status_code == 404 else (
                text, status_code)
            # text, status_code = self.get_html(movie_url, headers)
            if status_code == 404:
                error_msg = '{}的资源不存在!\n'.format(book_id)
                print('    ' + error_msg)
                self.error.append(error_msg)
            else:
                self.all_info[book_id] = self.parse_text(text, book_id)
                print("    id为 {} 的书籍的信息爬取完毕\n".format(book_id))
            if self.count % 20 == 0:
                print("   ", time.ctime())
            time.sleep(random.uniform(0.5, 1))  # 休眠 0.5 ~ 1s
        self.save_all_info_to_json()
        self.save_error_message()
