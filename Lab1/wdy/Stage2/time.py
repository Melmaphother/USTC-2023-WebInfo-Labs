def __getitem__(self, index):
    row = self.data.iloc[index]
    user = self.user_to_idx[row['User']]
    book = self.book_to_idx[row['Book']]
    rating = row['Rate'].astype('float32')

    time = row['Time'].astype(str)    # 转成 str 类型
    time = time.apply(lambda x: x.split('+')[0].replace('-', '').replace(
        'T', '').replace(':', '') if isinstance(x, str) else x)  # 去分隔符
    time = time.astype('int64')  # 转成可计算的 int64 类型
    max = time.max()
    min = time.min()
    time = time.apply(lambda x: (
        (x - min) / (max - min) + 1) / 2)  # 归一化到 0.5~1
    rating = rating * time

    text_embedding = self.tag_embedding_dict.get(row['Book'])
    return user, book, rating, text_embedding
