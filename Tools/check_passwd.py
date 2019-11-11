#!/usr/bin/python3.6
# encoding:utf-8
#Authored by Cless Li at 2018-12-19 13:58:40



#from collections import OrderedDict

#import aiofiles
import asyncio
import asyncssh
import sys
import os


async def ssh_by_passwd(hostname, username, passwd, cmd):
    async with asyncssh.connect(hostname, username=username, password=passwd) as conn:
        try:
            result = await conn.run(cmd, check=True)
            return result.stdout.strip('\n')
        #print(result.stdout, end='')
        except asyncssh. as err:
            print('访问服务器[%s]失败：\n%s' % (hostname, err))
            return 'Fail'


class OVER_WATCH():
    def __init__(self, filename, cmd='echo "OK"'):
        self._cmd = cmd
        self._tasks = []
        self._host_passwdinfo = {}
        self._passwdlist = self._read_filelist(filename)

    def _read_filelist(self, filename):
        try:
            with open(filename, 'r') as fp:
                return fp.readlines()
        except Exception as err:
            print(err)
            exit()

    def _add_corountines_tasks(self, c_obj):
        self._tasks.append(c_obj)

    def _check_passwd_tasks(self):
        for line in self._passwdlist:
            passwdinfo = line.split(',')
            host = passwdinfo[0]
            username = passwdinfo[1]
            passwd = eval(passwdinfo[2])
            self._add_corountines_tasks(self.check_passwd(host, username, passwd, self._cmd))

    async def check_passwd(self, host, username, passwd, cmd):
            result = await ssh_by_passwd(host, username, passwd, cmd)
            self._host_passwdinfo[host] = str(result)

    def main(self):
        self._check_passwd_tasks()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(self._tasks))
        loop.close()
        print(self._host_passwdinfo)
        for host in self._host_passwdinfo:
            print('%s:%s' % (host, self._host_passwdinfo[host]))


if __name__ == '__main__':
    #hostlist_path = sys.argv[1]
    hostlist_path = 'lt_oper'
    if os.path.exists(hostlist_path):
        overwatch = OVER_WATCH(hostlist_path)
        overwatch.main()
    else:
        print('Plz usage: %s <config_file_path>' % sys.argv[0])
        exit(code=1)
    #print(overwatch.main('sar 1 1'))
