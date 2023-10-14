from typing import Dict, List
import numpy
import bisect

class revert_list:
    def revert(self):
        for key in self.dict:            
            for item in self.dict[key]:          #key:id item:str(name) 
                if item in self.reverted_dict:
                    index = bisect.bisect_left(self.reverted_dict[item],key)
                    if index != len(self.reverted_dict[item]) and self.reverted_dict[item][index] == key:       #保证不会将重复的id加入词项中
                        continue
                    bisect.insort(self.reverted_dict[item],key) #将key有序插入到列表中
                else:
                    self.reverted_dict[item] = [key]


    def __init__(self,dict):
        self.dict = dict
        self.reverted_dict = {}
        self.revert()

class skip_node:
    def __init__(self,id_,next_node,down):
        self.id = id_
        self.down = down
        self.next_node = next_node

class Skip_revert_list(revert_list):
    def __init__(self,dict):
        self.dict = dict
        revert_list.__init__(self,dict)
        self.interval = {}          #键：字符串     值：跳表间隔
        self.skip_list = {}         #键：字符串     值：List，由一系列跳表节点组成的列表
    
    def cal_interval(self,reverted_dict):
        for id_ in reverted_dict:
            self.interval[id_] = (len(self.reverted_dict[id_])) ** 0.5

    def skip_list(self):
        pass
    #node = skip_node(id_,next_node,down)
    pass
