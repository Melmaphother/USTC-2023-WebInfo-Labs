import jieba
import json
from typing import Dict, List
import synonyms


def get_book_dict(file_path: str) -> Dict:
    book_dict = {}
    with open(file_path, 'r', encoding="UTF-8") as f:
        book_dict = json.load(f)
    return book_dict


def split_info(text: str, stop_word_file_path: str) -> List:
    seg_list = jieba.cut(text, cut_all=True)
    with open(stop_word_file_path, 'r', encoding="UTF-8") as f:
        stop_word_list = [word.strip('\n') for word in f.readlines()]
    extracted_word = []
    for word in seg_list:
        if word not in stop_word_list:
            extracted_word.append(word)
    print(extracted_word)
    true_extract_word = []
    for i in range(len(extracted_word)):
        if extracted_word[i] not in true_extract_word:
            true_extract_word.append(extracted_word[i])
        for j in range(i+1, len(extracted_word)):
            if extracted_word[j] not in true_extract_word and synonyms.compare(extracted_word[i], extracted_word[j], seg=False) < 0.6:
                true_extract_word.append(extracted_word[j])
    return true_extract_word


if __name__ == "__main__":
    # seg_list = jieba.cut("", cut_all=True)
    # print("Full Mode: " + "/ ".join(seg_list))  # 全模式
    #
    # seg_list = jieba.cut("安托万·德·圣埃克苏佩里（Antoine de Saint-Exupery, 1900-1944）1900年6月29日出生在法国里昂", cut_all=False)
    # print("Default Mode: " + "/ ".join(seg_list))  # 默认模式
    #
    # seg_list = jieba.cut("他来到了网易杭研大厦")
    # print("  ".join(seg_list))
    #
    # seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    # print("  ".join(seg_list))
    path1 = "./Result/Book_info.json"
    path2 = "./Dataset/cn_stopwords.txt"
    dict_ = get_book_dict(path1)
    print(dict_['1046265'])
    print(dict_['1017143'])
    true_word = split_info(dict_['1046265']['content introduction'], path2)
    print(true_word)
