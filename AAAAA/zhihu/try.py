# -*- coding: utf-8 -*-
import scrapy
from ..items import ZhihuItem,QuestionItem,AnswerItem,CommentItem
import pymysql
import re
from urllib import parse
import pdb
from .import lables
import traceback, sys
from scrapy.selector import Selector



class FilmSpider(scrapy.Spider):

    name = 'film'
    str = 'https://www.zhihu.com/'
    urls = lables.w
    path = []
    for w in urls[1:3]:
        path.append(str + w)
    start_urls = path


    def __init__(self):
        self.db = pymysql.connect(host="localhost", port=3306, user="root", passwd='867425', db="zhihufilm",
                             charset="utf8")

        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            print('* ' * 50)
            return closed(reason)

#爬取内容

    def parse(self, response):
        try:
            item = QuestionItem()
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
            # pdb.set_trace()
            yield item

            #提问——回答
            count = len(response.xpath(".//div[@class = 'ListShortcut']")[0].xpath(".//div[@class = 'List-item']").extract())
            for i in range(1,count):
                items = AnswerItem()
                sql = 'select id from question where focus_nums = "{0}" and Q_title = "{1}"'.format(focus_nums,  Q_title.encode('utf-8').decode())
                self.cursor.execute(sql)#从数据库提取当前回答的问题的ID
                id = self.cursor.fetchone()[0]
                try:
                    user_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]#回答用户名
                except:
                    user_A = '匿名用户'
                # print(20 * '@#$' + '  comment_nums_A')
                # #'1,734 条评论'  提取评论数
                try:
                    comment_nums_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[contains(@class, 'ContentItem-actions') and contains(@class, 'RichContent-actions')]/button/text()").extract()[0]
                    tmp = re.findall(r'[1-9]+\.?[0-9]*', str(comment_nums_A))
                    s = ''
                    for i in tmp:
                        if i.isdigit():
                            s = s + i
                    comment_nums_A = int(s)  # 提取数字
                except:
                    comment_nums_A = 0
                # print(20 * '@#$' + '  anwser_content_A')
                #回答内容
                anwser_content_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[@class = 'RichContent-inner']/span").extract()[0]
                # print(20 * '@#$' + '  fav_nums_A')
                fav_nums_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[starts-with(@class,'ContentItem-actions')]/span/button/text()").extract()[-1]
                if fav_nums_A.endswith('K'):  # 点赞数超过1K
                    fav_nums_A = fav_nums_A[0:-1]
                    a = fav_nums_A.split(' ')[-1].split('.')
                    if len(a) == 2:  # fav_nums_A = '4.6K'
                        fav_nums_A = int(a[0] + a[1]) * 100
                    elif len(a) == 1:  # fav_nums_A ='4K'
                        fav_nums_A = int(a[0]) * 1000
                else:#赞同 212
                    fav_nums_A = int(fav_nums_A.split(' ')[-1])
                add_time_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[@class = 'ContentItem-time']/a/span/text()").extract()[0].split(' ')[1]
                items['add_time'] = add_time_A
                items['content'] = anwser_content_A
                items['tag'] = '上海堡垒'
                items['user'] = user_A.encode('utf-8').decode()
                items['comment_nums'] = comment_nums_A
                items['fav_nums'] = fav_nums_A
                items['question_id'] = id
                yield items



                #answer下的comment
                try:
                    comment_totle = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]",temp=i).extract()[0]  # 定位到回答
                    Len = len(Selector(text=comment_totle).xpath( ".//div[@class = 'CommentListV2']/ul[@class = 'NestComment']").extract())
                    if Len != 0:  # 评论加载出来了
                        for j in range(1, Len):
                            comment_C_A = Selector(text=comment_totle).xpath(".//div[@class = 'CommentListV2']/ul[@class = 'NestComment'][$temp2]", temp2=j).extract()[0]  # 定位到回答某条评论
                            comment_C_user = Selector(text=comment_C_A).xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]
                            try:
                                comment_C_content = Selector(text=comment_C_A).xpath(".//div[contains(@class,'RichText') and contains(@class ,'ztext')]/text()").extract()[0]
                            except:
                                comment_C_content = Selector(text=comment_C_A).xpath( ".//div[contains(@class,'RichText') and contains(@class ,'ztext')]/p/text()").extract()[0]
                            try:
                                fav_C_nums = int(Selector(text=comment_C_A).xpath(".//div[@class = 'CommentItemV2-footer']/button[1]/text()").extract()[0])  # "1222"
                            except:
                                fav_C_nums = 0
                            try:
                                sql = 'select id from answer where A_user = "{0}" and fav_nums = "{1}"'.format(user_A, fav_nums_A)
                                self.cursor.execute(sql)
                                id = self.cursor.fetchone()[0]
                            except:
                                id = 0
                            items_C = CommentItem()
                            items_C['article_id'] = id
                            items_C['comment_user'] = comment_C_user.encode('utf-8').decode()
                            items_C['comment_content'] = comment_C_content.encode('utf-8').decode()
                            items_C['fav_nums'] = fav_C_nums
                            yield items_C
                            print(20*'end')

                except Exception as e:
                    print("question_answer_comment")
                    # pdb.set_trace()
                    print(e)
                    pass

        except Exception as e:
            # pdb.set_trace()
            print(e)
            pass



