#!/usr/bin/python2.7

import sys
import re

class e_mail():
    def __init__(self):
        self.rule1=re.compile(r'^([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\@([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\.(com|cn|org|net|us)$')
        self.rule2=re.compile(r'^<([a-zA-Z]+\s?[a-zA-Z]+)>\s*([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\@([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\.(com|cn|org|net|us)$')
    def check(self,address):
        if self.match(self.rule1,address):
            print '%s is an e-mail address.' % address
        elif self.match(self.rule2,address):
            print "%s is an e-mail address and name is %s" % (address,self.rule2.match(address).group(1))
        else:
            print "%s is not an e-mail address" % address

    def match(self,rule,address):
        if rule.match(address):
            return True
        else:
            return False
r=e_mail()
#print r.match(r.rule1,sys.argv[1])
#print r.match(r.rule2,sys.argv[1])
#print r.rule2.match(sys.argv[1]).group(1)
r.check(sys.argv[1])

