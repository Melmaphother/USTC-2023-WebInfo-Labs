import requests
from lxml import etree
from tqdm import tqdm
import time
import pandas as pd

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Cookie": 'bid=kdAg8r_7-14; ll="118254"; douban-fav-remind=1; \
     __yadk_uid=8UuZHIBpqV9hLEA8bSBdILTMwA0eC53y; \
     __utmz=30149280.1659860547.3.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; \
     gr_user_id=01ae869f-1ee1-4b74-ae62-a83c82f87b71; _cc_id=4409ce7f5492e4f91ee7775531b96303;\
      panoramaId=1f0542d66fbb33b19ce5ab8a117e16d5393846cff196b1757098abeef99beb13; \
      panoramaId_expiry=1664356265661; __gads=ID=21a9aebc1193eb27-222052b945d7002e:T=1652699121:RT=1663751468:S=ALNI_MYX4W98WjphUfN8mXQe04yBncEf3A; push_doumail_num=0; push_noty_num=0; __utmv=30149280.26299; __gpi=UID=000007f3c05158ed:T=1658476289:RT=1663842941:S=ALNI_Mb-cR3QRGsvHxr_ZE_eDybUeJxUww; _ga=GA1.1.819550760.1657457105; viewed="1794620_1432596_1046265_35819419_35757085"; _ga_RXNMP372GL=GS1.1.1663849396.2.0.1663849396.60.0.0; dbcl2="262998963:TEj1hf1udcM"; ck=dlcs; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=f834d036-6a1e-4d42-891f-c1018abfde95; gr_cs1_f834d036-6a1e-4d42-891f-c1018abfde95=user_id%3A1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_f834d036-6a1e-4d42-891f-c1018abfde95=true; __utmc=30149280; __utma=30149280.819550760.1657457105.1663862603.1663885107.10; __utmt_douban=1; ap_v=0,6.0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1663885114%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DCZeM0HJ91IDWDHcCtV9gtylizSoDTs-xVrvN3RNpp8FSePjFLDzpVCjfrClKxTaT%26wd%3D%26eqid%3D81d6f6c90001ffe100000003632abbf5%22%5D; _pk_ses.100001.8cb4=*; __utmt=1; __utmb=30149280.3.10.1663885107; _pk_id.100001.8cb4=85e2055268379903.1644738451.11.1663885116.1663851059.'
}
col_name = ['id', '电影名', '豆瓣评分', '基本信息', '剧情简介', '演职员']
data = []


def Catch_Movie(start_index):
    # 获取需要爬取的页面ID
    movie_id = []
    with open("data/Movie_id.txt", "r") as fin:
        movie_i = fin.readline().strip("\n")
        while movie_i:
            movie_id.append(movie_i)
            movie_i = fin.readline().strip("\n")

    for k in tqdm(range(start_index, len(movie_id))):
        time.sleep(2)
        # 获取网页
        id = movie_id[k]
        movie = {"id": id, "电影名": "", "基本信息": "", "剧情简介": "", "演职员": "", "豆瓣评分": ""}
        url = "https://movie.douban.com/subject/" + id + "/"
        response = requests.get(url, headers=headers)
        content = response.content.decode('utf8')
        html = etree.HTML(content)
        # 获取电影名
        title = html.xpath('//*[@id="content"]/h1/span/text()')
        for str in title:
            movie["电影名"] += str
        # 获取评分信息
        rating = html.xpath('//div[@class="rating_self clearfix"]//strong/text()')
        if len(rating):
            movie["豆瓣评分"] += html.xpath('//div[@class="rating_self clearfix"]//strong/text()')[0]
        else:  # 《建国大业》等电影禁止评分
            movie["豆瓣评分"] = "暂无评分"
        # 获取基本信息
        info = html.xpath(
            '//*[@id="info"]/span/text() | //*[@id="info"]/span//a/text() | //*[@id="info"]/text() | //*[@id="info"]/span/span/text()')
        for str in info:
            if str[0] == '\n':
                movie["基本信息"] += '\n'
            else:
                movie["基本信息"] += str
        # 获取完整的简介
        intro = html.xpath('//span[@class="all hidden"]/text()')
        if len(intro) == 0:
            intro = html.xpath('//span[@property="v:summary"]/text()')
        for str in intro:
            str = str.strip("\n").strip(" ").strip("\n")
            movie["剧情简介"] += str + '\n'
        # 获取演职员表
        stuff = html.xpath('//li[@class="celebrity"]//span/text() | //li[@class="celebrity"]//span//a/text()')
        for i, str in enumerate(stuff):
            movie["演职员"] += str + " "
            if i % 2 != 0:
                movie["演职员"] += "\n"
        data.append(movie)


def main():
    start_index = 0
    need_header = True if start_index == 0 else False
    try:
        Catch_Movie(start_index)
    finally:
        pd.DataFrame(data, columns=col_name).to_csv('data/book.csv', index=False, mode='a', header=need_header)


if __name__ == "__main__":
    main()
