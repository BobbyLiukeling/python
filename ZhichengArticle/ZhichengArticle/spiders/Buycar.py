

# -*- coding: utf-8 -*-
import scrapy
from ..items import ZhichengarticleItem,QuestionItem,AnswerItem,CommentItem,comment_replayItem
import pdb
from scrapy.spiders import CrawlSpider

from selenium import webdriver
import time
import pymysql
import re
from . import label
from urllib import parse

# s = (['医疗', '版权专利', '教育', '房屋租售', '商务', '车辆买卖', '农业', '交通安全', '机关', '入职工作', '餐饮', '社会保障'])
class BuycarSpider(scrapy.Spider):

    name = 'Buycar'
    path = ['https://www.zhihu.com/question/339855206']
    start_urls = path


    def __init__(self):
        self.db = pymysql.connect(host="localhost", port=3306, user="root", passwd='867425', db="zhichengariticle",
                             charset="utf8")

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            print('* ' * 50)
            return closed(reason)


    def parse(self, response):
        try:
            item = QuestionItem()
            pdb.set_trace()
            Q_content = response.xpath(".//div[@class = 'QuestionHeader-detail']/div/div/span").extract()[0]
            answer_nums = response.xpath(".//h4[@class = 'List-headerText']/span/text()").extract()[0]
            tmp = re.findall(r'[1-9]+\.?[0-9]*', str(answer_nums))
            s = ''
            for i in tmp:
                if i.isdigit():
                    s = s + i
            answer_nums = int(s)  # 提取数字
            labels = response.xpath(".//div[@class = 'Tag QuestionTopic']/span/a/div/div/text()").extract()
            label = ''
            for i in labels:
                label = label + ' ' + i
            nums = response.xpath(".//strong[@class = 'NumberBoard-itemValue']/text()").extract()  # 关注人数，和 被浏览者人数
            try:
                focus_nums = int(nums[0])
            except:
                focus_nums = int(''.join([str for str in nums[0].split(',')]))
            try:
                view_nums = int(nums[1])
            except:  # ['1,833,117']将此拼接为数字
                view_nums = int(''.join([str for str in nums[1].split(',')]))
            Q_title = response.xpath(".//div[@class = 'QuestionHeader-main']/h1/text()").extract()[0]
            item['user'] = 'None'
            item['Q_title'] = Q_title.encode('utf-8').decode()
            item['Q_content'] = Q_title.encode('utf-8').decode()
            item['label'] = label
            item['url'] = response.url
            item['focus_nums'] = focus_nums
            item['answer_nums'] = answer_nums
            item['view_nums'] = view_nums
            item['tag'] = '上海堡垒'
            yield item

        except Exception as e:
            pdb.set_trace()
            print(e)
            pass








