#!C:\\Python3.6\\python.exe
# encoding:utf-8
# Authored by Cless Li, at 2019/09/06

from Payrolls import Payrolls
from mail import E_mail
import xlrd
import sys
import os
import json


class Send_Payroll(object):
    def read_payrolls(self, payrolls):
        with xlrd.open_workbook(self.filepath) as payroll_fp:
            self.payrolls = payrolls(payroll_fp, 2).payrolls_list

    def send_mail(self):
        for payroll in self.payrolls:
            context = payroll.get('context')
            mail_address = payroll.get('mail_address')
            self.mail.send(mail_address, self.mail_title, context, 'html')

    def __init__(self, filepath, mail_title, payrolls_obj, mail_obj, smtp_server, port, mail_address, mail_passwd):
        self.filepath = filepath
        self.mail_title = mail_title
        self.mail = mail_obj(smtp_server, port, mail_address, mail_passwd)
        self.read_payrolls(payrolls_obj)


def help():
    print('Plz usage:\n%s <payrolls_file(xlsx)> <mail_title>' % sys.argv[0])


if __name__ == '__main__':
    if len(sys.argv) == 3:
        payrolls_file = sys.argv[1]
        mail_title = sys.argv[2]
        config_file = r'mail_config.json'
        if not os.path.exists(config_file):
            print('Plz check whether the "%s" exists.' % config_file)
            exit(1)
        else:
            with open(config_file, 'r') as cfg_fp:
                cfg_json = json.load(cfg_fp)
            smtp_server = cfg_json.get('smtp_server')
            smtp_port = cfg_json.get('smtp_port')
            email = cfg_json.get('from_addr')
            email_pwd = cfg_json.get('password')
        if os.path.exists(payrolls_file):
            auto_send_payroll = Send_Payroll(
                payrolls_file,
                mail_title,
                Payrolls,
                E_mail,
                smtp_server,
                smtp_port,
                email,
                email_pwd
            )
            auto_send_payroll.send_mail()
        else:
            help()
            exit(1)
    else:
        help()
        exit(1)
