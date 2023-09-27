import json

path = '../Dataset/Book_id.csv'
save_path = path[:path.rfind('/')] + '/Movie_info.json'
print(save_path)

dict1 = {'name': 'Melmaphother', 'type': 'Person', 'director': 'a', 'characters': {'1': 'b', '2': 'v', '3': 'c'}}
dict2 = {'name': 'Melmaphother', 'type': 'Person', 'director': 'a', 'characters': ['b', 'v', 'c']}
# json文件中支持数组 [], 所以主演可以用 dict2 形式表示
dict3 = {'1234567': dict2}

with open(save_path, 'w') as f:
    # json.dump(dict1, f, indent=4)

    # json.dump(dict2, f, indent=4)
    json.dump(dict3, f, indent=4)
