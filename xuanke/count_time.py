# -*- coding: utf-8 -*-
# @Time : 2021/4/19 0019 10:36
# @Author : Bobby_Liukeling
# @File : count_time.py


import time
from selenium import webdriver
import requests
import json
import pdb
from lxml import etree
from scrapy.selector import Selector
import datetime
import numpy as np

class YunPian(object): #只能是30s一次
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        """
        发送验证码
        :param code: 验证码
        :param mobile: 手机号码
        :return:
        """
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            # 这个text的值要跟你模板内容一模一样
            "text": "【刘珂伶】您的验证码是{}".format(code)
        }

        # 发送post请求  请求的地址self.single_send_url  发送的数据data=params
        response = requests.post(self.single_send_url, data=params)

        # response.text是json数据
        # 把json数据转换成字典
        re_dict = json.loads(response.text)
        print(re_dict)

class web_get():
    web = webdriver.Chrome('E:/software/python3.6/chromedriver.exe')
    path1 = 'https://www.bilibili.com/video/BV15741177Eh?from=search&seid=4962427678077481753'
    web.get(path1)
    time.sleep(10)

    content = web.find_elements_by_xpath(".//div[@class = 'cur-list']/ul/li")

    # pdb.set_trace()
    totel = '0:0'
    for list_time,index in zip(content,range(len(content))):

        name = list_time.find_element_by_xpath(".//span[@class='part']").text
        length_time = list_time.find_element_by_xpath(".//div[@class='duration']").text#不要秒

        M = int(totel.split(':')[0])+int(length_time.split(':')[0])
        S = int(totel.split(':')[1])+int(length_time.split(':')[1])
        totel = str(M+int(S/60))+':'+str(S%60)
        # pdb.set_trace()
        hour = np.around(int(totel.split(':')[0])/60,1)
        print(index," : ",name," ", length_time," ",hour)


        # pdb.set_trace()

if __name__ == "__main__":


    web = web_get()


