#!/home/cless/python2.7/bin/python2.7
# encoding:utf-8
from pyquery import PyQuery as pq
from pymongo import MongoClient
import json , urllib2 , time

class TaoGirl():
    def __init__(self,url):
        self.index_url = url
        self.db_host = '192.168.220.83:27017'
        self.db_name = 'tao_girl'
        self.col_name = 'tao_girl_info'
        self.db_user = 'worker'
        self.db_user_pwd = 'more_work'
        self.mongodb_conn(self.db_host,self.db_name,self.col_name,self.db_user,self.db_user_pwd)
        self.c_page = 1
        self.row = 0

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

    def save_Img(self,save_data,col_name):
        img_url = save_data.get('db_document').get('img_url')
        file_name = save_data.get('file_name')
        db_document = save_data.get('db_document')
        cat_img = urllib2.urlopen(img_url).read()
        db_document['filename'] = file_name
        with open(file_name,'wb') as img:
            img.write(cat_img)
            self.mongodb_update(col_name,db_document)

    def parse_data(self,url,page_max):
        page_status = 1
        while page_status == 1 and self.c_page <= page_max:
            doc = pq(url=url)
            data = json.loads(doc('p').text())
            page_status = data['status']
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

    def save_data(self,page_max = 99999999,row_max = 999999999999):
        gen_data = self.parse_data(self.index_url,page_max)
        if gen_data:
            for save_data in gen_data:
                print 'Downloading file:%s, url:%s' % (save_data.get('file_name'),save_data.get('db_document').get('img_url'))
                self.save_Img(save_data,self.col_name)
                print 'Download successful.[%s]' % save_data.get('db_document').get('userid')
                self.row += 1
                if self.row >= row_max:
                    break


if __name__ == '__main__':
    tao_girl_url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
    taogirl_data=TaoGirl(tao_girl_url)
    print taogirl_data.index_url
    page_max = 1
    row_max = 10
    taogirl_data.save_data(page_max,row_max)
