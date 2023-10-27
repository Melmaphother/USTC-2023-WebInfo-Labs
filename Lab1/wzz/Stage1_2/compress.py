import json
def compress(index_list)->bytes:
    count = 0
    vb_arr = []        #可变长度编码对应的列表（最后转换成bytes类）
    for i in range(0,len(index_list)):    #index_list:若干个长的id
        reverted_arr = []
        while index_list[i] >= 128 :
            mod = index_list[i]%128
            reverted_arr.append(mod)
            index_list[i] = index_list[i] >> 7
        if index_list[i] > 0:
            reverted_arr.append(index_list[i])
        reverted_arr[0] = int(reverted_arr[0])+128
        for j in range(len(reverted_arr)-1,-1,-1):           #倒着遍历
            vb_arr.append(reverted_arr[j])
    byte = bytes(vb_arr)
    return bytes(vb_arr)

if __name__ == "__main__":
    with open(r"D:\web_lab\WebInfo\Lab1\wzz\Stage1_2\data\Movie_reverted_dict.json","r",encoding="UTF-8" ) as f_in:
        reverted_dict = json.load(f_in)
    for key in reverted_dict:
        reverted_dict[key] = compress(reverted_dict[key])
    with open(r"D:\web_lab\WebInfo\Lab1\wzz\Stage1_2\data\Movie_reverted_dict_compressed.json","w",encoding="UTF-8" ) as f_out:
        json.dump(reverted_dict, f_out, indent=4, ensure_ascii=False)