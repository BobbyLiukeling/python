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

    name = 'XXXfilm'
    str = 'https://www.zhihu.com/search?type=content&q='
    urls = lables.a
    path = []
    for a in urls[:1]:
        path.append(str + a)
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
        # pdb.set_trace()
        try:
            line = parse.unquote(response.url)
            # pdb.set_trace()
            tag = line.split('=')[-1]

            node1s = response.xpath(".//div[@class = 'List']")[0].xpath(".//h2/a/@href").extract()
            node2s = response.xpath(".//div[@class = 'List']")[0].xpath(".//h2/div/a/@href").extract()
            pdb.set_trace()


            print(20*"$%$%")
            s = []
            for i in node2s:
                s.append(i)
                print(i)
            pdb.set_trace()
            # for url in node1s:
            #     # pdb.set_trace()
            #     url = 'https:' + url
            #     yield scrapy.Request(url=url, callback=self.zhuanlan_parse, meta={'tag': tag})

            for url in node2s[1:2]:
                # pdb.set_trace()
                url = 'https://www.zhihu.com' + url
                yield scrapy.Request(url=url, callback=self.Q_parse, meta={'tag': tag})  # 最后一次的时候传递下一个页面
        except Exception as e:
            print('100' * 20)
            print(e)


    def zhuanlan_parse(self, response):
        try:
            # 话题专栏
            item = ZhihuItem()
            username = response.xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]
            title = response.xpath(".//h1[@class = 'Post-Title']/text()").extract()[0]
            content = response.xpath(".//div[@class = 'RichText ztext Post-RichText']").extract()[0]
            try:
                fav_nums = response.xpath(".//div[@class = 'ContentItem-actions']/span/button/text()").extract()[0]
            except:
                fav_nums = '0'
            try:
                comment = response.xpath(".//div[@class = 'ContentItem-actions']/button/text()").extract()[1]
                response.xpath(".//div[@class = 'ContentItem-actions']/button").extract()[0]#评论点击
            except:
                pass
            add_time = response.xpath(".//div[@class = 'ContentItem-time']/text()").extract()[0].split(' ')[1]
            fav_nums = fav_nums.split(' ')[-1]
            if fav_nums.endswith('K') == True :
                fav_nums = fav_nums[0:-1] #去掉K
                fav_nums =int(float(fav_nums)*1000)
            else: #点赞未到1000 是数字
                fav_nums = int(fav_nums)

            item['user'] = username.encode('utf-8').decode()
            item['title'] = title.encode('utf-8').decode()
            item['content'] = content.encode('utf-8').decode()
            item['url'] = response.url
            item['fav_nums'] = fav_nums
            item['add_time'] = add_time
            item['tag'] = response.meta['tag'].encode('utf-8').decode()
            # pdb.set_trace()
            yield item

            items = CommentItem()
            try:
                # pdb.set_trace()
                # comment_content = response.xpath(".//div[@class = 'CommentListV2']/ul[1]")[0].xpath(".//div[@class = 'CommentItemV2-footer']/button/text()").extract()[0]
                a = len(response.xpath(".//div[@class = 'CommentListV2']/ul").extract()) + 1

                for i in range(1, a):
                    comment_user = response.xpath(".//div[@class = 'CommentListV2']/ul[$number]", number = i)[0].xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]
                    comment_content = response.xpath(".//div[@class = 'CommentListV2']/ul[$number]", number = i)[0].xpath(".//div[@class = 'CommentItemV2-metaSibling']/div/div/text()").extract()[0]
                    try:
                        fav_nums2 = response.xpath(".//div[@class = 'CommentListV2']/ul[$number]", number = i)[0].xpath(".//div[@class = 'CommentItemV2-footer']/button/text()").extract()[0]
                        fav_nums2 = fav_nums2.split(' ')[-1]
                        if fav_nums2.endswith('K') == True:
                            fav_nums2 = fav_nums2[0:-1]  # 去掉K
                            fav_nums2 = int(float(fav_nums2) * 1000)
                        else:  # 点赞未到1000 是数字
                            fav_nums2 = int(fav_nums2)

                    except:#为提取到有效点赞数
                        fav_nums2 = 0
                    # pdb.set_trace()
                    sql = 'select * from article_comment where comment_user = "{0}" and fav_nums = "{1}"'.format( comment_user , fav_nums2)
                    self.cursor.execute(sql)
                    if self.cursor.fetchall(): #出现重复跳出本次循环
                        print(50*'123  ')
                        continue

                    sql = 'select id from buycar where user = "{0}" and title = "{1}"'.format(username, title)
                    self.cursor.execute(sql)
                    id = self.cursor.fetchone()[0]

                    items['article_id'] = id
                    items['comment_user'] = comment_user.encode('utf-8').decode()
                    items['comment_content'] = comment_content.encode('utf-8').decode()
                    items['fav_nums'] = fav_nums2
                    yield items


            except Exception as e:  # 没有评论
                # pdb.set_trace()
                print(e)
                print('8 ' * 40)



        except Exception as e:
            print('2' * 20)
            info = sys.exc_info()
            print(info[0], ":", info[1])
            traceback.print_exc()
            print(e)



    def Q_parse(self, response):
        try:
            pdb.set_trace()
            item = QuestionItem()
            url = response.url
            #话题
            if 'answer' not in url.split('/')[-2]: #话题https://www.zhihu.com/topic/339494002
                user = "topic"
                Q_content = response.xpath(".//h1[@class = 'QuestionHeader-title']/text()").extract()[0]
                answer_nums = response.xpath(".//h4[@class = 'List-headerText']/span/text()").extract()[0]
                answer_nums = int(re.findall(r'[0-9]*', answer_nums)[0] ) # 提取数字
            #问答
            else:# 非话题 https://www.zhihu.com/question/61425583/answer/893671923
                try:
                    user = response.xpath(".//div[@class = 'AnswerAuthor-user-name']/span/text()").extract()[0]
                except:
                    user = response.xpath(".//div[@class = 'AnswerAuthor-user-name']/span/a/text()").extract()[0]
                try:
                    Q_content =  response.xpath(".//div[@class = 'QuestionHeader-detail']/div/div/span/text()").extract()[0]
                except:
                    Q_content = ''
                answer_nums = response.xpath(".//div[@class = 'Question-mainColumn']/div/a/text()").extract()[0]
            tmp = re.findall(r'[1-9]+\.?[0-9]*', str(answer_nums))
            s =''
            for i in tmp:
                if i.isdigit():
                    s = s+i
            answer_nums = int(s)#提取数字
            labels = response.xpath(".//div[@class = 'Tag QuestionTopic']/span/a/div/div/text()").extract()
            label = ''
            for i in labels:
                label = label + ' ' + i
            Q_title = response.xpath(".//div[@class = 'QuestionHeader-main']/h1/text()").extract()[0]
            # pdb.set_trace()
            nums = response.xpath(".//strong[@class = 'NumberBoard-itemValue']/text()").extract() #关注人数，和 被浏览者人数
            try:
                focus_nums = int(nums[0])
            except:
                focus_nums = int(''.join([str for str in nums[0].split(',')]))
            try:
                view_nums = int(nums[1])
            except: #['1,833,117']将此拼接为数字
                view_nums = int(''.join([str for str in nums[1].split(',')]))
            item['user'] = user.encode('utf-8').decode()
            item['Q_title'] = Q_title.encode('utf-8').decode()
            item['Q_content'] = Q_content.encode('utf-8').decode()
            item['label'] = label
            item['url'] = response.url
            item['focus_nums'] = focus_nums
            item['answer_nums'] = answer_nums
            item['view_nums'] = view_nums
            item['tag'] = response.meta['tag'].encode('utf-8').decode()
            pdb.set_trace()#断点
            yield item


            #提问——回答
            # count = len(response.xpath(".//div[@class = 'ListShortcut']")[0].xpath(".//div[@class = 'List-item']").extract())
            # i = 1
            # if i == 1 :#提取所有回答
            #     items = AnswerItem()
            #     sql = 'select id from question where user = "{0}" and Q_title = "{1}"'.format(user.encode('utf-8').decode(),  Q_title.encode('utf-8').decode())
            #     self.cursor.execute(sql)#从数据库提取当前回答的问题的ID
            #     id = self.cursor.fetchone()[0]
            #
            #     try:
            #         user_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]#回答用户名
            #     except:
            #         user_A = '匿名用户'
            #     print(20 * '@#$' + '  comment_nums_A')
            #     # #'1,734 条评论'  提取评论数
            #     try:
            #         comment_nums_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[contains(@class, 'ContentItem-actions') and contains(@class, 'RichContent-actions')]/button/text()").extract()[0]
            #         tmp = re.findall(r'[1-9]+\.?[0-9]*', str(comment_nums_A))
            #         s = ''
            #         for i in tmp:
            #             if i.isdigit():
            #                 s = s + i
            #         comment_nums_A = int(s)  # 提取数字
            #     except:
            #         comment_nums_A = 0
            #     print(20 * '@#$' + '  anwser_content_A')
            #     #回答内容
            #     anwser_content_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[@class = 'RichContent-inner']/span").extract()[0]
            #     print(20 * '@#$' + '  fav_nums_A')
            #     fav_nums_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[starts-with(@class,'ContentItem-actions')]/span/button/text()").extract()[-1]
            #     if fav_nums_A.endswith('K'):  # 点赞数超过1K
            #         fav_nums_A = fav_nums_A[0:-1]
            #         a = fav_nums_A.split(' ')[-1].split('.')
            #         if len(a) == 2:  # fav_nums_A = '4.6K'
            #             fav_nums_A = int(a[0] + a[1]) * 100
            #         elif len(a) == 1:  # fav_nums_A ='4K'
            #             fav_nums_A = int(a[0]) * 1000
            #     else:#赞同 212
            #         fav_nums_A = int(fav_nums_A.split(' ')[-1])
            #     add_time_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[@class = 'ContentItem-time']/a/span/text()").extract()[0].split(' ')[1]
            #
            #     items['add_time'] = add_time_A
            #     items['content'] = anwser_content_A
            #     items['tag'] = response.meta['tag'].encode('utf-8').decode()
            #     items['user'] = user_A.encode('utf-8').decode()
            #     items['comment_nums'] = comment_nums_A
            #     items['fav_nums'] = fav_nums_A
            #     items['question_id'] = id
            #     pdb.set_trace()
            #     yield items
            #
            #     # try:
            #     #     # pdb.set_trace()
            #     #     # sql = "insert into answer(question_id,A_user,comment_nums,content,fav_nums,add_time,tag) values(%s,%s,%s,%s,%s,%s,%s)"
            #     #     # params = (
            #     #     #     id, user_A.encode('utf-8').decode(), comment_nums_A, anwser_content_A[0].encode('utf-8').decode(),
            #     #     #     fav_nums_A, items['add_time'], response.meta['tag'].encode('utf-8').decode()
            #     #     # )
            #     #     pdb.set_trace()
            #     #     # sql_Q = "insert into answer(question_id,A_user,comment_nums,content,fav_nums,tag) values({0},'{1}',{2},'{3}',{4},'{5}')"\
            #     #     #     .format(id, items['user'], items['comment_nums'], items['content'],items['fav_nums'],items['tag'])
            #     #     sql_Q = "insert into answer(question_id,comment_nums,fav_nums) values({0},{1},{2})" .format(id,comment_nums_A, fav_nums_A)
            #     #     self.cursor.execute(sql_Q)
            #     #     sql_Q = "insert into answer(A_user,content,tag) values('{0}','{1}','{2}')".format(items['user'],items['content'],items['tag'])
            #     #     self.cursor.execute(sql_Q)
            #     #
            #     # except Exception as e:
            #     #     print('answer  ' * 20)
            #     #     # print(item['question_id'],item['user'],item['comment_nums'],
            #     #     #     item['fav_nums'],item['add_time'],item['tag'])
            #     #     # print(e)
            #     #     pass
            #
            #     #answer下的comment
            #     # try:
            #     #     comment_totle = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]",temp=i).extract()[0]  # 定位到回答
            #     #     Len = len(Selector(text=comment_totle).xpath( ".//div[@class = 'CommentListV2']/ul[@class = 'NestComment']").extract())
            #     #     if Len != 0:  # 评论加载出来了
            #     #         for j in range(1, Len):
            #     #             comment_C_A = Selector(text=comment_totle).xpath(".//div[@class = 'CommentListV2']/ul[@class = 'NestComment'][$temp2]", temp2=j).extract()[0]  # 定位到回答某条评论
            #     #             comment_C_user = Selector(text=comment_C_A).xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]
            #     #             try:
            #     #                 comment_C_content = Selector(text=comment_C_A).xpath(".//div[contains(@class,'RichText') and contains(@class ,'ztext')]/text()").extract()[0]
            #     #             except:
            #     #                 comment_C_content = Selector(text=comment_C_A).xpath( ".//div[contains(@class,'RichText') and contains(@class ,'ztext')]/p/text()").extract()[0]
            #     #             try:
            #     #                 fav_C_nums = int(Selector(text=comment_C_A).xpath(".//div[@class = 'CommentItemV2-footer']/button[1]/text()").extract()[0])  # "1222"
            #     #             except:
            #     #                 fav_C_nums = 0
            #     #             try:
            #     #                 sql = 'select id from answer where A_user = "{0}" and fav_nums = "{1}"'.format(user_A, fav_nums_A)
            #     #                 self.cursor.execute(sql)
            #     #                 id = self.cursor.fetchone()[0]
            #     #             except:
            #     #                 id = 0
            #     #
            #     #             try:
            #     #                 sql_C = "replace into article_comment(article_id ,comment_user,comment_content,fav_nums) values(%s,%s,%s,%s)"
            #     #                 params_C = (
            #     #                     id, comment_C_user.encode('utf-8').decode(), comment_C_content.encode('utf-8').decode(), fav_C_nums
            #     #                 )
            #     #                 self.cursor.execute(sql_C, params_C)
            #     #             except Exception as e:
            #     #                 print('comment   ' * 20)
            #     #                 print(e)
            #     #                 pass
            #     # except Exception as e:
            #     #     print("question_answer_comment")
            #     #     print(e)
            #     #     pass
        except Exception as e:
            print('3' * 20)
            print(e)
            pass




    # def Q_parse(self, response):
    #     try:
    #         # item = QuestionItem()
    #         url = response.url
    #         # pdb.set_trace()
    #         #
    #         if 'answer' not in url.split('/')[-2]: #话题https://www.zhihu.com/question/339494002
    #             user = "topic"
    #             # Q_content = response.xpath(".//h1[@class = 'QuestionHeader-title']/text()").extract()[0]
    #             # answer_nums = response.xpath(".//h4[@class = 'List-headerText']/span/text()").extract()[0]
    #
    #             # answer_nums = int(re.findall(r'[0-9]*', answer_nums)[0] ) # 提取数字
    #
    #         else:# 非话题 https://www.zhihu.com/question/61425583/answer/893671923
    #             try:
    #                 user = response.xpath(".//div[@class = 'AnswerAuthor-user-name']/span/text()").extract()[0]
    #             except:
    #                 user = response.xpath(".//div[@class = 'AnswerAuthor-user-name']/span/a/text()").extract()[0]
    #             # try:
    #             #     Q_content =  response.xpath(".//div[@class = 'QuestionHeader-detail']/div/div/span/text()").extract()[0]
    #             # except:
    #             #     Q_content = ''
    #             # answer_nums = response.xpath(".//div[@class = 'Question-mainColumn']/div/a/text()").extract()[0]
    #         # tmp = re.findall(r'[1-9]+\.?[0-9]*', str(answer_nums))
    #         # s =''
    #         # for i in tmp:
    #         #     if i.isdigit():
    #         #         s = s+i
    #         # answer_nums = int(s)#提取数字
    #         # labels = response.xpath(".//div[@class = 'Tag QuestionTopic']/span/a/div/div/text()").extract()
    #         # label = ''
    #         # for i in labels:
    #         #     label = label + ' ' + i
    #         #
    #         Q_title = response.xpath(".//div[@class = 'QuestionHeader-main']/h1/text()").extract()[0]
    #         # # pdb.set_trace()
    #         # nums = response.xpath(".//strong[@class = 'NumberBoard-itemValue']/text()").extract() #关注人数，和 被浏览者人数
    #         # try:
    #         #     focus_nums = int(nums[0])
    #         # except:
    #         #     focus_nums = int(''.join([str for str in nums[0].split(',')]))
    #         # try:
    #         #     view_nums = int(nums[1])
    #         # except: #['1,833,117']将此拼接为数字
    #         #     view_nums = int(''.join([str for str in nums[1].split(',')]))
    #         #
    #         # item['user'] = user.encode('utf-8').decode()
    #         # item['Q_title'] = Q_title.encode('utf-8').decode()
    #         # item['Q_content'] = Q_content.encode('utf-8').decode()
    #         # item['label'] = label
    #         # item['url'] = response.url
    #         # item['focus_nums'] = focus_nums
    #         # item['answer_nums'] = answer_nums
    #         # item['view_nums'] = view_nums
    #         # item['tag'] = response.meta['tag'].encode('utf-8').decode()
    #         # yield item
    #
    #
    #
    #         #提问回答
    #
    #         # pdb.set_trace()
    #         count = len(response.xpath(".//div[@class = 'ListShortcut']")[0].xpath(".//div[@class = 'List-item']").extract())
    #         for i in range(1,count):#提取所有回答
    #             # items = AnswerItem()
    #             # print(20*'@#$'+ '   url_A')
    #             # url_A =  response.xpath(".//div[@class = 'ListShortcut']")[0].xpath(".//div[@class = 'List-item'][$temp]/div/meta[3]/@content", temp=i).extract()[0]#提取链接
    #             #
    #             # sql = 'select id from question where user = "{0}" and Q_title = "{1}"'.format(user.encode('utf-8').decode(),  Q_title.encode('utf-8').decode())
    #             # self.cursor.execute(sql)#从数据库提取当前回答的问题的ID
    #             try:
    #                 user_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]#回答用户名
    #             except:
    #                 user_A = '匿名用户'
    #
    #             # print(20 * '@#$' + '  comment_nums_A')
    #             # #'1,734 条评论'  提取评论数
    #             # try:
    #             #     comment_nums_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[contains(@class, 'ContentItem-actions') and contains(@class, 'RichContent-actions')]/button/text()").extract()[0]
    #             #     tmp = re.findall(r'[1-9]+\.?[0-9]*', str(comment_nums_A))
    #             #     s = ''
    #             #     for i in tmp:
    #             #         if i.isdigit():
    #             #             s = s + i
    #             #     comment_nums_A = int(s)  # 提取数字
    #             # except:
    #             #     comment_nums_A = 0
    #             # print(20 * '@#$' + '  anwser_content_A')
    #             # #回答内容
    #             # anwser_content_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[@class = 'RichContent-inner']/span").extract()
    #             # print(20 * '@#$' + '  fav_nums_A')
    #             fav_nums_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[starts-with(@class,'ContentItem-actions')]/span/button/text()").extract()[-1]
    #             if fav_nums_A.endswith('K'):  # 点赞数超过1K
    #                 fav_nums_A = fav_nums_A[0:-1]
    #                 a = fav_nums_A.split(' ')[-1].split('.')
    #                 if len(a) == 2:  # fav_nums_A = '4.6K'
    #                     fav_nums_A = int(a[0] + a[1]) * 100
    #                 elif len(a) == 1:  # fav_nums_A ='4K'
    #                     fav_nums_A = int(a[0]) * 1000
    #             else:#赞同 212
    #                 fav_nums_A = int(fav_nums_A.split(' ')[-1])
    #         #
    #         #     add_time_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[@class = 'ContentItem-time']/a/span/text()").extract()[0].split(' ')[1]
    #         #     print(20 * '@#$' + '  end')
    #         #     items['tag'] = response.meta['tag'].encode('utf-8').decode()
    #         #     items['question_id'] = self.cursor.fetchone()[0]
    #         #     items['user'] = user_A.encode('utf-8').decode()
    #         #     items['comment_nums'] = comment_nums_A
    #         #     # pdb.set_trace()
    #         #     items['content'] = anwser_content_A[0].encode('utf-8').decode()
    #         #     items['fav_nums'] = fav_nums_A
    #         #     items['add_time'] = add_time_A
    #         #     items['tag'] = response.meta['tag'].encode('utf-8').decode()
    #         #     pdb.set_trace()
    #         #     yield items
    #             # try:
    #             #     yield items
    #             # except StopIteration as s:
    #             #     print(s + 20*'wes#')
    #             #     pass
    #
    #             try:
    #                 items_C = CommentItem()
    #                 # pdb.set_trace()
    #                 comment_totle = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]",temp=i).extract()[0]  # 定位到回答
    #                 Len = len(Selector(text=comment_totle).xpath( ".//div[@class = 'CommentListV2']/ul[@class = 'NestComment']").extract())
    #                 if Len != 0:  # 评论加载出来了
    #                     for j in range(1, Len):
    #                         # pdb.set_trace()
    #                         # print(20*'  C_A')
    #                         comment_C_A = Selector(text=comment_totle).xpath(".//div[@class = 'CommentListV2']/ul[@class = 'NestComment'][$temp2]", temp2=j).extract()[0]  # 定位到回答某条评论
    #                         # print(20*' user')
    #                         comment_C_user = Selector(text=comment_C_A).xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]
    #                         # print(20*' content')
    #                         try:
    #                             comment_C_content = Selector(text=comment_C_A).xpath(".//div[contains(@class,'RichText') and contains(@class ,'ztext')]/text()").extract()[0]
    #                         except:
    #                             comment_C_content = Selector(text=comment_C_A).xpath( ".//div[contains(@class,'RichText') and contains(@class ,'ztext')]/p/text()").extract()[0]
    #                         # print(20 * ' fav')
    #                         try:
    #                             fav_C_nums = int(Selector(text=comment_C_A).xpath(".//div[@class = 'CommentItemV2-footer']/button[1]/text()").extract()[0])  # "1222"
    #                         except:
    #                             fav_C_nums = 0
    #                         # print(20 * ' id')
    #                         try:
    #                             sql = 'select id from answer where A_user = "{0}" and fav_nums = "{1}"'.format(user_A, fav_nums_A)
    #                             self.cursor.execute(sql)
    #                             id = self.cursor.fetchone()[0]
    #                         except:
    #                             id = 0
    #                         # print(20 * ' end')
    #                         pdb.set_trace()
    #                         try:
    #                             yield scrapy.Request(url=url, callback=self.comment_C, dont_filter=True,meta={'id': id,'user':comment_C_user.encode('utf-8').decode(),'content':comment_C_content.encode('utf-8').decode(),'fav_nums':fav_C_nums})
    #                         except StopIteration as s:
    #                             print(s.__repr__())
    #                         # items_C['article_id'] = id
    #                         # items_C['comment_user'] = comment_C_user.encode('utf-8').decode()
    #                         # items_C['comment_content'] = comment_C_content.encode('utf-8').decode()
    #                         # items_C['fav_nums'] = fav_C_nums
    #                         # yield items_C
    #             except Exception as e:
    #                 print("question_answer_comment")
    #                 print(e)
    #                 pass
    #
    #
    #
    #         # items = AnswerItem()
    #         # i = 1
    #         # print(20*'@#$'+ '   url_A')
    #         # url_A =  response.xpath(".//div[@class = 'ListShortcut']")[0].xpath(".//div[@class = 'List-item'][$temp]/div/meta[3]/@content", temp=i).extract()[0]#提取链接
    #         #
    #         # sql = 'select id from question where user = "{0}" and Q_title = "{1}"'.format(user.encode('utf-8').decode(),  Q_title.encode('utf-8').decode())
    #         # self.cursor.execute(sql)#从数据库提取当前回答的问题的ID
    #         # try:
    #         #     user_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]#回答用户名
    #         # except:
    #         #     user_A = '匿名用户'
    #         #
    #         # print(20 * '@#$' + '  comment_nums_A')
    #         # #'1,734 条评论'  提取评论数
    #         # try:
    #         #     comment_nums_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[contains(@class, 'ContentItem-actions') and contains(@class, 'RichContent-actions')]/button/text()").extract()[0]
    #         #     tmp = re.findall(r'[1-9]+\.?[0-9]*', str(comment_nums_A))
    #         #     s = ''
    #         #     for i in tmp:
    #         #         if i.isdigit():
    #         #             s = s + i
    #         #     comment_nums_A = int(s)  # 提取数字
    #         # except:
    #         #     comment_nums_A = 0
    #         # print(20 * '@#$' + '  anwser_content_A')
    #         # #回答内容
    #         # anwser_content_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[@class = 'RichContent-inner']/span").extract()
    #         # print(20 * '@#$' + '  fav_nums_A')
    #         # fav_nums_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[starts-with(@class,'ContentItem-actions')]/span/button/text()").extract()[-1]
    #         # if fav_nums_A.endswith('K'):  # 点赞数超过1K
    #         #     fav_nums_A = fav_nums_A[0:-1]
    #         #     a = fav_nums_A.split(' ')[-1].split('.')
    #         #     if len(a) == 2:  # fav_nums_A = '4.6K'
    #         #         fav_nums_A = int(a[0] + a[1]) * 100
    #         #     elif len(a) == 1:  # fav_nums_A ='4K'
    #         #         fav_nums_A = int(a[0]) * 1000
    #         # else:#赞同 212
    #         #     fav_nums_A = int(fav_nums_A.split(' ')[-1])
    #         #
    #         # add_time_A = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).xpath(".//div[@class = 'ContentItem-time']/a/span/text()").extract()[0].split(' ')[1]
    #         # print(20 * '@#$' + '  end')
    #         # items['tag'] = response.meta['tag'].encode('utf-8').decode()
    #         # items['question_id'] = self.cursor.fetchone()[0]
    #         # items['user'] = user_A.encode('utf-8').decode()
    #         # items['comment_nums'] = comment_nums_A
    #         # # pdb.set_trace()
    #         # items['content'] = anwser_content_A[0].encode('utf-8').decode()
    #         # items['fav_nums'] = fav_nums_A
    #         # items['add_time'] = add_time_A
    #         # items['tag'] = response.meta['tag'].encode('utf-8').decode()
    #         # pdb.set_trace()
    #         # yield items
    #
    #         #anwser_comment
    #         # yield scrapy.Request(url=url, callback=self.Q_parse, meta={'tag': tag})
    #         # try:
    #         #     items_C = CommentItem()
    #         #     pdb.set_trace()
    #         #     comment_totle = response.xpath(".//div[@class = 'ListShortcut']").xpath(".//div[@class = 'List-item'][$temp]", temp=i).extract()[0]#定位到回答
    #         #     Len = len(Selector(text=comment_totle).xpath(".//div[@class = 'CommentListV2']/ul[@class = 'NestComment']").extract())
    #         #     for j in range(1, Len):
    #         #         if Len != 0:  # 评论加载出来了
    #         #             comment_C_A = Selector(text=comment_totle).xpath(".//div[@class = 'CommentListV2']/ul[@class = 'NestComment'][$temp2]",temp2 = j).extract()[0]#定位到回答某条评论
    #         #             comment_C_user = Selector(text=comment_C_A).xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]
    #         #             comment_C_content = Selector(text=comment_C_A).xpath(".//div[contains(@class,'RichText') and contains(@class ,'ztext')]/text()").extract()[0]
    #         #             try:
    #         #                 fav_C_nums =  int(Selector(text=comment_C_A).xpath(".//div[@class = 'CommentItemV2-footer']/button[1]/text()").extract()[0])   # "1222"
    #         #             except:
    #         #                 fav_C_nums = 0
    #         #             sql = 'select id from answer where user = "{0}" and fav_nums = "{1}"'.format(user_A, fav_nums_A)
    #         #             self.cursor.execute(sql)
    #         #             id = self.cursor.fetchone()[0]
    #         #
    #         #
    #         #             items_C['article_id'] = id
    #         #             items_C['comment_user'] = comment_C_user.encode('utf-8').decode()
    #         #             items_C['comment_content'] = comment_C_content.encode('utf-8').decode()
    #         #             items_C['fav_nums'] = fav_C_nums
    #         #             yield items_C
    #
    #
    #     except Exception as e:
    #         print('3' * 20)
    #         print(e)
    #         pass


    # def comment_C(self, response):
    #     pdb.set_trace()
    #     item = CommentItem()
    #     item['article_id'] = id
    #     item['comment_user'] = response.meta['user']
    #     item['comment_content'] = response.meta['content']
    #     item['fav_nums'] = response.meta['fav_nums']
    #     yield item
    #
    #
    # def A_parse(self, response):
    #     try:
    #         item = AnswerItem()
    #         pdb.set_trace()
    #         sql = 'select id from question where user = "{0}" and Q_title = "{1}"'.format(response.meta['Q_user'], response.meta['Q_title'])
    #
    #         self.cursor.execute(sql)
    #         item['question_id'] = self.cursor.fetchone()[0]
    #         lists = response.xpath(".//div[@class = 'ContentItem AnswerItem']")
    #
    #         for List in lists:
    #             # pdb.set_trace()
    #             try:
    #                 user = List.xpath(".//a[@class = 'UserLink-link']/text()").extract()[0]
    #             except:
    #                 user = '匿名用户'
    #             try:
    #
    #                 comment_nums = List.xpath(".//div[@class = 'ContentItem-actions']/button/text()").extract()[0]
    #                 # try:
    #                 comment_nums = int(re.findall(r'\d', comment_nums)[0])
    #             except:
    #                 comment_nums = 0
    #             s = List.xpath(".//div[@class = 'RichContent-inner']/span/text()").extract()
    #             content = ''
    #             for i in s:
    #                 content = content + i
    #             fav_nums = \
    #             List.xpath(".//div[starts-with(@class,'ContentItem-actions')]/span/button/text()").extract()[-1]
    #             if fav_nums.endswith('K'):  # 点赞数超过1K
    #                 fav_nums = fav_nums[0:len(fav_nums) - 1]
    #                 a = fav_nums.split('.')
    #                 if len(a) == 2:  # fav_nums = '4.6K'
    #                     fav_nums = int(a[0] + a[1]) * 100
    #                 elif len(a) == 1:  # fav_nums ='4K'
    #                     fav_nums = int(a[0]) * 1000
    #             else:
    #                 try:
    #                     fav_nums = int(fav_nums)  # 点赞数未超过1K
    #                 except:  # 没有点赞数
    #                     fav_nums = 0
    #             add_time = List.xpath(".//div[@class = 'ContentItem-time']/a/span/text()").extract()[0].split(' ')[1]
    #             # pdb.set_trace()
    #             item['user'] = user.encode('utf-8').decode()
    #             item['comment_nums'] = comment_nums
    #             item['content'] = content.encode('utf-8').decode()
    #             item['fav_nums'] = fav_nums
    #             item['add_time'] = add_time
    #             item['tag'] = response.meta['tag'].encode('utf-8').decode()
    #             yield item
    #
    #             # sql = 'select id from answer where question_id = "{0}" and A_user = "{1}"'.format(item['question_id'], user)
    #             # self.cursor.execute(sql)
    #             # id = self.cursor.fetchone()[0]
    #             # url = response.url
    #             # # yield scrapy.Request(url=url, callback=self.zhuanlan_parse, meta={'tag': tag})
    #             # yield scrapy.Request(url=url, callback=self.comment, meta={'id': id})
    #
    #     except Exception as e:
    #         print('4' * 20)
    #         print(e)


