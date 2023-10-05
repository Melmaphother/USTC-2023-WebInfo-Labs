import jieba

sent = """在写这篇专栏时，我一直在用jieba分词，之前花过一段时间去研究了最新分词的技术，并且做了对比，也有个大致的结论，详细可看我的另一篇专栏

无敌小想法：作为AI从业者，基本工具有哪些？（下篇），其中有一部分我介绍了各种前沿分词的介绍，但是就在今天早上，我在今日头条上看到ACL2019中的一篇文章Is Word Segmentation Necessary for Deep Learning of Chinese Representations?后，立马刷新了我的价值观，我花了一上午时间去研究这个玩意到底靠不靠谱，当然这个只是在学术角度去论述了它的可用之处，至于能否落地应用，可能还得要一段时间，好了，不说了，我们还是做好我们自己的事吧，来说说jieba分词，下面让我娓娓道来吧（结尾有彩蛋，不想麻烦的小伙伴可以直接看结尾再决定是否好好看这篇专栏，真是为你们操碎了心）。"""

seg_list = jieba.cut(sent, cut_all=True)

print('全模式：      ', '/ '.join(seg_list))

seg_list = jieba.cut(sent, cut_all=False)
print('精确模式：    ', '/ '.join(seg_list))

seg_list = jieba.cut(sent)
print('默认精确模式：', '/ '.join(seg_list))

seg_list = jieba.cut_for_search(sent)
print('搜索引擎模式  ', '/ '.join(seg_list))
