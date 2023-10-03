import json
import requests
from bs4 import BeautifulSoup

# path = '../Dataset/Book_id.csv'
# save_path = path[:path.rfind('/')] + '/Movie_info.json'
# print(save_path)
#
# dict1 = {'name': 'Melmaphother', 'type': 'Person', 'director': 'a', 'characters': {'1': 'b', '2': 'v', '3': 'c'}}
# dict2 = {'name': 'Melmaphother', 'type': 'Person', 'director': 'a', 'characters': ['b', 'v', 'c']}
# # json文件中支持数组 [], 所以主演可以用 dict2 形式表示
# dict3 = {'1234567': dict2}
#
# with open(save_path, 'w') as f:
#     json.dump(dict1, f, indent=4)
#
#     json.dump(dict2, f, indent=4)
#     json.dump(dict3, f, indent=4)

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
#                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
# }
#
#
# def get_html(url):
#     response = requests.get(url=url, headers=headers)
#     text = response.text
#     status_code = response.status_code
#     return text, status_code
#
#
# text, status_code = get_html('https://movie.douban.com/subject/1292052/')
# with open('douban.html', 'w', encoding='UTF-8') as f:
#     f.write(text)
# print(status_code)


from bs4 import BeautifulSoup

html = """
<html>
  <head>
    <title>Example</title>
  </head>
  <body>
    <p>Hello, <b>world</b>!</p>
  </body>
</html>
"""

soup = BeautifulSoup(html, 'html.parser')

print(type(soup))
# 获取标题标签
title_tag = soup.title
print(type(title_tag))
print(title_tag.text)  # 输出：Example
print(type(title_tag.text))

# 获取段落标签
p_tag = soup.p
print(p_tag.text)  # 输出：Hello, world!
