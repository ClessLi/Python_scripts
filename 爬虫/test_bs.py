from bs4 import BeautifulSoup as bs
import urllib
import re
from pyquery import PyQuery as pq
from pybloom import BloomFilter
bf = BloomFilter(capacity=1000,error_rate=0.001)
url = 'http://www.baidu.com'
bf.add(url)
level = 0

#html = urllib.urlopen(url)
#soup = bs(html,'lxml')
#init_html = soup.prettify()
#doc = pq(init_html)
#print doc
def search_url(url,max_level,level=0):
    try:
        print '|'+'-'*level+url
        doc = pq(url = url)
        pq_items = doc('[href]').items()
        for item in pq_items:
            url_new = item.attr('href')
            if re.findall(r'https?.+',url_new) and url_new not in bf and level < max_level:
                new_level = level + 1
                bf.add(url_new)
                search_url(url_new,max_level=max_level,level=new_level)
    except:
        return False
search_url(url,max_level=2)
#    print item.attr('href') if _re
