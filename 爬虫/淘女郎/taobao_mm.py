#!/home/cless/python2.7/bin/python2.7
# encoding:utf-8
from pyquery import PyQuery as pq
from pymongo import MongoClient
import json , urllib2 , time
#doc = pq(url='https://mm.taobao.com/search_tstar_model.htm?spm=719.6642093.1998089564.7.WIj7L7')
#print doc('div.lady-girls-wrap.tb_mm_main ul.girls-list')

class TaoGirl():
    def __init__(self,url):
        self.index_url = url
        self.db_host = '192.168.220.83:27017'
        self.db_name = 'tao_girl'
        self.col_name = 'tao_girl_info'
        self.db_user = 'worker'
        self.db_user_pwd = 'more_work'
        self.mongodb_conn(self.db_host,self.db_name,self.col_name,self.db_user,self.db_user_pwd)
        self.doc = pq(url=self.index_url)
        self.data = json.loads(self.doc('p').text())
        self.page_status = self.data['status']

    def mongodb_conn(self,db_host,db_name,col_name,db_user,db_user_pwd):
        self.MONGO_CONN = MongoClient(db_host)
        self.tao_girl_db = self.MONGO_CONN[db_name]
        self.tao_girl_db.authenticate(db_user,db_user_pwd)
        self.tao_girl_info = self.tao_girl_db[col_name]

    def mongodb_update(self,col_name,document):
        if col_name and document:
            self.tao_girl_info.update_one(
                filter = {'_id':document['userid']},
                update = {'$set':document},
                upsert = True
            )

    def save_Img(self,img_url,file_name):
        if 'jpeg' in img_url:
            file_suffix = '.jpeg'
        elif 'jpg' in img_url:
            file_suffix = '.jpg'
        elif 'png' in img_url:
            file_suffix = '.png'
        else:
            file_suffix = '.bmp'
        self.cat_img = urllib2.urlopen(img_url).read()
        self.file_name = file_name + file_suffix
        self.db_document['filename'] = self.file_name
        with open(self.file_name,'wb') as self.img:
            self.img.write(self.cat_img)
            self.mongodb_update(self.col_name,self.db_document)

    def parse_data(self):
        self.totalPage = self.data['data']['totalPage']
        self.page = self.data['data']['currentPage']
        #while self.page_status == 1 and self.page <= self.totalPage:
        while self.page_status == 1 and self.page <= 1:
                self.img_list = self.data['data']['searchDOList']
                self.page += 1
                for item in self.img_list:
                    self.userid = item['userId']
                    self.name = item['realName']
                    self.city = item['city']
                    self.height = item['height']
                    self.weight = item['weight']
                    self.img_url = 'https:'+item['avatarUrl']
                    self.file_name = '%s_%s_%skg_%scm' % (self.name,self.city,self.weight,self.height)
                    self.db_document = {'userid':self.userid,
                                        'name':self.name,
                                        'city':self.city,
                                        'height':self.height,
                                        'weight':self.weight,
                                        'img_url':self.img_url}
                    print 'Downloading file:%s, url:%s' % (self.file_name,self.img_url)
                    self.save_Img(self.img_url,self.file_name)
                self.url_new = self.index_url + '&currentPage=' + str(self.page)
                #time.sleep(1)
                print 'The url of the next page is %s(page number:%s, page status:%s)' % (self.url_new,self.page,self.page_status)
                try:
                    self.doc = pq(url=self.url_new)
                except:
                    return False
                self.data = json.loads(self.doc('p').text())
                self.page_status = self.data['status']

if __name__ == '__main__':
    tao_girl_url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
    taogirl_data=TaoGirl(tao_girl_url)
    print taogirl_data.index_url
    taogirl_data.parse_data()
#totalPage = tg_dict_data['totalPage']
#    city = data['city']
#data = tg_dict_data['searchDOList'][0]
#print data
#print img_url
#print file_name
#print type(img_url)
#print "%s %s" % (Img_url,city)
