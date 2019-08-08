#!/usr/bin/python3
# coding:utf-8

from snkrsMonitor import *
from wechatAccount import wechatAccount

class snkrsHelper(object):
    def __init__(self):
        self.wechatAccount = wechatAccount()
        self.monitor = snkrsMonitor(wechat=self.wechatAccount)

if __name__ == "__main__" :
    snkrsHelper()