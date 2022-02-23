# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.loader.processors import MapCompose


def data_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date



class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    label = scrapy.Field()

    user = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    fav_nums = scrapy.Field()
    add_time = scrapy.Field(
        input_processor=MapCompose(data_convert),
    )
    tag = scrapy.Field()

class CommentItem(scrapy.Item):  # 专栏评论 / 回答评论
    article_id = scrapy.Field()
    comment_user = scrapy.Field()
    comment_content = scrapy.Field()
    fav_nums = scrapy.Field()

class comment_replayItem(scrapy.Item):
    comment_id = scrapy.Field()
    right_user = scrapy.Field()
    left_user = scrapy.Field()
    replay_content = scrapy.Field()
    fav_nums = scrapy.Field()




class QuestionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user = scrapy.Field()
    Q_title = scrapy.Field()
    Q_content = scrapy.Field()
    label = scrapy.Field()
    url = scrapy.Field()
    focus_nums = scrapy.Field()
    answer_nums = scrapy.Field()
    view_nums = scrapy.Field()
    tag = scrapy.Field()

class AnswerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Q_user = scrapy.Field()
    Q_title = scrapy.Field()
    question_id = scrapy.Field()
    user = scrapy.Field()
    comment_nums = scrapy.Field()
    content = scrapy.Field()
    fav_nums = scrapy.Field()
    add_time = scrapy.Field(
        input_processor=MapCompose(data_convert),
    )
    tag = scrapy.Field()
