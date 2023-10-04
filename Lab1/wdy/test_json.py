import json


with open('../Dataset/Movie_info1.json', 'r', encoding='UTF-8') as f:
    json_data = json.load(f)

with open('../Dataset/Movie_id.csv', "r") as f:
    id_list = []
    id_list_n = f.readlines()  # 有换行符
    [id_list.append(line.strip()) for line in id_list_n]  # 无换行符


json_list = list(json_data.keys())
for item in id_list:
    if item not in json_list:
        print(item)


# 1309046
# 1768351
# 1293691
# 1292790
# 1316505
# 1292331
# 1796939
# 1308988
# 1307528
# 1303053
# 1307072
# 2043126
# 1305088
# 1296935
# 1304900
# 1829626


