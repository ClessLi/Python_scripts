# encoding:utf-8
from pyquery import PyQuery as pq
import json
import urllib2
#doc = pq(url='https://mm.taobao.com/search_tstar_model.htm?spm=719.6642093.1998089564.7.WIj7L7')
#print doc('div.lady-girls-wrap.tb_mm_main ul.girls-list')
def save_Img(img_url,file_name):
    if 'jpeg' in img_url:
        file_suffix = '.jpeg'
    elif 'jpg' in img_url:
        file_suffix = '.jpg'
    elif 'png' in img_url:
        file_suffix = '.png'
    else:
        file_suffix = '.bmp'
    cat_img = urllib2.urlopen(img_url).read()
    with open(file_name + file_suffix,'wb') as img:
        img.write(cat_img)

def parse_data(url):
    doc = pq(url=url)
    data = json.loads(doc('p').text())
    page_status = data['status']
    totalPage = data['data']['totalPage']
    page = data['data']['currentPage']
    while page_status == 1 and page <= totalPage:
            img_list = data['data']['searchDOList']
            page += 1
            for item in img_list:
                name = item['realName']
                city = item['city']
                height = item['height']
                weight = item['weight']
                img_url = 'https:'+item['avatarUrl']
                file_name = '%s_%s_%skg_%scm' % (name,city,weight,height)
                print file_name,img_url
                save_Img(img_url,file_name)
            print page_status,page
            url_new = url + '&currentPage=' + str(page)
            print url_new
            doc = pq(url=url_new)
            data = json.loads(doc('p').text())
            page_status = data['status']

if __name__ == '__main__':
    tao_girl_url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
    parse_data(tao_girl_url)
#totalPage = tg_dict_data['totalPage']
#    city = data['city']
#data = tg_dict_data['searchDOList'][0]
#print data
#print img_url
#print file_name
#print type(img_url)
#print "%s %s" % (Img_url,city)