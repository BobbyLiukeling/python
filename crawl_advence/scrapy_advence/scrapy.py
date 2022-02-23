# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/5/18 17:32
# 对csdn论坛内容进行爬取
# 静态网页的抓取
# 抓取内容：帖子，回答，用户信息
import re
import pdb

import requests


from scrapy_advence import models

def get_json():
    url = 'https://bbs.csdn.net/dynamic_js/left_menu.js?csdn'
    left_menu_text = requests.get(url).text
    pdb.set_trace()


if __name__ == '__main__':
    get_json()
