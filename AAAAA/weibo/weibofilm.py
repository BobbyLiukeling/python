# -*- coding: utf-8 -*-
import scrapy

from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import pymysql
import re
from urllib import parse
import pdb
import traceback, sys
from scrapy.selector import Selector






class WeibofilmSpider(scrapy.Spider):
    name = 'weibofilm'
    # allowed_domains = ['www.weibo.com']
    start_urls = labels.y #有评论
    # start_urls = labels.n #没评论


    def __init__(self):
        self.db = pymysql.connect(host="localhost", port=3306, user="root", passwd='867425', db="weibofilm",charset="utf8")

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()
        self.web = webdriver.Chrome("E:/software/python3.6/chromedriver.exe")

    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            print('* ' * 50)
            return closed(reason)

    def parse(self, response):

        pass
