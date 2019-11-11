#!/home/cless/python2.7/bin/python3.6
# encoding:utf-8
from pyquery import PyQuery as pq
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import time, aiohttp, asyncio, socket
selector = DefaultSelector()
stopped = False
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}

class Crawler:
    def __init__(self, host, url ,selector, urls_todo):
        self.host = host
        self.url = url
        self.selector = selector
        self.urls_todo = urls_todo
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('www.baidu.com', 80))
        except BlockingIOError:
            print('error')
            pass
        type(self.sock.fileno())
        print(self.sock.fileno())
        self.selector.register(self.sock.fileno(), EVENT_WRITE, self.connected)

    def connected(self, key, mask):
        print('connected')
        self.selector.unregister(key.fd)
        get = 'GET {0} HTTP/1.0\r\nHost: {0}\r\n\r\n'.format(self.url, self.host)
        self.sock.send(get.encode('ascii'))
        selector.register(key.fd, EVENT_READ, self.read_response)

    def read_response(self, key, mask):
        global stopped
        chunk = self.sock.recv(4096)
        if chunk:
            self.response += chunk
        else:
            print(pq(self.response))
            self.selector.unregister(key.fd)
            self.urls_todo.remove(self.url)
            if not self.urls_todo:
                stopped = True

def event_loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)

if __name__ == '__main__':
    import time
    start = time.time()
    for url in urls_todo:
        crawler = Crawler('www.baidu.com', url, selector, urls_todo)
        crawler.fetch()
    event_loop()
    print(time.time() - start)

