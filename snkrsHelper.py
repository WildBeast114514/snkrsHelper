#!/usr/bin/python3
# coding:utf-8

from snkrsMonitor import *
from wechatAccount import wechatAccount
from common.logger import *

class snkrsHelper(object):
    def __init__(self):
        self.wechatAccount = wechatAccount()
        self.monitor = snkrsMonitor(wechat=self.wechatAccount)

if __name__ == "__main__" :
    Logger.Init(level=logging.DEBUG, logfile = './log/snkrs')
    snkrsHelper()