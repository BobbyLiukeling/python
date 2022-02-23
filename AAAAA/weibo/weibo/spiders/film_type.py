# -*- coding: utf-8 -*-
# @author : bobby
# @time : 2020/3/3 18:35

'''
爬取近十年的上线电影名称，以及电影类型，并存入数据库
'''
import scrapy
import pymysql
from selenium import webdriver
import pdb
from scrapy.selector import Selector
import time

# from ..items import Types
from type_url import urls
# import  .type_url.urls as url


class FilmTypeSpider(scrapy.Spider):
    name = 'film_type'
    pdb.set_trace()

    # url = []
    # s = 'https://www.1905.com/mdb/film/calendaryear/'
    # for i in range(2010,2020):
    #     url.append(s+str(i))
    start_urls = urls
    # start_urls = ['https://www.1905.com/mdb/film/calendaryear/2010',]

    def __init__(self,**kwargs):
        self.db = pymysql.connect(host="localhost", port=3306, user="root", passwd='867425', db="weibofilm",charset="utf8")
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()
        # self.film = open('type_url.py','w')
        # self.film.write("urls = [")
        # self.web = webdriver.Chrome("E:/software/python3.6/chromedriver.exe")

    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            print('* ' * 50)
            return closed(reason)

    # def parse(self, response):
    #     count = 0
    #     month = response.xpath("..//div[contains(@class,'film-col') and contains(@class,'layout')]")
    #     for i in month:
    #         s = i.xpath("..//dd")
    #         for j in s:
    #             count = count+1
    #             temp_url = j.xpath("./a/@href").extract()[0] #爬取链接
    #             self.film.write("'https://www.1905.com{} ',".format(temp_url))
    #     print('233'*10)
    #     print(count)



    def parse(self,response):

        item = Types()
        filmname = response.xpath("..//div[@class = 'container-right']/h1/text()").extract()[0].strip() #电影名
        up_time = response.xpath("..//div[@class = 'information-list']/span/text()").extract()[0] #上映时间
        temp = response.xpath("..//div[@class = 'information-list']/span[@class = 'information-item'][2]/a") #类型
        # response.xpath("..//div[@class = 'information-list']/span[@class = 'information-item'][2]").extract()[0]
        types = '' #类型
        for i in temp:
            s = i.xpath("./text()").extract()[0] #从当前根目录向下搜索
            types = types + s +' '
        item['filmname'] = filmname
        item['types'] = types
        item['time'] = up_time
        yield item







