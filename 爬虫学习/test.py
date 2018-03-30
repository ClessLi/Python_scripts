rom pyquery import PyQuery as pq
doc = pq(url='http://www.baidu.com')
#print doc
#print doc('div').children('[class]')
print doc('div form span')