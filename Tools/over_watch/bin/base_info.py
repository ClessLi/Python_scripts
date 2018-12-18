# encoding:utf-8



#from collections import OrderedDict

#import aiofiles
import asyncio
import asyncssh
#import sys


async def ssh_by_keys(hostname, username, cmd):
    async with asyncssh.connect(hostname, username=username) as conn:
        result = await conn.run(cmd, check=True)
        #print(result.stdout, end='')
        return result.stdout


class CPUinfo():
    def __init__(self, hostname, username, cmd='sar 5 6'):
        self.hostname = hostname
        self.username = username
        self._cmd = cmd
        self.cpu_iowait = None
        self.cpu_idle = None

    async def get_info(self):
        result = await ssh_by_keys(self.hostname, self.username, self._cmd)
        cpuinfo_list = result.strip().split('\n')
        if cpuinfo_list[-1].strip():
            self.cpu_iowait = cpuinfo_list[-1].split()[-3]
            self.cpu_idle = cpuinfo_list[-1].split()[-1]


class OVER_WATCH():
    def __init__(self, filename, username='root'):
        self._tasks = []
        self._host_cpuinfo = {}
        self.username = username
        self._hostlist = self._read_filelist(filename)

    def _read_filelist(self, filename):
        try:
            with open(filename, 'r') as fp:
                return fp.readlines()
        except FileNotFoundError as err:
            print(err)
            exit()

    def _add_corountines_tasks(self, c_obj):
        self._tasks.append(c_obj)

    def _get_cpuinfo_tasks(self, cmd='sar 5 6'):
        for host in self._hostlist:
            self._host_cpuinfo[host] = CPUinfo(host, self.username, cmd)
            self._add_corountines_tasks(self._host_cpuinfo[host].get_info())

    def main(self, cmd):
        self._get_cpuinfo_tasks(cmd)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(self._tasks))
        loop.close()
        cpuinfo_dict = {}
        for host in self._hostlist:
            if self._host_cpuinfo[host].cpu_iowait or self._host_cpuinfo[host].cpu_idle:
                print('host:%s iowait:%s idle:%s' % (host,
                                                     self._host_cpuinfo[host].cpu_iowait,
                                                     self._host_cpuinfo[host].cpu_idle))
                cpuinfo_dict[host.strip('\n')] = dict(iowait=self._host_cpuinfo[host].cpu_iowait,
                                                      idle=self._host_cpuinfo[host].cpu_idle)
        return cpuinfo_dict


if __name__ == '__main__':
    hostlist_path = '/home/cless/hosts.list'
    overwatch = OVER_WATCH(hostlist_path)
    print(overwatch.main('sar 1 1'))
