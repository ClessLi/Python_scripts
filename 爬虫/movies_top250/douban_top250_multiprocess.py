#!/usr/bin/python2.7
# encoding='utf-8'

import codecs, time, multiprocessing
from multiprocessing import Pool
from pyquery import PyQuery as pq
from threading import Thread

DOWNLOAD_URL = 'https://movie.douban.com/top250'

def parse_html(url):
    html = pq(url = url)
    top_name_items = html('ol.grid_view li div.hd span.title,.other')
    top_name_list = []
    for item in top_name_items.items():
        if item.text()[0] == '/':
            top_name = top_name_list.pop() + item.text()[1] + item.text()
            top_name_list.append(top_name)
        else:
            top_name_list.append(item.text())
    next_page = html('div.paginator span.next a').attr('href')
    if next_page:
        return top_name_list, DOWNLOAD_URL + next_page
    return top_name_list, None

def parse_test_page(url):
    t_p_start = time.time()
    html = pq(url)
    t_p_step = time.time()
    print 't_p_step cost %ss' % (t_p_step - t_p_start)
    pages = [url]
    #pages = html('div.paginator a').attr('href')
    links = html('div.paginator')#.find('span').remove()
#    links.find('span').remove()
    links('span').remove()
    t_p_step = time.time()
    print 't_p_step cost %ss' % (t_p_step - t_p_start)
    for link in links('a').items():
        pages.append(url + link.attr('href'))
    t_p_end = time.time()
    print 'test_page cost %ss' % (t_p_end - t_p_start)
    return pages

def parse_test_html(url):
    start = time.time()
    html = pq(url)
    step = time.time()
    top_name_items = html('ol.grid_view li div.hd span.title,.other')
    top_name_list = []
    for item in top_name_items.items():
        if item.text()[0] == '/':
            top_name = top_name_list.pop() + item.text()[1] + item.text()
            top_name_list.append(top_name)
        else:
            top_name_list.append(item.text())
    end = time.time()
    print 'step cost %ss, all cost %ss' % (step - start, end - start)
    #print top_name_list

def save_data(p,url,movies):
    with codecs.open('top250_multi','wb',encoding='utf-8') as fp:
        while url:
            movies, url = p.apply_async(parse_html,args=(url,))
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))
        p.close()
        p.join()

def main_test(DOWNLOAD_URL):
    start_time = time.time()
    url = DOWNLOAD_URL
    #p = Pool()
    threads = []
    #movies = []
    #print parse_test_page(url)
    #save_data(p,url,movies)
    s_start = time.time()
    print 'to subproccess cost %ss' % (s_start - start_time)
    for i in parse_test_page(url):
        t = Thread(target=parse_test_html, args=[i])
        t.start()
        threads.append(t)
        #p.apply_async(parse_test_html, args=(i,))
    for t in threads:
        t.join()
    s_end = time.time()
    #p.close()
    #p.join()
    end_time = time.time()
    print 'Cost %s seconds.subproccess cost %ss,subproccess_wait cost %ss' % (end_time - start_time, s_end - s_start, end_time - s_end)

if __name__ == '__main__':
    main_test(DOWNLOAD_URL)

#print html('ol.grid_view li div.hd span.title').text()