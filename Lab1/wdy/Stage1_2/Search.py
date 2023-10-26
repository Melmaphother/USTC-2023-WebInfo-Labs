from typing import AnyStr, List, Tuple
import json
import colorama

class BooleanMatch:
    def __init__(self):
        self.query = ""
        self.query_list = []
        self.query_cache_list = []
        self.mode = ""
        self.error = False
        self.info = {}  # info of the mode (Stage1_1)
        self.inverted_table = {}  # inverted table of the mode (Stage1_2)
        self.skip_list = {}  # skip list of the mode (Stage1_2)
        self.pre_sort_ids = ()

        # Load data
        print('*' * 10 + " Douban Searching Engine " + '*' * 10)
        print('*' * 10+ " LOADING DATA! Please wait for a few seconds! " + '*' * 10)
        self.book_info_path = '../../Stage1_1/Result/Book_info.json'
        self.movie_info_path = '../../Stage1_1/Result/Movie_info.json'
        self.book_inverted_table_path = '../../wzz/Stage1_2/data/reverted_dict.json'
        self.movie_inverted_table_path = '../../wzz/Stage1_2/data/reverted_dict.json'
        self.book_skip_list_path = '../../wzz/Stage1_2/data/skip_dict.json'
        self.movie_skip_list_path = '../../wzz/Stage1_2/data/skip_dict.json'

        with open(self.book_info_path, 'r', encoding="utf-8") as f_book_info:
            self.book_info = json.load(f_book_info)

        with open(self.movie_info_path, 'r', encoding="utf-8") as f_movie_info:
            self.movie_info = json.load(f_movie_info)

        with open(self.book_inverted_table_path, 'r', encoding="utf-8") as f_book_inverted_table:
            self.book_inverted_table = json.load(f_book_inverted_table)

        with open(self.movie_inverted_table_path, 'r', encoding="utf-8") as f_movie_inverted_table:
            self.movie_inverted_table = json.load(f_movie_inverted_table)

        with open(self.book_skip_list_path, 'r', encoding="utf-8") as f_book_skip_list:
            self.book_skip_list = json.load(f_book_skip_list)

        with open(self.movie_skip_list_path, 'r', encoding="utf-8") as f_movie_skip_list:
            self.movie_skip_list = json.load(f_movie_skip_list)

        print("Initialization completed! Start you travel!")

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

    def CreateSkipList(self, L: List) -> List:
        if len(L) == 0:
            self.error = True
            return []
        if not self.error:
            interval = int(len(L) ** 0.5)
            skip_list = [(L[0], 0 if len(L) == 1 else interval, 0)]  # avoid len(L) == 1
            for i in range(interval, len(L) - interval, interval):
                skip_list.append((L[i], i + interval, i))
            last = len(skip_list) * interval
            if last < len(L):
                skip_list.append(((L[last - 1]), len(L) - 1, last - 1))
            return skip_list

    def BooleanSearch(self, query: AnyStr, mode: AnyStr) -> bool:
        self.query = query
        self.mode = mode
        self.query_list = self.SplitQuery()
        self.info = self.book_info if mode == 'book' else self.movie_info
        self.inverted_table = self.book_inverted_table if mode == 'book' else self.movie_inverted_table
        self.skip_list = self.book_skip_list if mode == 'book' else self.movie_skip_list
        pre_sort_id_list = list(self.info.keys())
        pre_sort_id_list.sort()
        self.pre_sort_ids = (pre_sort_id_list, self.CreateSkipList(pre_sort_id_list))

        ret = self.BracketOperation(self.query_list)
        if len(ret) == 0:
            print("Sorry! But there are no results you want here.")
            # not find doesn't mean error
        if not self.error:
            ret_id_list = ret[0]
            print(ret_id_list)

        return self.error

    def BracketOperation(self, query_list: List) -> Tuple:
        if not query_list:
            return [], []
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
                    item_id_list = self.inverted_table[item] if item in self.inverted_table.keys() else []
                    item_skip_list = self.skip_list[item] if item in self.skip_list.keys() else []
                    item_id_list_and_skip_list = (item_id_list, item_skip_list)
                    ret.append(item_id_list_and_skip_list)
                    index += 1
            else:
                break
        logic_ret = self.LogicOperation(ret)

        return logic_ret

    def LogicOperation(self, ret: List) -> Tuple:
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
                print("Lack of some parameters")
                self.error = True
            elif not self.error and len(ret) > 1:
                print("There are some unexpected parameters")
                self.error = True
            return ret[0]

    def OR(self, T1: Tuple, T2: Tuple) -> Tuple:
        ret = []
        L1_id_list = T1[0]
        L2_id_list = T2[0]
        L1_skip_list = T1[1]
        L2_skip_list = T2[1]
        if not L1_id_list or not L2_id_list:
            print("The operand 'OR' lacks parameter!")
            self.error = True
        else:
            index1 = 0
            index2 = 0
            len_1 = len(L1_id_list)
            len_2 = len(L2_id_list)
            interval_1 = int((len(L1_id_list)) ** 0.5)
            interval_2 = int((len(L2_id_list)) ** 0.5)
            while index1 < len(L1_id_list) and index2 < len(L2_id_list):
                while index1 % interval_1 == 0 and index1 < len_1 - interval_1:  # index1 should skip
                    if L1_id_list[index1] == L2_id_list[index2] and L1_skip_list[index1 // interval_1 + 1][0] == \
                            L2_id_list[index2]:
                        ret.extend(L1_id_list[index1: index1 + interval_1])
                        index1 += interval_1
                        index2 += 1
                    elif L1_id_list[index1] < L2_id_list[index2] and L1_skip_list[index1 // interval_1 + 1][0] < \
                            L2_id_list[index2]:
                        ret.extend(L1_id_list[index1: index1 + interval_1])
                        index1 += interval_1
                    else:
                        break  # fail skip
                while index2 % interval_2 == 0 and index2 < len_2 - interval_2:  # index2 should skip
                    if L2_id_list[index2] == L1_id_list[index1] and L2_skip_list[index2 // interval_2 + 1][0] == \
                            L1_id_list[index1]:
                        ret.extend(L2_id_list[index2: index2 + interval_2])
                        index2 += interval_2
                        index1 += 1
                    elif L2_id_list[index2] < L1_id_list[index1] and L2_skip_list[index2 // interval_2 + 1][0] < \
                            L1_id_list[index1]:
                        ret.extend(L2_id_list[index2: index2 + interval_2])
                        index2 += interval_2
                    else:
                        break  # fail skip

                if L1_id_list[index1] == L2_id_list[index2]:
                    ret.append(L1_id_list[index1])
                    index1 += 1
                    index2 += 1
                elif L1_id_list[index1] < L2_id_list[index2]:
                    ret.append(L1_id_list[index1])
                    index1 += 1
                else:
                    ret.append(L2_id_list[index2])
                    index2 += 1

            if index1 < len(L1_id_list):
                ret.extend(L1_id_list[index1:])
            if index2 < len(L2_id_list):
                ret.extend(L2_id_list[index2:])

        return ret, self.CreateSkipList(ret)

    def AND(self, T1: Tuple, T2: Tuple) -> Tuple:
        ret = []
        L1_id_list = T1[0]
        L1_skip_list = T1[1]
        L2_id_list = T2[0]
        L2_skip_list = T2[1]
        if not L1_id_list or not L2_id_list:
            print("The operand 'AND' lacks parameter!")
            self.error = True
        if not self.error:
            index1 = 0
            index2 = 0
            len_1 = len(L1_id_list)
            len_2 = len(L2_id_list)
            interval_1 = int((len(L1_id_list)) ** 0.5)
            interval_2 = int((len(L2_id_list)) ** 0.5)
            while index1 < len_1 and index2 < len_2:
                # try_skip
                while index1 % interval_1 == 0 and index1 < len_1 - interval_1:  # index1 should skip
                    if L1_id_list[index1] < L2_id_list[index2] and L1_skip_list[index1 // interval_1 + 1][0] < \
                            L2_id_list[index2]:
                        index1 = L1_skip_list[index1 // interval_1][1]
                    else:
                        break
                while index2 % interval_2 == 0 and index2 < len_2 - interval_2:  # index2 should skip
                    if L2_id_list[index2] < L1_id_list[index1] and L2_skip_list[index2 // interval_1 + 1][0] < \
                            L1_id_list[index1]:
                        index2 = L2_skip_list[index2 // interval_2][1]
                    else:
                        break

                if L1_id_list[index1] == L2_id_list[index2]:
                    ret.append(L1_id_list[index1])
                    index1 += 1
                    index2 += 1
                elif L1_id_list[index1] < L2_id_list[index2]:
                    index1 += 1
                else:
                    index2 += 1

        return ret, self.CreateSkipList(ret)

    def AND_NOT(self, T1: Tuple, T2: Tuple) -> Tuple:
        ret = []
        L1_id_list = T1[0]
        L2_id_list = T2[0]
        L1_skip_list = T1[1]
        L2_skip_list = T2[1]
        if not L1_id_list or not L2_id_list:
            print("The operand 'NOT' lacks parameter!")
            self.error = True
        else:
            index1 = 0
            index2 = 0
            len_1 = len(L1_id_list)
            len_2 = len(L2_id_list)
            interval_1 = int((len(L1_id_list)) ** 0.5)
            interval_2 = int((len(L2_id_list)) ** 0.5)
            while index1 < len(L1_id_list) and index2 < len(L2_id_list):
                while index1 % interval_1 == 0 and index1 < len_1 - interval_1:  # index1 should skip
                    if L1_id_list[index1] == L2_id_list[index2] and L1_skip_list[index1 // interval_1 + 1][0] == \
                            L2_id_list[index2]:
                        ret.extend(L1_id_list[index1: index1 + interval_1])
                        index1 += interval_1
                        index2 += 1
                    elif L1_id_list[index1] < L2_id_list[index2] and L1_skip_list[index1 // interval_1 + 1][0] < \
                            L2_id_list[index2]:
                        ret.extend(L1_id_list[index1: index1 + interval_1])
                        index1 += interval_1
                    else:
                        break  # fail skip
                while index2 % interval_2 == 0 and index2 < len_2 - interval_2:  # index2 should skip
                    if L2_id_list[index2] == L1_id_list[index1] and L2_skip_list[index2 // interval_2 + 1][0] == \
                            L1_id_list[index1]:
                        ret.extend(L2_id_list[index2: index2 + interval_2])
                        index2 += interval_2
                        index1 += 1
                    elif L2_id_list[index2] < L1_id_list[index1] and L2_skip_list[index2 // interval_2 + 1][0] < \
                            L1_id_list[index1]:
                        ret.extend(L2_id_list[index2: index2 + interval_2])
                        index2 += interval_2
                    else:
                        break  # fail skip

                if L1_id_list[index1] == L2_id_list[index2]:
                    index1 += 1
                    index2 += 1
                elif L1_id_list[index1] < L2_id_list[index2]:
                    ret.append(L1_id_list[index1])
                    index1 += 1
                else:
                    index2 += 1

            if index1 < len(L1_id_list):
                ret.extend(L1_id_list[index1:])

        return ret, self.CreateSkipList(ret)

    def NOT(self, T: Tuple) -> Tuple:
        return self.AND_NOT(self.pre_sort_ids, T)


if __name__ == '__main__':
    bm = BooleanMatch()
    while True:
        while True:
            user_mode = input(
                "Please input which mode you'll search: book / movie?")
            if user_mode == 'book' or user_mode == 'movie':
                break
            else:
                print("Some error! Please be care that you can only choose 'book' or 'movie'!")

        user_query = input("Please input the sequence you'll search:")

        error = bm.BooleanSearch(user_query, user_mode)

        if error:
            next_choice = input("Maybe search for something else? y / n?")
        else:
            next_choice = input("Would you still like to search: y / n?")

        if next_choice == 'n':
            print("Thank you for using this searching engine! Welcome your next travel!")
            break

# （一部）And Not NOt动人
# (一部）And NOt动人
