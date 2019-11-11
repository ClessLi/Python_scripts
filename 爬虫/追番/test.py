#!/home/cless/python2.7/bin/python2.7
# encoding:utf-8

from pyquery import PyQuery as pq
from bs4 import BeautifulSoup as bs
import lxml

html = 'http://www.msj1.com/archives/6042.html'
doc = pq(html)
soup = bs(str(doc('table.table tbody tr td a')), 'lxml')
print soup.prettify()
