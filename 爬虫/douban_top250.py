#!/usr/bin/python2.7
# encoding=utf-8

import codecs
from pyquery import PyQuery as pq
DOWNLOAD_URL = 'https://movie.douban.com/top250'

def parse_html(url):
    html = pq(url = url)
    top_name_items = html('ol.grid_view li div.hd span.title,.other')
    top_name_list = []
    for item in top_name_items.items():
        if item.text()[0] == '/':
            top_name = top_name_list.pop() + '  ' + item.text()
            top_name_list.append(top_name)
        else:
            top_name_list.append(item.text())
    next_page = html('div.paginator span.next a').attr('href')
    if next_page:
        return top_name_list, DOWNLOAD_URL + next_page
    return top_name_list, None

if __name__ == '__main__':
    url = DOWNLOAD_URL
    with codecs.open('top250','wb',encoding='utf-8') as fp:
        while url:
            movies, url = parse_html(url)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))


#print html('ol.grid_view li div.hd span.title').text()