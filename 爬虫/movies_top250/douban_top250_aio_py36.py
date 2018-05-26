#!/usr/bin/python3.6
# encoding='utf-8'

import codecs, time, aiohttp, asyncio
from aiohttp import web
from pyquery import PyQuery as pq

DOWNLOAD_URL = 'https://movie.douban.com/top250'

@asyncio.coroutine
async def get_html(url):
    start = time.time()
    print(start)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            html = await resp.text()
            end = time.time()
            print('%s Cost %s seconds.' % ('get_html',end - start))
            return pq(html)
@asyncio.coroutine
async def get_page(pages):
    start = time.time()
    index_pq = await get_html(pages[0])
    links = index_pq('div.paginator')
    links('span').remove()
    for link in links('a').items():
        pages.append(pages[0] + link.attr('href'))
    end = time.time()
    print('%s Cost %s seconds.' % ('get_page',end - start))
@asyncio.coroutine
async def parse_html(url, top_name_list, list_index):
    start = time.time()
    html_pq = await get_html(url)
    top_name_items = html_pq('ol.grid_view li div.hd span.title,.other')
    item_list = []
    for item in top_name_items.items():
        if item.text()[0] == '/':
            top_name = item_list.pop() + item.text()[1] + item.text()
            item_list.append(top_name)
        else:
            item_list.append(item.text())
    top_name_list[list_index] = item_list
    end = time.time()
    print(end)
    print('%s Cost %s seconds.' % ('parse_html',end - start))

def save_data(top_name_list):
    start = time.time()
    movies = []
    for list_index in range(len(top_name_list)):
        movies.extend(top_name_list[list_index])
    with codecs.open('top250_aio','wb',encoding='utf-8') as fp:
        fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))
    end = time.time()
    print('%s Cost %s seconds.' % ('save_data',end - start))

def main(index_url):
    start_time = time.time()
    pages = [index_url]
    tasks = [get_page(pages)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    pages_num = len(pages)
    top_name_list = [[]] * pages_num
    tasks = [parse_html(pages[list_index], top_name_list, list_index) for list_index in range(pages_num)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    save_data(top_name_list)
    end_time = time.time()
    print('Cost %s seconds.' % (end_time - start_time))

if __name__ == '__main__':
    main(DOWNLOAD_URL)
