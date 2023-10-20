from split_word import Split

if __name__ == "__main__":
    path1 = "./Result/Book_info.json"
    path2 = "./Dataset/cn_stopwords.txt"
    path3 = "./Dataset/Book_id.csv"
    path4 = "./Result/Book_keyword.json"
    book_test = Split(path3, path1, path2, path4)
    book_test.get_id_list()
    book_test.get_full_info()
    book_test.get_stop_word_list()
    for id_ in book_test.full_info.keys():
        book_test.split_info(book_test.full_info[id_]['title'])
        book_test.split_info(book_test.full_info[id_]['author introduction'])
        book_test.split_info(book_test.full_info[id_]['content introduction'])
        book_test.single_id_info.append(book_test.full_info[id_]['title'])
        book_test.single_id_info.append(book_test.full_info[id_]['author'])
        print(book_test.single_id_info)
        book_test.combine_single_info(id_)
    book_test.save_keyword_to_json()