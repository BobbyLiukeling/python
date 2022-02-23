# -*- coding: utf-8 -*-
# @Time : 2020/10/12 0012 12:42
# @Author : Bobby_Liukeling
# @File : mengti.py

# -*- coding: utf-8 -*-
# @Time : 2020/9/29 0029 21:25
# @Author : Bobby_Liukeling
# @File : moto.py


import time
from selenium import webdriver
import requests
import json
import pdb
from lxml import etree
from scrapy.selector import Selector

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
    path1 = 'http://ehall.scu.edu.cn/yjsxkapp/sys/xsxkapp/index.html'
    path2 = 'http://ehall.scu.edu.cn/yjsxkapp/sys/xsxkapp/course.html'
    web.get(path1)
    time.sleep(25)

    # path2 = '' #课程选取链接,在登陆状态下，重新登录选课链接
    web.get(path2)

    while(1):
        web.refresh() # 刷新
        time.sleep(1) #缓存
        content = []
        #暂时只有两门课

        content1 = web.find_element_by_xpath('//table[contains(@class,"zero-grid") and contains(@class,"zero-grid-hover")]/tbody/tr[1]/td/span').text

        content.append(content1)
        for i in content:
            a = i.split('/')
            if int(a[0])<int(a[1]): #有课
                #参数是你的apikey
                apikey = '7d850770e04e8ba10d9a93f4b8f77528'
                yunpian = YunPian(apikey)
                # 填写你要发送的验证码  和  手机号码
                yunpian.send_sms('123456', '19180968154')
        time.sleep(30) #30s刷新一次

if __name__ == "__main__":
    web = web_get()


