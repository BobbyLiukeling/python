# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class ZhichengarticlePipeline(object):
#     def process_item(self, item, spider):
#         return item


from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors
import pdb
from .items import ZhichengarticleItem,QuestionItem,AnswerItem,CommentItem
# if isinstance(item, JsTotalItem):
class ZhichengarticlePipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host="127.0.0.1",
            port=3306,
            user="root",
            passwd="867425",
            db="zhichengariticle",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)
        print('@'*30)

    def do_insert(self, cursor, item):
        #执行具体的插入
        #根据不同的item 构建不同的sql语句并插入到mysql中
        if isinstance(item, ZhichengarticleItem):
            # pdb.set_trace()
            try:
                sql = "insert into buycar(user,title,content,url,fav_nums,add_time,tag) values(%s,%s,%s,%s,%s,%s,%s)"
                params = (item["user"], item["title"],item['content'],item['url'],int(item['fav_nums']),item['add_time'],item['tag'])
                cursor.execute(sql, params)
            except Exception as e:
                pass


        elif isinstance(item,QuestionItem):
            try:
                sql = "insert into question(user,Q_title,Q_content,url,label,focus_nums,view_nums,answer_nums,tag)" \
                      " values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                params = (
                item["user"], item["Q_title"], item['Q_content'], item['url'],item['label'],
                item['focus_nums'], item['view_nums'],item['answer_nums'],item['tag']
                )
                cursor.execute(sql, params)
            except Exception as e:
                pass

        elif isinstance(item,AnswerItem):
            try:
                sql = "insert into answer(question_id,A_user,comment_nums,content,fav_nums,add_time,tag)" \
                      " values(%s,%s,%s,%s,%s,%s,%s)"
                params = (
                item['question_id'],item['user'],item['comment_nums'],item['content'],
                    item['fav_nums'],item['add_time'],item['tag']
                )
                cursor.execute(sql, params)
            except Exception as e:
                pass
                # print('anser  ' * 20)
                # print(item['question_id'],item['user'],item['comment_nums'],
                #     item['fav_nums'],item['add_time'],item['tag'])
                # print(e)

        elif isinstance(item, CommentItem):
            try:
                sql = "insert into comment(article_id ,comment_user,comment_content,fav_nums)" \
                      " values(%s,%s,%s,%s)"
                params = (
                    item['aricle_id'], item['comment_user'], item['comment_content'], item['fav_nums']
                )
                cursor.execute(sql, params)
            except Exception as e:
                print('comment   ' * 20)
                print(item['aricle_id'], item['comment_user'], item['comment_content'], item['fav_nums'])
                print(e)
                pass



