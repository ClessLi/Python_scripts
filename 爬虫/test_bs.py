from bs4 import BeautifulSoup as bs
import urllib
import re
from pyquery import PyQuery as pq
from pybloom import BloomFilter
#bf = BloomFilter()
url = 'http://www.baidu.com'

#html = urllib.urlopen(url)
#soup = bs(html,'lxml')
#init_html = soup.prettify()
#doc = pq(init_html)
#print doc
def search_url(url):
    try:

        doc = pq(url = url)
        pq_items = doc('[href]').items()
        for item in pq_items:
            url_new = item.attr('href')
            if re.findall(r'https?.+',url_new):
                print url_new
                search_url(url_new)
    except:
        return False
search_url(url)
#    print item.attr('href') if _re
