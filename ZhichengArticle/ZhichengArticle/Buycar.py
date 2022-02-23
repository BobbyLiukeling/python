

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
    str = 'https://www.zhihu.com/search?type=content&q='
    urls = label.a['版权专利']
    path = []
    for a in urls[:1]:
        path.append(str+'办理'+a+'手续的流程')
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
        # pdb.set_trace()
        try:
            line = parse.unquote(response.url)
            tag = line.split('=')[-1]
            tag = tag[2:]
            tag = tag[:-5]
            node1s = response.xpath(".//div[@class = 'List']")[0].xpath(".//h2/a/@href").extract()
            node2s = response.xpath(".//div[@class = 'List']")[0].xpath(".//h2/div/a/@href").extract()
            # pdb.set_trace()
            count = len(node1s)
            # for url in node1s:
            #     count -= count
            #     url = 'https:'+url
            #     if count>-1:
            #         yield scrapy.Request(url=url, callback=self.zhuanlan_parse, meta={'tag':tag})
            #         pass
            #     # else:
            #     #     for urls in node2s:
            #     #         urls = 'https://www.zhihu.com' + urls
            #     #         yield scrapy.Request(url=urls, callback=self.Q_parse, meta={'tag':tag})#最后一次的时候传递下一个页面
            for urls in node2s:
                urls = 'https://www.zhihu.com' + urls
                yield scrapy.Request(url=urls, callback=self.Q_parse, meta={'tag': tag})  # 最后一次的时候传递下一个页面
        except Exception as e:
            print('1' * 20)
            print(e)

    # def zhuanlan_parse(self, response):#爬取评论
    #     try:
    #         # pdb.set_trace()
    #         username = response.xpath(".//div[@id = 'Popover3-toggle']/a/text()").extract()[0]
    #         title = response.xpath(".//h1[@class = 'Post-Title']/text()").extract()[0]
    #         sql = 'select id from buycar where user = "{0}" and title = "{1}"'.format(username, title)
    #         self.cursor.execute(sql)
    #         id = self.cursor.fetchone()[0]
    #         item = CommentItem()
    #         # pdb.set_trace()
    #         try:
    #             s = response.xpath(".//div[@class = 'CommentListV2']/ul").extract()
    #         except Exception as e:
    #             s = 0
    #         for i in range(1, len(s) + 1):
    #             comment_user = response.xpath( ".//div[@class = 'CommentListV2']/ul[i]/li/div/div/div/span[@class = 'UserLink']/a/text()").extract()[0]
    #             comment_content = response.xpath(".//div[@class = 'CommentListV2']/ul[i]/li/div/div/div/div/div/text()").extract()[0]
    #             try:
    #                 fav_nums2 = int(response.xpath(
    #                     ".//div[@class = 'CommentListV2']/ul[i]/li/div/div/div[2]/div[2]/button/text()").extract()[0])
    #             except:
    #                 fav_nums2 = 0
    #             item['article_id'] = 2
    #             item['comment_user'] = comment_user
    #             item['comment_content'] = comment_content
    #             item['fav_nums'] = fav_nums2
    #             yield item
    #     except Exception as e:  # 没有评论
    #         print(e)
    #         pass

    def zhuanlan_parse(self, response):
        try:
            # pdb.set_trace()
            item = ZhichengarticleItem()
            username = response.xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]
            title = response.xpath(".//h1[@class = 'Post-Title']/text()").extract()[0]
            content = response.xpath(".//div[@class = 'RichText ztext Post-RichText']").extract()[0]
            try:
                fav_nums = response.xpath(".//div[@class = 'ContentItem-actions']/span/button/text()").extract()[1]
            except:
                fav_nums = '0'
            # try:
            #     comment = response.xpath(".//div[@class = 'ContentItem-actions']/button/text()").extract()[1]
            #     response.xpath(".//div[@class = 'ContentItem-actions']/button").extract()[0]#评论点击
            # except:
            #     pass
            add_time = response.xpath(".//div[@class = 'ContentItem-time']/text()").extract()[0].split(' ')[1]
            item['user'] = username
            item['title'] = title
            item['content'] = content
            item['url'] = response.url
            item['fav_nums'] = fav_nums
            item['add_time'] = add_time
            item['tag'] = response.meta['tag']

            yield item

            #将评论内容传递到下一个页面爬取
            # pdb.set_trace()
            # sql = 'select id from buycar where user = "{0}" and title = "{1}"'.format(username, title)
            # self.cursor.execute(sql)
            # id = self.cursor.fetchone()[0]
            # url = response.url
            # # yield scrapy.Request(url=url, callback=self.zhuanlan_parse, meta={'tag': tag})
            # yield scrapy.Request(url=url, callback=self.comment, meta={'id': id})

        except Exception as e:
            print('2' * 20)
            print(e)

    # def comment(self,response):
    #     pdb.set_trace()
    #     item = CommentItem()
    #     try:
    #         for i in range(1, len(response.xpath(".//div[@class = 'CommentListV2']/ul").extract()) + 1):
    #             comment_user = response.xpath(
    #                 ".//div[@class = 'CommentListV2']/ul[i]/li/div/div/div/span[@class = 'UserLink']/a/text()").extract()[
    #                 0]
    #             comment_content = response.xpath(".//div[@class = 'CommentListV2']/ul[i]/li/div/div/div/div/div/text()").extract()[0]
    #             try:
    #                 fav_nums2 = int(response.xpath(
    #                     ".//div[@class = 'CommentListV2']/ul[i]/li/div/div/div[2]/div[2]/button/text()").extract()[0])
    #             except:
    #                 fav_nums2 = 0
    #             item['article_id'] = response.meta['id']
    #             item['comment_user'] = comment_user
    #             item['comment_content'] = comment_content
    #             item['fav_nums'] = fav_nums2
    #             yield item
    #     except:  # 没有评论
    #         print('8 '*25)
    #         pass



    def Q_parse(self,response):
        try:
            item = QuestionItem()
            # pdb.set_trace()
            try:
                user = response.xpath(".//div[@class = 'AnswerAuthor-user-name']/span/text()").extract()[0]
            except:
                user = response.xpath(".//div[@class = 'AnswerAuthor-user-name']/span/a/text()").extract()[0]
            Q_title = response.xpath(".//div[@class = 'QuestionHeader-main']/h1/text()").extract()[0]
            try:
                Q_content = response.xpath(".//div[@class = 'QuestionHeader-detail']/div/div/span/text()").extract()[0]
            except:
                Q_content =''
            labels = response.xpath(".//div[@class = 'Tag QuestionTopic']/span/a/div/div/text()").extract()
            label = ''
            for i in labels:
                label = label+' '+i
            nums = response.xpath(".//strong[@class = 'NumberBoard-itemValue']/text()").extract()
            focus_nums = nums[0]
            try:
                focus_nums = int(focus_nums)
            except:
                num = focus_nums.split(',')
                t=''
                for i in nums:
                    focus_nums = int(t+i)
            view_nums = nums[1]
            try:
                view_nums = int(focus_nums)
            except:
                num = view_nums.split(',')
                t=''
                for i in nums:
                    view_nums = int(t+i)
            answer_nums = response.xpath(".//div[@class = 'Question-mainColumn']/div/a/text()").extract()[0]
            answer_nums = re.findall(r'\d',answer_nums)[0]

            item['user'] = user
            item['Q_title'] =Q_title
            item['Q_content'] =Q_content
            item['label'] =label
            item['url'] =response.url
            item['focus_nums'] =focus_nums
            item['answer_nums'] =answer_nums
            item['view_nums'] =view_nums
            item['tag'] = response.meta['tag']
            yield item

            url = response.url
            s = url.split('/')
            t = len(s)
            u = ''
            for i in s:
                u = u + i
                t = t - 1
                if t == 2:
                    break
                else:
                    u = u + '/'
            yield scrapy.Request(url=u, callback=self.A_parse,meta={'Q_user':user,'Q_title':Q_title,'tag':response.meta['tag']})
        except Exception as e:
            print('3' * 20)
            print(e)
            pass

    def A_parse(self,response):
        try:
            item = AnswerItem()

            sql = 'select id from question where user = "{0}" and Q_title = "{1}"'.format(response.meta['Q_user'],response.meta['Q_title'])
            # pdb.set_trace()
            self.cursor.execute(sql)
            item['question_id'] = self.cursor.fetchone()[0]
            lists = response.xpath(".//div[@class = 'ContentItem AnswerItem']")

            for List in lists:
                # pdb.set_trace()
                try:
                    user = List.xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]
                except:
                    user = '匿名用户'
                try:

                    comment_nums = List.xpath(".//div[@class = 'ContentItem-actions']/button/text()").extract()[0]
                # try:
                    comment_nums = int(re.findall(r'\d', comment_nums)[0])
                except:
                    comment_nums = 0
                s = List.xpath(".//div[@class = 'RichContent-inner']/span/text()").extract()
                content = ''
                for i in s:
                    content = content + i
                fav_nums = List.xpath(".//div[starts-with(@class,'ContentItem-actions')]/span/button/text()").extract()[-1]
                if fav_nums.endswith('K'):#点赞数超过1K
                    fav_nums = fav_nums[0:len(fav_nums) - 1]
                    a = fav_nums.split('.')
                    if len(a) == 2:# fav_nums = '4.6K'
                        fav_nums = int(a[0]+a[1])*100
                    elif len(a) == 1:#fav_nums ='4K'
                        fav_nums = int(a[0])*1000
                else:
                    try:
                        fav_nums = int(fav_nums)#点赞数未超过1K
                    except:#没有点赞数
                        fav_nums = 0
                add_time = List.xpath(".//div[@class = 'ContentItem-time']/a/span/text()").extract()[0].split(' ')[1]
                # pdb.set_trace()
                item['user'] = user
                item['comment_nums'] = comment_nums
                item['content'] = content
                item['fav_nums'] = fav_nums
                item['add_time'] = add_time
                item['tag'] = response.meta['tag']
                yield item



                # sql = 'select id from answer where question_id = "{0}" and A_user = "{1}"'.format(item['question_id'], user)
                # self.cursor.execute(sql)
                # id = self.cursor.fetchone()[0]
                # url = response.url
                # # yield scrapy.Request(url=url, callback=self.zhuanlan_parse, meta={'tag': tag})
                # yield scrapy.Request(url=url, callback=self.comment, meta={'id': id})

        except Exception as e:
            print('4'*20)
            print(e)








