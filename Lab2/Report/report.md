# Web 第二次实验实验报告

## 目录

[toc]

## 简介

### 小组成员

> 组长：王道宇  PB21030794

>  组员：王   昱  PB21030814
>
>  ​          吴泽众  PB21030802

### 实验环境

> System:  Win 11 
>
> IDE / Editor:  Pycharm community ,  Visual Studio Code
>
> Language:  python3 ,  Jupyter Notebook
>
> Environment / tool:  Anaconda ,  git
>
> Repository:  [WebInfo](https://github.com/Melmaphother/WebInfo)    ( private now)

## 实验内容简介

### **Stage1**

1. 从公开图谱中匹配已经从 Freebase 中抽取的 578 部电影实体有关系的实体和关系，并生成图谱。
2. 按照规则对抽取到的图谱进行处理，过滤出数量在合适区间的实体或关系。

### **Stage2**

TODO

## 实现过程介绍

### **Stage1**

#### 关于 Freebase 数据库：

Freebase是一个已经不再活跃的结构化知识数据库，它由Meta公司创建，于2016年关闭。Freebase旨在建立一个包含大量实体及其之间关系的知识图谱，以支持广泛的信息检索、语义搜索和知识图谱构建。

关于Freebase数据库：

1. **数据结构：** Freebase采用图谱结构，将知识组织成实体和关系的网络。实体包括人物、地点、电影、书籍等，而关系描述了这些实体之间的连接。
2. **三元组格式：** Freebase的数据以三元组（主体-谓词-客体）的格式存储。例如，一个关于电影的三元组可能是（Inception，genre，Science Fiction）。

#### 提取三元组并计数

在第一阶段中，我们需要从给定的 578 个电影实体出发，将其作为头或尾与 Freebase 中的三元组匹配。

提取的代码如下：

```python
def ExtractFreebase(freebase_path, KG_path, entities_set):
    with gzip.open(freebase_path, 'rb') as f:
        with open(KG_path, 'w', encoding='utf-8') as f_out:
            for line in f:
                line = line.strip()
                triplet = line.decode().split('\t')[:3]
                if triplet[0] in entities_set or triplet[2] in 						entities_set:
                    f_out.write('\t'.join(triplet) + '\n')
```

#### 过滤三元组

在实体和关系的筛选中，我们有三重过滤标准：

1. 只保留具有`<http://rdf.freebase.com/ns/`前缀的实体。因为存在一类关系<http://rdf.freebase.com/ns/common.notable_for.display_name>，这类关系的构成三元组的尾实体通常为一种语言的字符串，而此类关系的尾实体一般不会和其他的实体相连。便于缩小子图规模
2. 只抽取在子图中出现数目在一定范围内的实体：如果某个实体数目太少，就会导致它与其他实体关系过少，进而导致它的语义关系不强。如果某个实体数量过多，就会导致它形成一种过中心化的趋势，进而导致其呈现“大 V”化。关系也同理，但是考虑到关系一般不会太多，所以没有给关系做上界划分。

过滤的代码如下（以实体过滤为例）：

```python
def __filter_entities(self):
        triple_list_filter_entities = []
        for triplet in self.triple_list:
            if (self.entities_min <= self.entities_count[triplet[0]] <= self.entities_max) and (
                    self.entities_min <= self.entities_count[triplet[2]] <= self.entities_max):
                triple_list_filter_entities.append(triplet)
        return triple_list_filter_entities
```

#### 结果介绍

在保证子图完整度的前提下，考虑到内存的影响，我们做了两跳子图以及两次过滤。

其中第二跳子图基于第一跳子图过滤后生成的实体。

第一次过滤的参数为实体数最小 40，最大 20000，关系数最小 50

第二次过滤的参数为实体数最小 20，最大 20000，关系数最小 50

结果如下：

|              | 第一跳子图 | 第一条子图过滤 | 第二跳子图 | 第二次子图过滤 |
| ------------ | ---------- | -------------- | ---------- | -------------- |
| 三元组数     | 502128     | 37981          | 317217383  | 277816         |
| 实体数       | 308789     | 760            | 50861749   | 23948          |
| 关系数       | 452        | 49             | 1818       | 62             |
| 生成文件类型 | .txt.gz    | .txt           | .txt.gz    | .txt           |
| 生成文件大小 | 9.9MB      | 5.2MB          | 1.38GB     | 74MB           |

### **Stage2**

#### 生成可供操作的 kg_final

通过给定的豆瓣 id 与 freebase id 的映射以及 豆瓣 id 与 kg_final 最终 id 的映射关系，我们可以得到 freebase id 与 kg_final 最终 id 的关系。并对剩余的未编号实体以及关系接下去编号，最终将第一阶段生成的第二跳过滤子图变成用连续数字所代替的子图。

其中编号代码如下（以实体编号为例）：

```python
entities2id = {}
num_of_entities = 578
for entity in entities:
    if entity in entity2id.keys():
        entities2id[entity] = entity2id[entity]
    else:
        entities2id[entity] = str(num_of_entities)
        num_of_entities += 1
```

最终生成的 kg-final 的三元组、实体、关系数量与第二跳子图过滤后的参数一致。但是大小变为了 8.5 MB，更加便于下文的处理。
