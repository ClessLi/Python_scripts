#!/usr/bin/python2.7

import sys
import re

class e_mail():
    def check(self,version,address):
        if version=="1":
            self.rule=re.compile(r'^([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\@([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\.(com|cn|org|net|us)$')
            print '%s %s an e-mail address.' % (address,self.match(self.rule,address))
        elif version=="2":
            self.rule=re.compile(r'^(\<[a-zA-Z]+\s?[a-zA-Z]+\>)\s*([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\@([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\.(com|cn|org|net|us)$')
            if self.match(self.rule,address)=="is":
                print "%s %s an e-mail address and name is %s" (address,self.match(self.rule,address),self.rule.match(address).group(1))
        else:
            return "Usage %s <version>(1|2) <e-mail address>" % sys.argv[0]

    def match(self,rule,address):
        if rule.match(address):
            return "is"
        else:
            return "is not"

r=e_mail()
r.check(sys.argv[1],sys.argv[2])

