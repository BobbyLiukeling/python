# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pdb
from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse

class ZhichengarticleSpiderMiddleware(object):
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


class ZhichengarticleDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.


    def __init__(self):
        self.web = webdriver.Chrome("E:/software/python3.6/chromedriver.exe")

    def process_response(self, request, response, spider):

        try:
            if (spider.name == "Buycar") and str(request.url).startswith('https://www.zhihu.com/search?type=content&q=')==False:
                self.web.get(request.url)
                time.sleep(2)
                # body = self.web.page_source
                # return HtmlResponse(url=self.web.current_url, body=body, encoding="utf-8", request=request)
                str_url = str(response.url).split('/')
                if len(str_url) == 7 or str_url[-2] == 'p':
                    # self.web.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    # time.sleep(1.5)
                    body = self.web.page_source
                    return HtmlResponse(url=self.web.current_url, body=body, encoding="utf-8", request=request)
                else:
                    self.web.find_element_by_xpath(".//*[@class='Question-main']/div/div/a").click()
                    pdb.set_trace()
                    i = 1
                    # while True:
                    #     try:
                    #         self.web.find_element_by_xpath(".//*[@class = 'List-item'][i]/div/div[2]/div[3]/button").click()
                    #         i=i+1
                    #     except:
                    #         break
                    # self.web.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    # time.sleep(1.5)
                    body = self.web.page_source
                    return HtmlResponse(url=self.web.current_url, body=body, encoding="utf-8", request=request)


            elif spider.name == "Buycar" and str(request.url).startswith('https://www.zhihu.com/search?type=content&q='):

                # pdb.set_trace()
                self.web.get(request.url)
                time.sleep(1.5)
                self.web.find_element_by_xpath(".//*[@class='AppHeader-profile']/div/button").click()#点击登陆
                # web.find_element_by_xpath(".//*[@class='SignContainer-switch']/span").click()#点击登陆
                # 点击社交网络账号登陆
                try:
                    self.web.find_element_by_xpath(".//*[@class='Login-socialLogin']/button").click()  # 点击qq登陆

                    self.web.find_element_by_xpath(".//*[@class='Login-socialButtonGroup']/button[3]").click()  # 点击微博登陆
                except:
                    pass
                time.sleep(6)
                self.web.refresh()
                body = self.web.page_source
                return HtmlResponse(url=self.web.current_url, body=body, encoding="utf-8", request=request)

        except Exception as e:
            print(e)
            print("webdriver 失败")
            self.web.close()
            return response




# class JSMiddleware(object):
#     def process_request(self, request, spider):
#         web = webdriver.Chrome("E:/software/python3.6/chromedriver.exe")
#         try:
#             if spider.name == "Buycar":
#                 web.get(request.url)
#                 web.find_element_by_xpath(".//*[@class='SignContainer-switch']/span").click()
#                 # 点击社交网络账号登陆
#                 web.find_element_by_xpath(".//*[@class='Login-socialLogin']/button").click()  # 点击微博登陆
#                 web.find_element_by_xpath(".//*[@class='Login-socialButtonGroup']/button[3]").click()  # 点击微博登陆
#                 time.sleep(10)
#                 web.refresh()
#                 body = web.page_source
#                 print("访问:{0}".format(request.url))
#                 print("^" * 50)
#                 return HtmlResponse(url=web.current_url, body=body, encoding="utf-8", request=request)
#         except Exception as e:
#             print(e)
#             print("webdriver 失败")
#             return None


