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

doc = pq(url='https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8')
tg_dict_data = json.loads(doc('p').text())['data']
#totalPage = tg_dict_data['totalPage']
for data in tg_dict_data['searchDOList']:
#    city = data['city']
#data = tg_dict_data['searchDOList'][0]
    name = data['realName']
    city = data['city']
    height = data['height']
    weight = data['weight']
    img_url = 'https:'+data['avatarUrl']
    file_name = '%s_%s_%skg_%scm' % (name,city,weight,height)
    save_Img(img_url,file_name)
#print data
#print img_url
#print file_name
#print type(img_url)
#print "%s %s" % (Img_url,city)