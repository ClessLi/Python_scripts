# coding: utf-8
from bs4 import BeautifulSoup as bs
from pyquery import PyQuery as pq
import requests, aiohttp, asyncio, json, lxml, re
SOURCE = '19552207'
USER_AGENT = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
REFERER = "https://www.zhihu.com/topic/%s/newest" % SOURCE
AUTHORIZATION = "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
URL_QUERY = "?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.comment_count&limit=" + str(5)

url = 'https://www.zhihu.com/api/v4/topics/%s/feeds/timeline_activity' % SOURCE + URL_QUERY
async def fetch_activities(url):
    try:
        headers = {
                "User-Agent": USER_AGENT,
                "Referer": REFERER,
                "authorization": AUTHORIZATION
                }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                s = await resp.read()
    except Exception as e:
        print("fetch last activities fail. " + url)
        raise e

    return s
async def main(url):
    s = await fetch_activities(url)
    s_json = json.loads(s)
    datas = s_json['data']
    list = []
    for data in datas:
        target = data['target']
        if "content" not in target or "question" not in target or "author" not in target:
            continue
        question_title = target["question"]["title"]

        author_name = target["author"]["name"]
        print("current answer: " + question_title + " author: " + author_name)
        print(target['content'])
        html = pq(target['content'])
        seq = 0
        images = html('img').items()
        for item in images:
            image = str(item.attr('src'))
            if not image.startswith('http'):
                continue
            s = await fetch_activities(image)
            filename = author_name + '--' + question_title + ('--%d' % seq) + '.jpg'
            filename = re.sub(r'(?u)[^-\w.]', '_', filename)
            seq += 1
            with open(filename,'wb') as fd:
                fd.write(s)
        #list.append(images)
    #print(list)
loop = asyncio.get_event_loop()
tasks = [main(url)]
loop.run_until_complete(asyncio.wait(tasks))
