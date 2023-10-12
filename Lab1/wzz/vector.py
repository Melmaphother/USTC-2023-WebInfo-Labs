import jieba

sent = """骇客任务hacker mission J.K.Rolling（台）"""

seg_list = jieba.cut(sent, cut_all=True)

print('\n全模式：      ', '/ '.join(seg_list))

seg_list = jieba.cut(sent, cut_all=False)
print('\n精确模式：    ', '/ '.join(seg_list))

seg_list = jieba.cut(sent)
print('\n默认精确模式：', '/ '.join(seg_list))

seg_list = jieba.cut_for_search(sent)
print('\n搜索引擎模式  ', '/ '.join(seg_list))
