from Spider import Spider
import bs4
from typing import Dict, List, Any
import json


class bookSpider(Spider):
    def __init__(self, pre_url, spider_path, header):
        super(bookSpider, self).__init__(pre_url, spider_path, header)
        self.book_list = []

    def parse_html(self, text: str, id_single: str) -> Dict:
        soup = bs4.BeautifulSoup(text, "html.parser")
        book_title = str(soup.find('span', property='v:itemreviewed')).strip()
        book_score = soup.find('strong', property="v:average")
        book_score = str(book_score.next).strip()
        book_tag = {"id": id, "title": book_title, "score": book_score}
        self.book_list.append(book_tag)
        return book_tag

    def save_to_json(self):
        for book in self.book_list:
            with open('./test.json', 'a+') as f:
                json.dump(book, f)
