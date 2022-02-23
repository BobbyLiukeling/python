# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver

import time
from scrapy.http.response.html import HtmlResponse
import pdb
from scrapy.selector import Selector

class ZhihuSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# HtmlResponse(url, body, encoding, request)
# url 重定向后的地址
# body 网页内容
# request 重定向前的网址
class ZhihuDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        self.web = webdriver.Chrome("E:/software/python3.6/chromedriver.exe")

    def process_response(self, request, response, spider):
        try:
            # pdb.set_trace()
            #非搜索主页面
            if (spider.name == "film") and str(request.url).startswith('https://www.zhihu.com/search?type=content&q=') == False:
                self.web.get(request.url)
                time.sleep(2)
                # pdb.set_trace()
                str_url = str(response.url).split('/')
                if str_url[-2] == 'p': #专栏  链接样式 https://zhuanlan.zhihu.com/p/77565739
                    body = self.web.page_source
                    return HtmlResponse(url=self.web.current_url, body=body, encoding="utf-8", request=request)
                else:  #问题  链接样式 https://www.zhihu.com/question/312793089
                    try:
                        # self.web.find_element_by_xpath(".//*[@class='AppHeader-profile']/div/button").click()
                        # # 点击社交网络账号登陆
                        # try:
                        #     # pdb.set_trace()
                        #     time.sleep(2)
                        #     self.web.find_element_by_xpath(
                        #         ".//*[@class='Login-socialButtonGroup']/div[2]").click()  # 点击qq登陆
                        #     time.sleep(10)  # 网络不通畅时将时间再延长
                        #     # self.web.find_element_by_xpath(
                        #     #     ".//*[@class='Login-socialButtonGroup']/div[1]").click()  # 点击微信登陆,待启用
                        #     # self.web.find_element_by_xpath(
                        #     #     ".//*[@class='Login-socialButtonGroup']/div[3]").click()  # 点击微博登陆，待启用
                        # except:
                        #     pass
                        #没有点击查看全部了
                        # self.web.find_element_by_xpath(".//*[@class='Card ViewAll']/a").click() #点击查看全部内容
                        # time.sleep(0.5)
                        # js = "var q=document.documentElement.scrollTop=100000"
                        # self.web.execute_script(js)
                        # time.sleep(4)
                        # 在向下加载一次，加载更多内容
                        js = "var q=document.documentElement.scrollTop=300000"#
                        self.web.execute_script(js)
                        time.sleep(4)
                        count = len(Selector(text=self.web.page_source).xpath(".//div[@class = 'ListShortcut']")[0].xpath(".//div[@class = 'List-item']").extract())#获取当前回答个数
                        Selector(text=self.web.page_source).xpath(".//div[@class = 'ListShortcut']")[0].xpath(".//div[@class = 'List-item'][1]")
                        for i in range(1, count):  # 将所有回答内容的评论都加载出来
                            try:
                                self.web.find_element_by_xpath(".//div[@class='ListShortcut']").find_element_by_xpath(".//div[@class = 'List-item'][%d]"%i)\
                                    .find_element_by_xpath(".//button[contains(@class,'Button--withLabel')and contains(@class,'ContentItem-action')]/span").click()
                                time.sleep(0.5)
                                print(20*' {}'.format(i))
                            except Exception as e:
                                #再试一次
                                try:
                                    pdb.set_trace()
                                    self.web.find_element_by_xpath(".//div[@class='ListShortcut']").find_element_by_xpath(".//div[@class = 'List-item'][%d]" % i) \
                                        .find_element_by_xpath( ".//button[contains(@class,'Button--withLabel')and contains(@class,'ContentItem-action')]/span").click()
                                    time.sleep(1)
                                except:
                                    pass
                                print(e)
                                print('lalalalalalalalalalallaal')
                                pass
                        body = self.web.page_source
                        return HtmlResponse(url=self.web.current_url, body=body, encoding="utf-8", request=request)
                    except Exception as e:
                        print(20*'lalal')
                        print(e)
                        pass

            #搜索主页面,需要点击登录
            elif spider.name == "film" and str(request.url).startswith(
                    'https://www.zhihu.com/search?type=content&q='):
                self.web.get(request.url)
                time.sleep(1.5)
                # pdb.set_trace()
                a = 1
                self.web.find_element_by_xpath(".//*[@class='AppHeader-profile']/div/button").click()
                # 点击社交网络账号登陆
                try:
                    # pdb.set_trace()
                    time.sleep(2)
                    self.web.find_element_by_xpath(".//*[@class='Login-socialButtonGroup']/div[2]").click()  # 点击qq登陆
                    time.sleep(10)# 网络不通畅时将时间再延长
                    # self.web.find_element_by_xpath(
                    #     ".//*[@class='Login-socialButtonGroup']/div[1]").click()  # 点击微信登陆,待启用
                    # self.web.find_element_by_xpath(
                    #     ".//*[@class='Login-socialButtonGroup']/div[3]").click()  # 点击微博登陆，待启用
                except:
                    pass

                # js = "var q=document.documentElement.scrollTop=100000"
                # self.web.execute_script(js)
                # time.sleep(2)
                # self.web.refresh()
                # time.sleep(2)
                js = "var q=document.documentElement.scrollTop=2000000"  #
                self.web.execute_script(js)
                time.sleep(5)
                body = self.web.page_source
                return HtmlResponse(url=self.web.current_url, body=body, encoding="utf-8", request=request)

        except Exception as e:
            print("webdriver111111111111111111111111111111111111111 失败")
            print(e)
            print("webdriver111111111111111111111111111111111111111 失败")
            self.web.close()
            return response

        # AppHeader - login
