# coding: utf-8

import time
import os
import re
import requests
import aiohttp, asyncio, json, base64, aiofiles
from pyquery import PyQuery as pq
from threading import Thread

# 百度云 人脸检测 申请信息
# 唯一必须填的信息就这三行
APP_ID = "11376646"
API_KEY = "mTv3FKRqMD84j4apKh0wDMLR"
SECRET_KEY = "mPV4F7U9zmtOC4gctop2y8LgrbigOPWh"

# 文件存放目录名，相对于当前目录
DIR = "image"
# 过滤颜值阈值，存储空间大的请随意
BEAUTY_THRESHOLD = 45

# 浏览器中打开知乎，在开发者工具复制一个，无需登录
# 如何替换该值下文有讲述
AUTHORIZATION = "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"

# 以下皆无需改动

# 每次请求知乎的讨论列表长度，不建议设定太长，注意节操
LIMIT = 5

# 这是话题『美女』的 ID，其是『颜值』（20013528）的父话题
SOURCE = "19552207"

# 爬虫假装下正常浏览器请求
USER_AGENT = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.5 Safari/534.55.3"
# 爬虫假装下正常浏览器请求
REFERER = "https://www.zhihu.com/topic/%s/newest" % SOURCE
# 某话题下讨论列表请求 url
BASE_URL = "https://www.zhihu.com/api/v4/topics/%s/feeds/timeline_activity"
# 初始请求 url 附带的请求参数
URL_QUERY = "?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.comment_count&limit=" + str(LIMIT)


async def fetch(url):
    try:
        headers = {
            "User-Agent": USER_AGENT,
            "Referer": REFERER,
            "authorization": AUTHORIZATION
        }
#       s = requests.get(url, headers=headers)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                s = await resp.read()
    except Exception as e:
        print("fetch last activities fail. " + url)
        raise e

    return s

# 指定 url，获取对应原始内容 / 图片
async def fetch_image(url):
    s = await fetch(url)
    return s

# 指定 url，获取对应 JSON 返回 / 话题列表
async def fetch_activities(url):
    s = await fetch(url)
    return json.loads(s)


# 处理返回的话题列表
async def process_activities(datums, face_detective, event_loop):
    for data in datums["data"]:

        target = data["target"]
        if "content" not in target or "question" not in target or "author" not in target:
            continue

        # 解析列表中每一个元素的内容
        html = pq(target['content'])

        seq = 0

        # question_url = target["question"]["url"]
        question_title = target["question"]["title"]

        author_name = target["author"]["name"]
        # author_id = target["author"]["url_token"]

        print("current answer: " + question_title + " author: " + author_name)

        # 获取所有图片地址
        images = html('img').items()
        for item in images:
            image = str(item.attr('src'))
            if not image.startswith("http"):
                continue
            s = await fetch_image(image)

            # 请求人脸检测服务
            scores = await face_detective(s)

            async def download_image (filename):
                async with aiofiles.open(os.path.join(DIR, filename), "wb") as fd:
                    await fd.write(s)
            for score in scores:
                filename = ("%d--" % score) + author_name + "--" + question_title + ("--%d" % seq) + ".jpg"
                filename = re.sub(r'(?u)[^-\w.]', '_', filename)
                # 注意文件名的处理，不同平台的非法字符不一样，这里只做了简单处理，特别是 author_name / question_title 中的内容
                seq = seq + 1
                asyncio.run_coroutine_threadsafe(download_image(filename),event_loop)
            # 人脸检测 免费，但有 QPS 限制
            await asyncio.sleep(5.0)

    if not datums["paging"]["is_end"]:
        # 获取后续讨论列表的请求 url
        return datums["paging"]["next"]
    else:
        return None


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '_', s)


async def detect_face(image, token):
    try:
        URL = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        image = base64.b64encode(image)
        #print(image)
        params = {
            "access_token": token
        }
        data = {
            "face_field": "age,gender,beauty,qualities",
            "image": image,
            "image_type": "BASE64"
        }
        s = requests.post(URL, params=params, data=data)
        #print(s.json())
        return s.json()["result"]
#        async with aiohttp.ClientSession() as session:
#            async with session.post(URL, params=params, data=data) as resp:
#                s = await resp.read()
#        print(json.loads(s))
#        return json.loads(s)["result"]
    except Exception as e:
        print("detect face fail. " + URL)
        raise e

async def fetch_auth_token(api_key, secret_key):
    try:
        URL = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
                "grant_type": "client_credentials",
                "client_id": api_key,
                "client_secret": secret_key
                }
        async with aiohttp.ClientSession() as session:
            async with session.post(URL, params=params) as resp:
                s = await resp.read()
        return json.loads(s)["access_token"]
    except Exception as e:
        print("fetch baidu auth token fail. " + URL)
        raise e

async def init_face_detective(app_id, api_key, secret_key):
    #client = AipFace(app_id, api_key, secret_key)
    # 百度云 V3 版本接口，需要先获取 access token
    token = await fetch_auth_token(api_key, secret_key)
    async def detective(image):
        #r = client.detect(image, options)
        # 直接使用 HTTP 请求
        r = await detect_face(image, token)
        #如果没有检测到人脸
        if r is None or r["face_num"] == 0:
            return []

        print('face_num' + str(r['face_num']))
        scores = []
        for face in r["face_list"]:
            print(face['beauty'])
            #人脸置信度太低
            if face["face_probability"] < 0.6:
                continue
            #颜值低于阈值
            if face["beauty"] < BEAUTY_THRESHOLD:
                continue
            #性别非女性
            if face["gender"]["type"] != "female":
                continue
            scores.append(face["beauty"])

        return scores

    return detective


def init_env():
    if not os.path.exists(DIR):
        os.makedirs(DIR)

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def main(url, event_loop):
    face_detective = await init_face_detective(APP_ID, API_KEY, SECRET_KEY)
    while url is not None:
        print("current url: " + url)
        datums = await fetch_activities(url)
        url = await process_activities(datums, face_detective, event_loop)
        # 注意节操，爬虫休息间隔不要调小
        await asyncio.sleep(5.0)


init_env()

url = BASE_URL % SOURCE + URL_QUERY
event_loop = asyncio.new_event_loop()
t = Thread(target=start_loop, args=(event_loop,))
t.start()
loop = asyncio.get_event_loop()
loop.run_until_complete(main(url, event_loop))
#tasks = [main(url)]
#loop = asyncio.get_event_loop()
#loop.run_until_complete(asyncio.wait(tasks))
#loop.close()

# vim: set ts=4 sw=4 sts=4 tw=100 et: