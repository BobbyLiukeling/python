# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/5/18 11:11
# 爬虫相关字段

from peewee import *

db = MySQLDatabase('csdn_scrapy',host = '127.0.0.1',port =3306,user ='root',password ='867425') #连接数据库


class BaseModel(Model): #连接数据库的模块，后面只需要继承
    class Meta:
        database = db


class Topic(BaseModel):
    title = CharField()
    content = TextField()
    id = IntegerField(primary_key=True) #话题ID,设置为主键
    author = CharField()
    create_time = DateTimeField()
    answer_nums = IntegerField(default=0)
    click_nums = IntegerField(default=0)
    parised_nums = IntegerField(default=0) #点赞
    jtl = FloatField(default=0.0) #结帖率
    score = IntegerField(default=0) #赏分
    status = CharField() #状态


class Answer(BaseModel):
    topic_id = IntegerField()
    author = CharField()
    content = TextField(default="")
    create_time = DateTimeField()
    parsed_nums = IntegerField(default=0)


class Author(BaseModel):
    name = CharField()
    id = IntegerField(primary_key=True)
    click_nums = IntegerField(default=0)
    original_nums = IntegerField(default=0) #原创文章数
    forward_nums = IntegerField(default=0) #转发数
    rate = IntegerField(default=-1) #排名数
    answer_nums = IntegerField(default=0) #被评论数
    parised_nums = IntegerField(default=0) #点赞数
    desc = TextField(null=True)
    industry = CharField(null=True) #就职企业
    location = CharField(null=True) #地址
    follower_nums = IntegerField(default=0) #粉丝数
    followeing_nums = IntegerField(default=0) #关注数


if __name__ == '__main__':
    db.create_tables([Topic,Answer,Author]) #创建表


