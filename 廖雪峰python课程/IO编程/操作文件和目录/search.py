#!/usr/bin/python2.7
#加载os、sys模块
import os
import sys

#递归查询path下所有文件路径，并匹配关键字keyword
def search_dir(keyword,path):
    for i in os.listdir(path):
        new_path=os.path.join(path,i)
        if os.path.isdir(new_path):
            search_dir(keyword,new_path)
        else:
            if keyword in new_path:
                print new_path[2:]

#将程序第一个参数传给keyword
keyword=sys.argv[1]
#获取当前目录路径
path='.'

#运行程序
search_dir(keyword,path)