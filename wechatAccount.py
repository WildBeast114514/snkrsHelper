#!/usr/bin/python3
# coding:utf-8

import itchat
import threading
from common.logger import *

class wechatAccount(object):

    def __init__(self, noticeGroup="李田所粉丝群"):
        self.noticeGroup = noticeGroup
        self.instance = itchat.new_instance()
        self.status = 0 # 0==available;1==login;2==running;
        self.login()
        self.start()

    def login(self):
        if self.status != 0:
            return
        else:
            '''
            自动登录，使用缓存
            '''
            try:
                self.instance.auto_login(hotReload=True, enableCmdQR=2)
                self.status = 1
            except:
                pass

    def start(self):
        if self.status != 1:
            return
        else:
            '''
            启动机器人
            '''
            try:
                self.thread = threading.Thread(target=self.wechatRun)
                self.thread.setDaemon(True)
                self.thread.start()
                self.status = 2
            except:
                pass

    def wechatRun(self):
        self.instance.run(debug=False)
        
    def sendNotice(self,notice):
        if not self.status:
            LOG_ERROR("微信模组没有运行，请检查账号是否被封")
            print("微信模组没有运行，请检查账号是否被封")
        else:
            try:
                user_name = self.instance.search_chatrooms(name=self.noticeGroup)[0].UserName
            except:
                LOG_WARN('查询不到"'+self.noticeGroup+'"的群，发送提醒失败！')
                print('查询不到"'+self.noticeGroup+'"的群，发送提醒失败！')
            self.instance.send_msg(notice,toUserName=user_name)