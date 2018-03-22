#!/usr/bin/python2.7

import sys
import re

class e_mail():
    def __init__(self,address):
        self.address = address
        self.rule1=re.compile(r'^([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\@([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\.(com|cn|org|net|us)$')
        self.rule2=re.compile(r'^<([a-zA-Z]+\s?[a-zA-Z]+)>\s*([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\@([a-zA-Z0-9][a-zA-Z0-9\-\_\.]*?[a-zA-Z0-9])\.(com|cn|org|net|us)$')
        self.name=self.check()
    def check(self):
        if self.match(self.rule1,self.address):
            return self.rule1.match(self.address).group(1)
            #print '%s is an e-mail address.' % address
        elif self.match(self.rule2,self.address):
            return self.rule2.match(self.address).group(1)
            #print "%s is an e-mail address and name is %s" % (address,self.rule2.match(address).group(1))
        else:
            return False
            #print "%s is not an e-mail address" % address

    def match(self,rule,address):
        if rule.match(address):
            return True
        else:
            return False
if __name__ == '__main__':
    r=e_mail(sys.argv[1])
    #print r.match(r.rule1,sys.argv[1])
    #print r.match(r.rule2,sys.argv[1])
    #print r.rule2.match(sys.argv[1]).group(1)
    print ('%s is an e-mail address and name is %s.' % (r.address, r.name) if r.name else '%s is not an e-mail address.' % r.address)

