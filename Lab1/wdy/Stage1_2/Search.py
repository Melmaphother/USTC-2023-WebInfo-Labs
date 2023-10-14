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
        print("LOADING DATA!\nPlease wait for a few minutes!")
        self.book_info_path = '../../Stage1_1/Result/Book_info.json'
        self.movie_info_path = '../../Stage1_1/Result/Movie_info.json'
        self.book_inverted_table_path = ''
        self.movie_inverted_table_path = ''
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
                self.error = True
            elif self.query_list[i] == ')':
                if flag == 0:
                    return i
                else:
                    flag -= 1
            elif self.query_list[i] == '(':
                flag += 1
            i += 1
        self.error = True
        return -1

    def BooleanSearch(self, query: str, mode: str) -> bool:
        self.query = query
        self.mode = mode
        self.query_list = self.SplitQuery()
        self.info_mirror = {'book': self.book_info, 'movie': self.movie_info}
        self.inverted_table_mirror = {'book': self.book_inverted_table, 'movie': self.movie_inverted_table}
        self.BracketOperation(self.query_list)
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
                    ret.append(self.inverted_table_mirror[self.mode][item] if item in self.inverted_table_mirror[
                        self.mode].keys else [])

        return self.LogicOperation(ret)

    def LogicOperation(self, ret: list) -> list:
        if 'OR' in ret:
            or_list = ret.index('OR')
            last_or_index = or_list[len(or_list) - 1]
            return Operation.OR(self.LogicOperation(ret[: last_or_index + 1]), ret[last_or_index + 1:])
        elif 'AND' in ret:
            and_list = ret.index('AND')
            last_and_index = and_list[len(and_list) - 1]
            return Operation.AND(self.LogicOperation(ret[: last_and_index + 1]), ret[last_and_index + 1:])
        elif 'NOT' in ret:
            not_list = ret.index('NOT')
            first_not_index = not_list[0]
            return Operation.NOT(self.LogicOperation[ret[first_not_index + 1:]])
        else:
            return ret


class Operation:

    def OR(self, L1: list, L2: List) -> list:
        pass

    def AND(self, L1: list, L2: list) -> list:
        pass

    def NOT(self, L: list) -> list:
        pass


if __name__ == '__main__':
    bm = BooleanMatch()
    while True:
        while True:
            mode = input("Please input which mode you'll search: book / movie?\n")
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
