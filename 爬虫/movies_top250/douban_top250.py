#!/usr/bin/python2.7
# encoding='utf-8'

import codecs,time
from pyquery import PyQuery as pq
DOWNLOAD_URL = 'https://movie.douban.com/top250'

def parse_html(url):
    p_h_start = time.time()
    html = pq(url = url)
    p_h_step1 = time.time()
    print 's1: cost %ss' % (p_h_step1 - p_h_start)
    top_name_items = html('ol.grid_view li div.hd span.title,.other')
    top_name_list = []
    p_h_step2 = time.time()
    print 's2: cost %ss' % (p_h_step2 - p_h_step1)
    n = 0
    for item in top_name_items.items():
        if item.text()[0] == '/':
            top_name = top_name_list.pop() + item.text()[1] + item.text()
            top_name_list.append(top_name)
        else:
            top_name_list.append(item.text())
    next_page = html('div.paginator span.next a').attr('href')
    p_h_end = time.time()
    print 'parse_html cost %ss' % (p_h_end - p_h_start)
    if next_page:
        return top_name_list, DOWNLOAD_URL + next_page
    return top_name_list, None

if __name__ == '__main__':
    start_time = time.time()
    url = DOWNLOAD_URL
    with codecs.open('top250','wb',encoding='utf-8') as fp:
        while url:
            movies, url = parse_html(url)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))
    end_time = time.time()
    print 'Cost %s seconds.' % (end_time - start_time)

#print html('ol.grid_view li div.hd span.title').text()