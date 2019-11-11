#!/home/cless/python2.7/bin/python2.7
# encoding:utf-8

from pyquery import PyQuery as pq
import re
import time
import urllib2
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pymongo import MongoClient
import os

class BingeWatching():
    def __init__(self,index_url):
        self.psj_path = 'F:\\Program Files (x86)\\phantomjs\\bin\\phantomjs.exe'
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
        self.index_url = index_url
        self.episodes_node = ''
        self.page_num_node = ''
        self.page_height_node = ''
        self.download_url_node = ''
        self.path = u'追番'
        self.episodes_re = re.compile(r'.*[0](\d+).*')
        self.db_host = '192.168.220.83:27017'
        self.db_name = 'binge_watching'
        self.db_user = 'worker'
        self.db_user_pwd = 'more_work'
        self.db_col_name = 'test'
        self.__mongodb_conn__(self.db_host, self.db_name, self.db_user, self.db_user_pwd)

    def __mongodb_conn__(self,db_host,db_name,db_user,db_user_pwd):
        self.MONGO_CONN = MongoClient(db_host)
        self.MONGO_DB = self.MONGO_CONN[db_name]
        self.MONGO_DB.authenticate(db_user,db_user_pwd)

    def __mongodb_update__(self,col_name,document):
        if col_name and document:
            MONGO_COL = self.MONGO_DB[col_name]
            MONGO_COL.update_one(
                filter = {'_id':document['_id']},
                update = {'$set':document},
                upsert = True
            )
    def __mongodb_find__(self,col_name,query,projection):
        if col_name and query:
            MONG_COL = self.MONGO_DB[col_name]
            return MONG_COL.find(query,projection)

    def update(self,index_url, re_rule):
        pq_index = pq(index_url)
        page_url = re_rule.match(pq_index(self.episodes_node).eq(-1).text()).group(1)
        pq_page = self.parse_page(page_url)
        self.download_data(pq_page,self.download_url_node)

    def download_data(self,pq_page,download_url_node):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        n = 1
        for item in pq_page(download_url_node).items():
            file_name = str(n)
            file = urllib2.urlopen(item).read()
            with open(self.path + '\\' + file_name, 'wb') as file_fp:
                file_fp.write(file)
            n += 1

    def parse_page(self,page_url):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (self.userAgent)
        browser = webdriver.PhantomJS(self.psj_path, desired_capabilities=dcap)
        browser.get(page_url)

        _init_pq_page = pq(browser.page_source)
        page_num = int(_init_pq_page(self.page_num_node).eq(1).text().split('/')[-1])
        page_height = int(_init_pq_page(self.page_height_node).eq(1).attr('data-h')) + 50
        for n in xrange(0, page_num):
            js = 'window.scrollTo(0,' + str(page_height * n) + ')'
            browser.execute_script(js)
            time.sleep(0.1)
        pq_page = pq(browser.page_source)
        browser.close()
        return pq_page

class BingeWatching_shixiong(BingeWatching):
    def __init__(self,index_url = 'http://ac.qq.com/Comic/ComicInfo/id/17114'):
        BingeWatching.__init__(self,index_url)
        self.episodes_node = 'ol.chapter-page-new.works-chapter-list li p span.works-chapter-item a'
        self.page_num_node = 'ul#comicContain.comic-contain li span.comic-ft'
        self.page_height_node = 'ul#comicContain.comic-contain li img.loaded'
        self.comic_img_url_node = 'ul#comicContain.comic-contain li img.loaded'
        self.path = self.path + u'\\尸兄'
        self.db_col_name = 'comic'

    def __mongodb_find__(self,col_name,query,projection):
        if col_name and query:
            MONG_COL = self.MONGO_DB[col_name]
            return MONG_COL.find(query,projection)

    def __mongodb_update__(self,col_name,document):
        if col_name and document:
            MONGO_COL = self.MONGO_DB[col_name]
            MONGO_COL.update_one(
                filter={'name': document.get('name')},
                update={'$push': {'episodes': document.get('episodes')}},
                upsert=True
            )

    def get_episodes(self):
        query = {'name': u'尸兄'}
        projection = {'episodes': 1, '_id': 0}
        for item in self.__mongodb_find__(self.db_col_name, query, projection):
            return max(item.get('episodes'))

    def update_episodes(self, episodes):
        document = {'name': u'尸兄', 'episodes': episodes}
        self.__mongodb_update__(self.db_col_name, document)

    def update(self):
        pq_index = pq(self.index_url)
        episodes = int(self.episodes_re.match(pq_index(self.episodes_node).eq(-1).text()).group(1))
        episodes_old = self.get_episodes()
        if episodes > episodes_old:
            comic_page_url = 'http://' + self.index_url.split('/')[2] + pq_index(self.episodes_node).eq(-1).attr('href')
            pq_comic_page = self.parse_page(comic_page_url)
            if self.download_data(pq_comic_page,self.comic_img_url_node, episodes):
                self.update_episodes(episodes)
                print 'Updating Successful (the ' + str(episodes) + ' EP of ShiXiong)'
                return True
            else:
                print 'Updating failed'
                return False
        else:
            print 'The ' + str(episodes_old) + ' EP is the lastest one'
            return False

    def download_data(self,pq_page,download_url_node,episodes):
        download_path = self.path + u'\\第' + str(episodes) + u'话\\'
        if not os.path.exists(download_path):
            os.makedirs(download_path)
        cur_page_num = 1
        for item in pq_page(download_url_node).items():
            img_url = item.attr('src')
            extension = img_url.split('.')[-1]
            file_name = str(cur_page_num) + '.' + extension
            img = urllib2.urlopen(img_url).read()
            with open(download_path + file_name, 'wb') as img_fp:
                img_fp.write(img)
            cur_page_num += 1
        return True

if __name__ == "__main__":
    shixiong_update = BingeWatching_shixiong()
    #EP = shixiong_update.get_episodes()
    #print EP,type(EP)
    shixiong_update.update()
