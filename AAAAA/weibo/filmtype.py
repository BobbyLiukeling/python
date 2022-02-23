# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/3/3 19:24
import os,sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "film_type"])