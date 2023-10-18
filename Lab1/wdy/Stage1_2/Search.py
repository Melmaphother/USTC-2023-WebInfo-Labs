from typing import AnyStr, List
import json

output_len = 80


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
        print("Douban Searching Engine\n".center(output_len))
        print("LOADING DATA! Please wait for a few seconds!\n".center(output_len))
        self.book_info_path = '../../Stage1_1/Result/Book_info.json'
        self.movie_info_path = '../../Stage1_1/Result/Movie_info.json'
        self.book_inverted_table_path = '../../wzz/Stage1_2/data/reverted_dict_temp.json'
        self.movie_inverted_table_path = '../../wzz/Stage1_2/data/reverted_dict_temp.json'
        with open(self.book_info_path, 'r', encoding="utf-8") as f_book_info:
            self.book_info = json.load(f_book_info)

        with open(self.movie_info_path, 'r', encoding="utf-8") as f_movie_info:
            self.movie_info = json.load(f_movie_info)

        with open(self.book_inverted_table_path, 'r', encoding="utf-8") as f_book_inverted_table:
            self.book_inverted_table = json.load(f_book_inverted_table)

        with open(self.movie_inverted_table_path, 'r', encoding="utf-8") as f_movie_inverted_table:
            self.movie_inverted_table = json.load(f_movie_inverted_table)

        print("Initialization completed! Start you travel!\n".center(output_len))

    def SplitQuery(self) -> List:
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
                print("The right bracket overabundant!\n".center(output_len))
                self.error = True
            elif self.query_list[i] == ')':
                if flag == 0:
                    return i
                else:
                    flag -= 1
            elif self.query_list[i] == '(':
                flag += 1
            i += 1
        print("Lack of right bracket!\n".center(output_len))
        self.error = True
        return -1

    def BooleanSearch(self, query: AnyStr, mode: AnyStr) -> bool:
        self.query = query
        self.mode = mode
        self.query_list = self.SplitQuery()
        self.info_mirror = {'book': self.book_info, 'movie': self.movie_info}
        self.inverted_table_mirror = {'book': self.book_inverted_table, 'movie': self.movie_inverted_table}
        ret = self.BracketOperation(self.query_list)
        if len(ret) == 0:
            print("Sorry! But there are no results you want here.\n".center(output_len))
            # not find doesn't mean error
        if not self.error:
            print(ret)
        return self.error

    def BracketOperation(self, query_list) -> List:
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
                    else:
                        index += 1
                elif item == 'AND' or item == 'OR' or item == 'NOT':
                    ret.append(item)
                    index += 1
                else:
                    inverted_table = self.inverted_table_mirror[self.mode]
                    ret.append(inverted_table[item] if item in inverted_table.keys() else [])
                    index += 1
            else:
                break
        logic_ret = self.LogicOperation(ret)
        return logic_ret

    def LogicOperation(self, ret: list) -> List:
        if 'OR' in ret:
            or_list = []
            for loc, val in enumerate(ret):
                if val == 'OR':
                    or_list.append(loc)
            last_or_index = or_list[-1]
            return self.OR(self.LogicOperation(ret[: last_or_index]), self.LogicOperation(ret[last_or_index + 1:]))
        elif 'AND' in ret:
            and_list = []
            for loc, val in enumerate(ret):
                if val == 'AND':
                    and_list.append(loc)
            last_and_index = and_list[-1]
            if ret[last_and_index + 1] == 'NOT':
                if ret[last_and_index + 2] != 'NOT':
                    return self.AND_NOT(self.LogicOperation(ret[: last_and_index]),
                                        self.LogicOperation(ret[last_and_index + 2:]))
            return self.AND(self.LogicOperation(ret[: last_and_index]),
                            self.LogicOperation(ret[last_and_index + 1:]))
        elif 'NOT' in ret:
            first_not_index = ret.index('NOT')
            if ret[first_not_index + 1] == 'NOT':
                if ret[first_not_index + 2] != 'NOT':
                    return self.LogicOperation(ret[first_not_index + 2:])
            else:
                return self.NOT(self.LogicOperation(ret[first_not_index + 1:]))
        else:
            if not self.error and len(ret) == 0:
                print("Lack of some parameters\n".center(output_len))
                self.error = True
            elif not self.error and len(ret) > 1:
                print("There are some unexpected parameters\n".center(output_len))
                self.error = True
            return ret[0]

    def OR(self, L1: List, L2: List) -> List:
        ret = []
        if not L1 or not L2:
            print("The operand 'OR' lacks parameter!\n".center(output_len))
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

    def AND(self, L1: List, L2: List) -> List:
        ret = []
        if not L1 or not L2:
            print("The operand 'AND' lacks parameter!\n".center(output_len))
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

    def AND_NOT(self, L1: List, L2: List) -> List:
        ret = []
        if not L2:
            print("The operand 'NOT' lacks parameter!\n".center(output_len))
            self.error = True
        if not self.error:
            for x in L1:
                if x not in L2:
                    ret.append(x)
        return ret

    def NOT(self, L: List) -> list:
        ret = []
        if not L:
            print("The operand 'NOT' lacks parameter!\n".center(output_len))
            self.error = True
        if not self.error:
            info = self.info_mirror[self.mode]
            for x in info.keys():
                if x not in L:
                    ret.append(x)
        ret.sort()
        return ret


if __name__ == '__main__':
    bm = BooleanMatch()
    while True:
        while True:
            mode = input(
                "Please input which mode you'll search: book / movie?\n".center(output_len))
            if mode == 'book' or mode == 'movie':
                break
            else:
                print("Some error! Please be care that you can only choose 'book' or 'movie'!\n".center(output_len))

        query = input("Please input the sequence you'll search:\n".center(output_len))

        error = bm.BooleanSearch(query, mode)

        if error:
            next_choice = input("Maybe search for something else? y / n?\n".center(output_len))
        else:
            next_choice = input("Would you still like to search: y / n?\n".center(output_len))

        if next_choice == 'n':
            print("Thank you for using this searching engine! Welcome your next travel!".center(output_len))
            break

# （一部）And Not NOt动人
