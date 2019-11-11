import os
import multiprocessing
from multiprocessing import Pool

def func(i):
    global a
    p = multiprocessing.current_process()
    print i, p.name, p._identity, p.pid, os.getpid(), os.getppid(),  b,  a
    a += 10

a, b = 1, 1
pool = Pool(2)

a, b = 2, 2
print '--------'
pool.map(func, range(4))

pool = Pool(2)
print '--------'
pool.map(func, range(4))

def func(i, c=[]):
    p = multiprocessing.current_process()
    print i, p.name, p._identity, p.pid, os.getpid(), c
    c.append(i)

print '--------'
pool.map(func,  range(4))

pool = Pool(2)
print '--------'
pool.map(func,   range(4))