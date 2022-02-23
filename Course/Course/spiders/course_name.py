# -*- coding: utf-8 -*-
import scrapy
from ..items import CourseItem
import time
import re


class CourseNameSpider(scrapy.Spider):
    name = 'course_name'
    #allowed_domains = ['ios.com']
    start_urls = ['http://www.newbiefly.com/?post_type=gift']

    def __init__(self):
        self.count = 0

    def parse(self, response):
        lists = response.xpath("//div[@class='row clearfix']/article")
        for list in lists:
            #type = response.meta.get("type","") #类型
            try:
                title = list.xpath(".//div[@class='entry-meta']/a/text()").extract()[0].strip()
            except:
                title = "没有标题"
            content_href =list.xpath(".//div[@class='entry-meta']/a/@href").extract()[0]#课程链接
            try:
                score = list.xpath(".//div[@class='entry-meta']/span/text()").extract()[0]
            except:
                score = list.xpath(".//div[@class='entry-meta']/span/em/text()").extract()[0]
            #img_href = list.xpath(".//img/@src").extract()[0]
            item = CourseItem()
            #item["type"] = type
            item["title"] = title
            item["href"] = content_href
            item["score"] = score
            #item["img_href"] = img_href
            yield item
        time.sleep(0.2)#爬取速度太快会返回429

        try:#拿到下一页
            #count = response.meta.get("count", "")#链接后缀
            self.count+=1
            #next_page_href = response.xpath("//a[@class='next page-numbers']/@href").extract()[0]
            next_page_href = "http://www.newbiefly.com/?paged="+str(self.count)+"&post_type=gift"
            yield scrapy.Request(url=next_page_href, callback=self.parse)
        except:
            pass
