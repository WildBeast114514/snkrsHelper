#!/usr/bin/python3
# coding:utf-8
import urllib3
import json
import time
from datetime import datetime
import traceback
from collections import deque
import os
import requests
import platform

from enum import Enum

urllib3.disable_warnings()


class publicMethod(object):
    def formatTimeStr(self, str1):
        return str1[0:10] + " " + str1[11:19]
    def getTime(self, str1):
        return time.mktime(time.strptime(self.formatTimeStr(str1), "%Y-%m-%d %H:%M:%S"))
    def getLocalTimeStr(self, str1):
        tm = self.getTime(str1)
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(tm + 28800)))
    def addsepline(self):
        print("-----------------------------------------------------------------------------------------------")
    def addseptag(self):
        print("##################################################################")

class RegionURL(Enum):
    cn = "&country=CN&language=zh-Hans"
    us = "&country=US&language=en"
    jp = "&country=JP&language=ja"
        
        
class OrderBy(Enum):
    published = "&orderBy=published"
    updated = "&orderBy=lastUpdated"


class snkrsMonitor(object):
    def __init__(self, wechat=None):
        self.wechat = wechat
        self.totalCount = 1000000
        self.apiurl = "https://api.nike.com/snkrs/content/v1/?"
        self.publicMethod = publicMethod()
        self.titlePrint()
        self.sneakers = []  # 球鞋缓存
        self.ludict = {}  #

        self.baseConfig()
        self.listPublishedShoes()
        self.userSetup()
        self.timer(3)

    def titlePrint(self):
        self.publicMethod.addsepline()
        print("田所浩二的Nike球鞋监控 V0.1")
        self.publicMethod.addsepline()
    def baseConfig(self):
        areaCode = input("请选择市场区域(1:美国,2:日本,3:中国):")
        if areaCode == "1":
            self.apiurl += RegionURL.us.value
        elif areaCode == "2":
            self.apiurl += RegionURL.jp.value
        else:
            self.apiurl += RegionURL.cn.value
    def printSneaker(self, data):
        str1 = data["name"] + " " + data["title"]
        try:
            if data["product"]["colorDescription"]:
                str1 += ("[" + data["product"]["colorDescription"] + "]")
            if data["product"]["merchStatus"]:
                str1 += ("[" + data["product"]["merchStatus"] + "]")
        except:
            pass
        if data["restricted"]:
            str1 += "[受限]"
        print(str1)
        return str1
    def printSneakerDetail(self, data):
        dict1 = {
            "LEO": "LEO(限量)",
            "DAN": "DAN(抽签)",
        }
        product = data["product"]
        try:
            try:
                name = product["title"] + "[" + product["colorDescription"] + "]"
            except:
                name = data["title"] + "[" + product["colorDescription"] + "]"
            if data["restricted"]:
                name += "[受限]"
            price = "价格:" + str(product["price"]["msrp"])
            publicType = "发售方式:正常"
            if product["publishType"] == "LAUNCH":
                engine = product["selectionEngine"]
                publicType = "发售方式:" + dict1[engine]
            launchInfo = "不可购买"
            if product["merchStatus"] == "ACTIVE" and product["available"] and "stopSellDate" not in product.keys():
                launchInfo = "发售时间:" + self.publicMethod.getLocalTimeStr(product["startSellDate"])
            print(name)
            print(price)
            print(publicType)
            print(launchInfo)
            return name + "\n" + price + "\n" + publicType + "\n" + launchInfo
        except Exception as ex:
            return "接口修改警告"
    def requestSneakers(self, order, offset):
        requrl = self.apiurl + "&offset=" + str(offset) + order
        http = urllib3.PoolManager()
        r = http.request("GET", requrl)
        shoes = []
        try:
            json_data = json.loads(str(r.data, encoding="utf-8"))
            if "error_id" in json_data:
                print("请求offset超出范围，返回shoes")
                return shoes
            else:
                if len(self.sneakers) >= self.totalCount:
                    return []
                self.totalCount = json_data["totalRecords"]
                for data in json_data["threads"]:
                    shoes.append(data["id"])
                    self.ludict[data["id"]] = self.publicMethod.getTime(data["lastUpdatedDate"])
                    if offset == 0:
                        self.printSneaker(data)
                return shoes
        except Exception as ex:
            print("\r访问服务器失败，3秒后重试,原因为:"+str(ex))
            time.sleep(3)
            return self.requestSneakers(order, offset)
    def listPublishedShoes(self):
        for num in range(0, 50):
            k = num * 50
            snkrs = self.requestSneakers(OrderBy.published.value, k)
            if len(snkrs) == 0:
                print("数据请求完毕,一共获取到", str(len(self.sneakers)), "条数据(只显示前50条)...")
                break
            self.sneakers.extend(snkrs)
            time.sleep(2)
    def userSetup(self):
        self.publicMethod.addsepline()
        self.keyword = "off white"
        self.frequency = 3
        self.warningTime = 5
        inputfreq = input("请设定接口访问频率(秒)，访问频率过快可能会导致服务器异常，默认是3，最小是1:")
        try:
            self.frequency = int(inputfreq)
        except:
            print("输入出错，按照默认频率请求")
        if self.frequency <= 0:
            self.frequency = 3
        warning = input("请设定发现新款过后报警次数，默认是5，最小是1:")
        try:
            self.warningTime = int(warning)
        except:
            print("输入出错，按照默认次数报警")
        if self.warningTime <= 0:
            self.warningTime = 5
        self.keyword = input("设定库存监控关键词,多个关键词用&区分(eg:off white):")
        print("服务器实时请求接口中(" + str(self.frequency) + "秒每次)...")
        self.publicMethod.addseptag()
    def warning_hints(self, tip_text):
        sys_str = platform.system()
        if sys_str == "Windows":
            winsound.Beep(2600, 1000)
            print(tip_text)
        elif sys_str == "Linux":
            os.system('say ' + tip_text)
            print(tip_text)
        else:
            os.system('say ' + tip_text)
            print(tip_text)
    def timer(self,n):
        while True:
            try:
                http = urllib3.PoolManager()
                requesturl = self.apiurl + OrderBy.updated.value + "&offset=0"
                r = http.request("GET", requesturl)
                json_data = json.loads(str(r.data, encoding="utf-8"))
                datas = json_data["threads"]
            except Exception as ex:
                print("\r请求失败" + str(ex), flush=True)
                continue
            findstrs = self.keyword.split("&")
            for data in datas:
                sneakerid = data["id"]
                t_last_update_date = data["lastUpdatedDate"]
                if sneakerid not in self.sneakers:
                    self.sneakers.append(sneakerid)
                    self.ludict[data["id"]] = self.publicMethod.getTime(t_last_update_date)
                    i = self.warningTime
                    while i > 0:
                        self.warning_hints("\r《发现新款更新》")
                        print("\r", "发现新款  更新时间:", self.publicMethod.getLocalTimeStr(t_last_update_date))
                        productIntro = self.printSneakerDetail(data)
                        self.publicMethod.addseptag()
                        for key in findstrs:
                            if key in productIntro:
                                self.wechat.sendNotice("发现新款  更新时间:" + self.publicMethod.getLocalTimeStr(t_last_update_date) + productIntro)
                        i -= 1
                else:
                    if self.publicMethod.getTime(t_last_update_date) > self.ludict[sneakerid]:
                        self.ludict[sneakerid] = self.publicMethod.getTime(t_last_update_date)
                        product = data["product"]
                        print("\r", self.publicMethod.getLocalTimeStr(t_last_update_date), end=" ")
                        t_str = "售罄"
                        try:     
                            if product["merchStatus"] == "ACTIVE":
                                if product["available"]:
                                    t_str = "库存更新("
                                    for sku in product["skus"]:
                                        if sku["available"]:
                                            t_str += (sku["localizedSize"] + ",")
                                            t_str = t_str[:-1]
                                            t_str += ")"
                            print(t_str, end=" ")
                            productIntro = self.printSneaker(data)
                        except:
                            continue
                        for key in findstrs:
                            if key in productIntro:
                                self.wechat.sendNotice(t_str + productIntro)
                        seostr = data["seoSlug"]
                        for key in findstrs:
                            if seostr.find(key) != -1:
                                productIntro = self.printSneakerDetail(data)
                                self.publicMethod.addseptag()
                                i = self.warningTime
                                while i > 0:
                                    self.warning_hints("\r《关注鞋款库存更新》")
                                    print("关注鞋款库存更新")
                                    self.wechat.sendNotice("关注鞋款库存更新" + productIntro)
                                    i -= 1
                                break
                print("\r" + time.strftime("time :%Y-%m-%d %H:%M:%S", time.localtime(time.time())), end=" ")
            time.sleep(self.frequency)

if __name__ == "__main__":
    snkrsMonitor()