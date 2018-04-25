from pyquery import PyQuery as pq
import requests
from bs4 import BeautifulSoup
import time
import image
import json
import urllib2

#url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
url = 'https://www.zhihu.com/signup?next=%2F#signin'
session = requests.session()
_xsrf = BeautifulSoup(session.get('https://www.zhihu.com/#signin').content).find('input', attrs={'name': '_xsrf'})['value']
captcha_content = session.get('http://www.zhihu.com/captcha.gif?r=%d' % (time.time() * 1000)).content
data = {
    '_xsrf': _xsrf,
    'email': username,
    'password': password,
    'remember_me': 'true',
    'captcha': oncaptcha(captcha_content)
}
resp = session.post('http://www.zhihu.com/login/email', data).content
assert '\u767b\u9646\u6210\u529f' in resp
print session
#doc = pq(session.get(url).content)
#doc = pq(url)
#print doc
#header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'}

#doc = pq(url=url)
#print doc
