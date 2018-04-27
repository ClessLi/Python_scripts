#!/home/cless/python2.7/bin/python2.7
# encoding:utf-8

from pyquery import PyQuery as pq
import re
import time
import urllib2
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

url = 'http://ac.qq.com/Comic/ComicInfo/id/17114'
nodes = 'ol.chapter-page-new.works-chapter-list li p span.works-chapter-item a'
re_compile = re.compile(r'.*[0](\d+).*')
doc = pq(url)
episodes = re_compile.match(doc(nodes).eq(-1).text()).group(1)
play_url = 'http://' + url.split('/')[2] + doc(nodes).eq(-1).attr('href')
print episodes,play_url
doc2 = pq(play_url)
print doc2('ul#comicCotain.comic-contain li')

psj_path = 'F:\\Program Files (x86)\\phantomjs\\bin\\phantomjs.exe'
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36")
#dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/4.0 (compatible; MSIE 5.5; windows NT)")
browser = webdriver.PhantomJS(psj_path,desired_capabilities=dcap)
browser.get(play_url)
print dcap
o_data = browser.page_source
o_doc = pq(o_data)
page_num = int(o_doc('div#mainView.main ul#comicContain.comic-contain li span.comic-ft').eq(1).text().split('/')[-1])
page_height = int(o_doc('ul#comicContain.comic-contain li img.loaded').eq(1).attr('data-h')) + 50
#print page_num,type(page_num)
for n in xrange(0,page_num):
    js = 'window.scrollTo(0,' + str(page_height * n) + ')'
    browser.execute_script(js)
    time.sleep(0.1)

#将打开的界面截图保存，方便观察
#a = browser.get_screenshot_as_file('test.png')

#获取当前页面所有源码（此时包含触发出来的异步加载的资源）
data = browser.page_source
#print data
#将相关网页源码写入本地文件中，方便分析
#with open('test.html','wb') as test_fp:
#    test_fp.write(data)
doc = pq(data)
cur_page_num = 1
#print doc('ul#comicContain.comic-contain li img.loaded').items().attr('src')
for item in doc('ul#comicContain.comic-contain li img.loaded').items():
    #print item.attr('src'),type(item.attr('src'))
    img_url = item.attr('src')
    extension = img_url.split('.')[-1]
    file_name = str(cur_page_num) + '.' + extension
    img = urllib2.urlopen(img_url).read()
    with open(file_name, 'wb') as img_fp:
        img_fp.write(img)
    cur_page_num += 1
browser.quit()