# -*- coding: utf-8 -*-
import scrapy


class MotoXuankeSpider(scrapy.Spider):
    name = 'moto_xuanke'
    # allowed_domains = ['http://ehall.scu.edu.cn/']
    # path = 'http://ehall.scu.edu.cn/new/index.html'
    path = 'https:www.baidu.com'
    start_urls = path

    def parse(self, response):
        pass
