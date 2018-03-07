#!/usr/bin/python2.7
import os
import sys

def search_dir(keyword,path):
    for i in os.listdir(path):
        new_path=os.path.join(path,i)
        if os.path.isdir(new_path):
            search_dir(keyword,new_path)
        else:
            if keyword in new_path:
                print new_path[2:]

keyword=sys.argv[1]
path='.'

search_dir(keyword,path)