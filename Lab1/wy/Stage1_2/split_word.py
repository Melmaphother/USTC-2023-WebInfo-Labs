import jieba
import json
from typing import Dict, List
import synonyms
import re


class Split:
    def __init__(self, id_path, info_path, stop_word_path, result_path):
        self.id_path = id_path
        self.info_path = info_path
        self.stop_word_path = stop_word_path
        self.result_path = result_path
        self.full_info = {}
        self.single_id_info = []
        self.id_list = []
        self.stop_word_list = []
        self.extracted_info = {}

    def get_id_list(self) -> List:
        with open(self.id_path, 'r', encoding="UTF-8") as f:
            ids = f.readlines()
            for id_single in ids:
                self.id_list.append(id_single.replace('\n', ''))
        return self.id_list

    def get_full_info(self) -> Dict:
        with open(self.info_path, 'r', encoding="UTF-8") as f:
            self.full_info = json.load(f)
        return self.full_info

    def get_stop_word_list(self) -> List:
        with open(self.stop_word_path, 'r', encoding="UTF-8") as f:
            self.stop_word_list = [word.strip('\n') for word in f.readlines()]
        return self.stop_word_list

    def split_info(self, text: str) -> List:
        pattern = '[^A-Za-z0-9\u4e00-\u9fa5]'
        seg_list = jieba.lcut(re.sub(pattern, '', text), cut_all=True)
        extracted_word = []
        print(seg_list)
        for word in seg_list:
            if word not in self.stop_word_list:
                extracted_word.append(word)
        for i in range(len(extracted_word)):
            if extracted_word[i] not in self.single_id_info and extracted_word[i] != '':
                self.single_id_info.append(extracted_word[i])
            for j in range(i + 1, len(extracted_word)):
                if len(extracted_word[j]) > 0 and len(extracted_word[i]) > 0:
                    if extracted_word[j] not in self.single_id_info and synonyms.compare(extracted_word[i],
                                                                                         extracted_word[j],
                                                                                         seg=False) > 0.6:
                        extracted_word[j] = ''
        return self.single_id_info

    def combine_single_info(self, id__: str) -> Dict:
        self.extracted_info[id__] = self.single_id_info
        self.single_id_info = []
        return self.extracted_info

    def save_keyword_to_json(self):
        with open(self.result_path, 'w', encoding="UTF-8") as f:
            json.dump(self.extracted_info, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    path1 = "./Result/Book_info.json"
    path2 = "./Dataset/cn_stopwords.txt"
    path3 = "./Dataset/Book_id.csv"
    path4 = "./Result/Book_keyword.json"
    book_test = Split(path3, path1, path2, path4)
    book_test.get_id_list()
    book_test.get_full_info()
    book_test.get_stop_word_list()
    for id_ in book_test.id_list:
        book_test.split_info(book_test.full_info[id_]['title'])
        book_test.split_info(book_test.full_info[id_]['author introduction'])
        book_test.split_info(book_test.full_info[id_]['content introduction'])
        book_test.combine_single_info(id_)
    print(book_test.extracted_info)
    book_test.save_keyword_to_json()
