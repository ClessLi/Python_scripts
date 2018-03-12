#!/usr/bin/python2.7

import sys
import re

class e-mail():
    __init__(self):
        self.version=sys.argv(1)
        self.address=sys.argv(2)
        self.check(self.version,self.address)

    check(self,version,address):
        if version=1:
            self.rule=re.compile(r'^([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\@([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\.(com|cn|org|net|us)$')
            print '%s %s an e-mail address.' % address,self.match(self.rule,address)
        elif version=2:
            self.rule=re.compile(r'^(\<[a-zA-Z]+\s?[a-zA-Z]+\>)\s*([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\@([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\.(com|cn|org|net|us)$')
            if self.match(self.rule,address)=="is":
                print "%s %s an e-mail address and name is %s" address,self.match(self.rule,address),self.rule.match(address).group(1)
        else:
            return "Usage check_e-mail <version>(1|2) <e-mail address>"

    match(self,rule,address):
        if rule.match(address):
            return "is"
        else:
            return "is not"
