from typing import AnyStr, List
import json


class BooleanMatch:
    def __init__(self):
        self.query = ""
        self.query_list = []
        self.query_cache_list = []
        self.mode = ""
        self.error = False
        self.info_mirror = {}
        self.inverted_table_mirror = {}
        # Load data
        print("LOADING DATA!\nPlease wait for a few seconds!")
        self.book_info_path = '../../Stage1_1/Result/Book_info.json'
        self.movie_info_path = '../../Stage1_1/Result/Movie_info.json'
        self.book_inverted_table_path = '../../wzz/Stage1_2/inverted_list_temp.json'
        self.movie_inverted_table_path = '../../wzz/Stage1_2/inverted_list_temp.json'
        with open(self.book_info_path, 'r', encoding="utf-8") as f_book_info:
            self.book_info = json.load(f_book_info)

        with open(self.movie_info_path, 'r', encoding="utf-8") as f_movie_info:
            self.movie_info = json.load(f_movie_info)

        with open(self.book_inverted_table_path, 'r', encoding="utf-8") as f_book_inverted_table:
            self.book_inverted_table = json.load(f_book_inverted_table)

        with open(self.movie_inverted_table_path, 'r', encoding="utf-8") as f_movie_inverted_table:
            self.movie_inverted_table = json.load(f_movie_inverted_table)

        print("Initialization completed! Please start retrieval.")

    def SplitQuery(self) -> list:
        self.query = self.query.strip()
        self.query = self.query.replace('（', '(').replace('）', ')')
        self.query = self.query.replace('(', ' ( ').replace(')', ' ) ')
        self.query = self.query.upper()
        self.query = self.query.replace('AND', ' AND ').replace('OR', ' OR ').replace('NOT', ' NOT ')
        self.query = self.query.replace('和', ' AND ').replace('且', ' OR ').replace('非', ' NOT ')
        return self.query.split()

    def FindCorrespondBracket(self, index: int) -> int:
        i = index + 1
        flag = 0
        while i < len(self.query_list) and not self.error:
            if flag < 0:
                print("The right bracket overabundant!")
                self.error = True
            elif self.query_list[i] == ')':
                if flag == 0:
                    return i
                else:
                    flag -= 1
            elif self.query_list[i] == '(':
                flag += 1
            i += 1
        print("Lack of right bracket!")
        self.error = True
        return -1

    def BooleanSearch(self, query: AnyStr, mode: AnyStr) -> bool:
        self.query = query
        self.mode = mode
        self.query_list = self.SplitQuery()
        self.info_mirror = {'book': self.book_info, 'movie': self.movie_info}
        self.inverted_table_mirror = {'book': self.book_inverted_table, 'movie': self.movie_inverted_table}
        ret = self.BracketOperation(self.query_list)
        if len(ret) != 1:
            print("There are some unexpected words")
            self.error = True
        if not self.error:
            expect_id_list = ret[0]
            if not expect_id_list:
                print("There are no results you want here. Search for something else?")
            else:
                print(expect_id_list)
        return self.error

    def BracketOperation(self, query_list) -> list:
        if not query_list:
            return []
        ret = []
        index = 0
        while index < len(query_list):
            item = query_list[index]
            if not self.error:
                if item == '(':
                    l_bracket = index
                    r_bracket = self.FindCorrespondBracket(l_bracket)
                    if not self.error:
                        ret.append(self.BracketOperation(query_list[l_bracket + 1: r_bracket]))
                        index = r_bracket + 1
                elif item == 'AND' or item == 'OR' or item == 'NOT':
                    ret.append(item)
                else:
                    inverted_table = self.inverted_table_mirror[self.mode]
                    ret.append(inverted_table[item] if item in inverted_table.keys() else [])
                index += 1
            else:
                break
        return self.LogicOperation(ret)

    def LogicOperation(self, ret: list) -> list:
        if 'OR' in ret:
            or_list = []
            for loc, val in enumerate(ret):
                if val == 'OR':
                    or_list.append(loc)
            last_or_index = or_list[-1]
            return self.OR(self.LogicOperation(ret[: last_or_index]), ret[last_or_index + 1])
        elif 'AND' in ret:
            and_list = []
            for loc, val in enumerate(ret):
                if val == 'AND':
                    and_list.append(loc)
            last_and_index = and_list[-1]
            return self.AND(self.LogicOperation(ret[: last_and_index]), ret[last_and_index + 1])
        elif 'NOT' in ret:
            first_not_index = ret.index('NOT')
            return self.NOT(self.LogicOperation(ret[first_not_index + 1:]))
        else:
            return ret[0]

    def OR(self, L1: List, L2: List) -> list:
        ret = []
        if not L1 or not L2:
            print("The operand 'OR' lacks parameter!")
            self.error = True
        if not self.error:
            index1 = 0
            index2 = 0
            while index1 < len(L1) and index2 < len(L2):
                if L1[index1] == L2[index2]:
                    ret.append(L1[index1])
                    index1 += 1
                    index2 += 1
                elif L1[index1] < L2[index2]:
                    ret.append(L1[index1])
                    index1 += 1
                else:
                    ret.append(L2[index2])
                    index2 += 1
            if index1 < len(L1):
                ret.append(L1[index1:])
            if index2 < len(L2):
                ret.append(L2[index2:])
        return ret

    def AND(self, L1: List, L2: List) -> list:
        ret = []
        if not L1 or not L2:
            print("The operand 'AND' lacks parameter!")
            self.error = True
        if not self.error:
            index1 = 0
            index2 = 0
            while index1 < len(L1) and index2 < len(L2):
                if L1[index1] == L2[index2]:
                    ret.append(L1[index1])
                    index1 += 1
                    index2 += 1
                elif L1[index1] < L2[index2]:
                    index1 += 1
                else:
                    index2 += 1
        return ret

    def NOT(self, L: List) -> list:
        ret = []
        if not L:
            print("The operand 'NOT' lacks parameter!")
            self.error = True
        if not self.error:
            info = self.info_mirror[self.mode]
            ret = [x for x in info.key() not in L]
        return ret


if __name__ == '__main__':
    bm = BooleanMatch()
    while True:
        while True:
            mode = input(
                "Please input which mode you'll search: book / movie?\n")
            if mode == 'book' or mode == 'movie':
                break
            else:
                print("Some error? Please input the mode again!")
        query = input("Please input the sequence you'll search:\n")
        error = bm.BooleanSearch(query, mode)
        if error:
            print("Your given sequence is error, Please input again!\n")
        next_choice = input("Would you still like to search: y / n?\n")
        if next_choice == 'n':
            print("Thank you for using this searching engine!")
            break
