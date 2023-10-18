from skip_list import Skip_revert_list
import json


def AND(skip ,S1: str, S2: str) -> list:
        ret = []
        L1 = skip.reverted_dict[S1]
        L2 = skip.reverted_dict[S2]
        Skip_1 = skip.skip_dict[S1]
        Skip_2 = skip.skip_dict[S2]
        if not L1 or not L2:
            print("The operand 'AND' lacks parameter!")
        else:
            index1 = 0
            index2 = 0
            len_1 = len(L1) 
            len_2 = len(L2)
            while index1 < len_1 and index2 < len_2:
                #try_skip
                if index1 % skip.interval[S1] == 0:     #index1有跳表指针
                    if L1[index1] < L2[index2] and Skip_1[index1 // skip.interval[S1] + 1][0] < L2[index2]:
                        index1 += skip.interval[S1]
                if index2 % skip.interval[S2] == 0:     #index2有跳表指针
                    if L2[index2] < L1[index1] and Skip_2[index2 // skip.interval[S2] + 1][0] < L1[index1]:
                        index2 += skip.interval[S1]
                
                if L1[index1] == L2[index2]:
                    ret.append(L1[index1])
                    index1 += 1
                    index2 += 1
                elif L1[index1] < L2[index2]:
                    index1 += 1
                else:
                    index2 += 1
        return ret


if __name__ == "__main__":
    with open(r"D:\web_lab\WebInfo\Lab1\wy\Stage1_2\Result\Book_keyword.json","r",encoding="UTF-8") as fin:
        participle_dict = json.load(fin)
    skip = Skip_revert_list(participle_dict)
    AND(skip,"挪威","森林")