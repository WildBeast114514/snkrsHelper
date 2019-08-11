#!/usr/bin/python3
# coding:utf-8

import time
from common.logger import *
import threading

class reporter(object):

    def __init__(self,snkrsHelper=None,intervalTime=600):
        self.snkrsHelper = snkrsHelper
        self.programStatus = 1
        self.intervalTime = intervalTime
        self.start()
    
    def report(self):
        self.programStatus = 1

    def checkoutHealth(self):
        while True:
            if self.programStatus != 1:
                LOG_ERROR("monitor异常")
                if self.snkrsHelper.snkrsMonitor.status == 0:
                    self.snkrsHelper.wechat.sendNotice("警告，monitor异常,timer已经退出")
                else:
                    self.snkrsHelper.wechat.sendNotice("警告，monitor异常,timer异常")
            else:
                LOG_INFO("monitor正常")
                self.programStatus = 0
                time.sleep(self.intervalTime)
                
    def start(self):
        try:
            self.thread = threading.Thread(target=self.checkoutHealth)
            self.thread.setDaemon(True)
            self.thread.start()
        except:
            pass

if __name__ == "__main__":
    Logger.Init(level=logging.DEBUG, logfile = './testLog')
    test = reporter(None,3)
    while True:
        test.report()
        time.sleep(1)