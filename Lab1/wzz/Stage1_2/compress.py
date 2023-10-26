import json
from typing import List
def compress(List: index_list)->bytes:
    count = 0
    vb_byte = []        #可变长度编码
    for i in index_list:    #index_list:若干个长的id
        reverted_byte = []
        while index_list[i] >= 128 :
            mod = index_list[i]%128
            reverted_byte.append(bytes(mod))
            index_list[i] >> 7
        reverted_byte[0] = byte(int(reverted_byte[0])+128)
        for j in reverted_byte[::-1]:           #倒着遍历
            vb_byte.append(reverted_byte[j])
    return 

if __name__ == "__main__":
    with open(r"D:\web_lab\WebInfo\Lab1\wzz\Stage1_2\data\reverted_dict.json","r",encoding="UTF-8" ) as f_in:
        reverted_dict = json.load(f_in)
    for key in reverted_dict:
        reverted_dict[key] = compress(reverted_dict[key])
        