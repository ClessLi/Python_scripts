#!/home/cless/python2.7/bin/python2.7
# encoding:utf-8
from pyquery import PyQuery as pq
from pymongo import MongoClient
import json , urllib2 , time
import re

class TaoGirl():
    def __init__(self,url):
        self.index_url = url
        self.db_host = '192.168.220.83:27017'
        self.db_name = 'tao_girl'
        self.db_user = 'worker'
        self.db_user_pwd = 'more_work'
        self.mongodb_conn(self.db_host,self.db_name,self.db_user,self.db_user_pwd)
        self.c_page = 1
        self.row = 0

    def mongodb_conn(self,db_host,db_name,db_user,db_user_pwd):
        self.MONGO_CONN = MongoClient(db_host)
        self.MONGO_DB = self.MONGO_CONN[db_name]
        self.MONGO_DB.authenticate(db_user,db_user_pwd)

    def mongodb_update(self,col_name,document):
        if col_name and document:
            MONGO_COL = self.MONGO_DB[col_name]
            MONGO_COL.update_one(
                filter = {'_id':document['userid']},
                update = {'$set':document},
                upsert = True
            )

    def mongodb_find(self,col_name,query,projection):
        if col_name and query:
            MONG_COL = self.MONGO_DB[col_name]
            return MONG_COL.find(query,projection)

    def save_data(self,data,col_name):
        img_url = data.get('db_document').get('img_url')
        file_name = data.get('file_name')
        db_document = data.get('db_document')
        cat_img = urllib2.urlopen(img_url).read()
        db_document['filename'] = file_name
        with open(file_name,'wb') as img:
            img.write(cat_img)
            self.mongodb_update(col_name,db_document)

    def parse_data(self,url,page_max):
        while self.c_page <= page_max:
            doc = pq(url=url)
            data = json.loads(doc('p').text())
            page_status = data['status']
            if page_status != 1:
                break
            total_page = data['data']['totalPage']
            page_max = page_max if page_max<total_page else total_page
            for item in data['data']['searchDOList']:
                userid = item['userId']
                name = item['realName']
                city = item['city']
                height = item['height']
                weight = item['weight']
                img_url = 'https:' + item['avatarUrl']
                file_title = '%s_%s_%skg_%scm' % (name, city, weight, height)
                file_name = file_title + '.' + img_url.split('.')[-1]
                yield {
                    'file_name':file_name,
                    'db_document':{
                       'userid':userid,
                        'name':name,
                        'city':city,
                        'height':height,
                        'weight':weight,
                        'img_url':img_url
                    }
                }
                self.c_page = data['data']['currentPage'] + 1
                url = self.index_url + '&currentPage=' + str(self.c_page)

    def download(self,page_max = 99999999,row_max = 999999999999):
        gen_data = self.parse_data(self.index_url,page_max)
        if gen_data:
            for data in gen_data:
                print 'Downloading file:%s, url:%s' % (data.get('file_name'),data.get('db_document').get('img_url'))
                self.save_data(data,'tao_girl_info')
                print 'Download successful.[%s]' % data.get('db_document').get('userid')
                self.row += 1
                print self.row
                if self.row >= row_max:
                    break

class TaoGirl_model_info(TaoGirl):
    def save_data(self,data,col_name):
        userid = data.get('db_document').get('userid')
        db_document = {'userid':userid}
        url = 'https://mm.taobao.com/self/info/model_info_show.htm?user_id=' + str(userid)
        info_index_url = 'https://mm.taobao.com/self/model_info.htm?user_id=' + str(userid)
        bmi = float(data.get('db_document').get('weight')[:-2]) / float(data.get('db_document').get('height')[:-2]) ** 2 / 10000
        doc = pq(url)
        mm_info = doc('ul.mm-p-info-cell.clearfix li').items()
        for item in mm_info:
            if item('label').text() and item('span').text() and '>0<' not in str(item('.price')):
                db_document[item('label').text()] = item('span').text()
            elif item('p').text():
                db_document[item.attr('class').split('-')[-1]] = item('p').text()
        if db_document.get('bar'):
            db_document['bra'] = db_document.pop('bar')
        if db_document.get('shose'):
            db_document['shoes'] = db_document.pop('shose')
        db_document['index_url'] = info_index_url
        db_document['bmi'] = bmi
        self.mongodb_update(col_name,db_document)

    def download(self,page_max = 99999999,row_max = 999999999999):
        gen_data = self.parse_data(self.index_url,page_max)
        if gen_data:
            for data in gen_data:
                self.save_data(data,'tao_girl_model_info')
                self.row += 1
                print self.row
                if self.row >= row_max:
                    break

    def find_girl(self,size):
        re_rule = '[0-9]+[' + size.lower() + '-z' + size.upper() + '-Z]$'
        regex = re.compile(re_rule)
        query = {'bra':regex}
        projection = {'bra':1,'height':1,'weight':1,'index_url':1}
        girl_data = self.mongodb_find('tao_girl_model_info',query,projection)
        for item in girl_data:
            height = item.get('height')
            weight = item.get('weight')
            bmi = float(weight[:-2]) / float(height[:-2]) ** 2 * 10000
            item['bmi'] = bmi
            if bmi < 25:
                print 'BMI:' + str(item['bmi']),item['bra'],item['index_url']

if __name__ == '__main__':
    tao_girl_url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
#    taogirl_data=TaoGirl(tao_girl_url)
    taogirl_data = TaoGirl_model_info(tao_girl_url)
    print taogirl_data.index_url
    page_max = 10
    row_max = 1
#    help(taogirl_data.MONGO_DB['test'].find)
#    size = 'f'
#    re_size = '.+[' + size.lower() + '-z' + size.upper() + '-Z]$'
#    rexExp = re.compile(re_size)
#    for info in taogirl_data.MONGO_DB['tao_girl_model_info'].find(
#        {'bra':rexExp},
#        {'bra':1,'height':1,'weight':1,'index_url':1}
#    ):
#        print info
    taogirl_data.find_girl('e')
    #taogirl_data.download(page_max,row_max)
    #taogirl_data.download()

