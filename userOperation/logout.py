# -*- encoding: utf-8 -*-
from random import uniform
from time import sleep
from custom.xuexi_edge import XuexiEdge


def logout(browser: XuexiEdge):
    browser.xuexi_get('https://www.xuexi.cn/')
    sleep(round(uniform(1, 2), 2))
    logoutBtn = browser.find_element_by_class_name('logged-link')
    logoutBtn.click()
