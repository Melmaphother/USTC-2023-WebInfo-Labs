from Spider import Spider
import bs4
from typing import Dict, List, Any
import json


class bookSpider(Spider):
    # douban book spider
    def __init__(self, pre_url, spider_path, header):
        super(bookSpider, self).__init__(pre_url, spider_path, header)
        self.book_list = []

    def parse_html(self, text: str, id_single: str) -> Dict:
        soup = bs4.BeautifulSoup(text, "html.parser")
        book_title = str(soup.find('span', property='v:itemreviewed')).strip()
        book_score = soup.find('strong', property="v:average")
        book_score = str(book_score.next).strip()
        book_dict = {"id": id_single, "title": book_title, "score": book_score}
        self.book_list.append(book_dict)
        return book_dict

    def save_to_json(self):
        for book in self.book_list:
            json_obj = json.dumps(book)
            with open("test.json", 'a+') as f:
                f.write(json_obj)


