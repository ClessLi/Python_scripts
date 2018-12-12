# -*- coding : utf-8 -*-


from collections import OrderedDict

import aiofiles
import asyncio
import asyncssh

async def ssh_by_keys(hostname, username, keys_filename, cmd):
    async with asyncssh.auth_keys.read_authorized_keys(keys_filename) as auth_keys:
        async with asyncssh.connect(hostname, username=username, client_keys=[auth_keys]) as conn:
            result = await conn.run(cmd, check=True)
            return result.stdout

class CPUinfo():
    def __init__(self, hostname, username, keys_filename, cmd='cat /proc/CPUinfo'):
        self.CPUinfo = OrderedDict()
        self.procinfo = OrderedDict()
        self.hostname = hostname
        self.username = username
        self.keys_filename = keys_filename
        self.cmd = cmd
        self.nprocs = 0

    async def get_info(self):
        result = await ssh_by_keys(self.hostname,self.username,self.keys_filename,self.cmd)
        for line in result:
            if not line.strip():
                # end of one processor
                self.CPUinfo['proc%s' % self.nprocs] = self.procinfo
                self.nprocs = self.nprocs + 1
                # Reset
                self.procinfo = OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    self.procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    self.procinfo[line.split(':')[0].strip()] = ''


class OVER_WATCH():
    def __init__(self, filename, ssh_filename):
        self.filename = filename
        self.ssh_filename = ssh_filename

    async def read_hostlist(self, filename):
        try:
            async with aiofiles.open(filename) as hostlist:
                return await hostlist
        except FileNotFoundError as err:
            print(err)
            exit()

    async def get_cpuinfo_tasks(self, filename, ssh_filename, cmd='cat /proc/CPUinfo'):
        hostlist = await self.read_hostlist(filename)
        tasks = [hostlist]
        for host in hostlist:
            host_cpuinfo = CPUinfo(host, 'root', ssh_filename, cmd)
            task = await host_cpuinfo.get_info()
            tasks.append(task)
        return tasks

    def main(self):
        cpuinfo_tasks = self.get_cpuinfo_tasks(self.filename, self.ssh_filename)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(cpuinfo_tasks))
        loop.close()


if __name__ == '__main__':


