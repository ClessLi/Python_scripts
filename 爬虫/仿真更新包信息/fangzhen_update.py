# encoding:utf-8

from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class GetUpdate(object):
    def open_browser(self, ):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (self.userAgent)
        self.browser = webdriver.PhantomJS(self.pjs_path, desired_capabilities=dcap)

    def login(self):
        self.browser.get(self.login_url)
        self.browser.find_element_by_class_name('login-info login-user').send_keys(self.user)
        self.browser.find_element_by_class_name('login-info login-pwd').send_keys(self.passwd)
        self.browser.find_element_by_class_name('loginbtn').click()

    def go_to_update_page(self):
        self.browser.switch_to.frame('leftFrame')
        self.browser.find_element_by_link_text('仿真版本管理').click()
        self.browser.find_element_by_link_text('仿真升级包').click()
        self.browser.switch_to.frame('rightFrame')

    def info_parse(self):
        page_doc = pq(self.browser.page_source)
        page_total = page_doc('').text()
        current_page = page_doc('').text()
        if current_page < page_total:
            data = page_doc('#listDT table.tablelist tbody')




if __name__ == "__main__":
    url = 'http://183.62.156.138:9065/gpaybank/login.jsp'
    user_name = u'富民银行'
    user_passwd = '123456'
    fangzhen_update = GetUpdate(url=url, user=user_name, passwd=user_passwd)
    print(fangzhen_update.info)
