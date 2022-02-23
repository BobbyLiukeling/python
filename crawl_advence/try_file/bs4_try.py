# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/5/17 18:05

from bs4 import BeautifulSoup       #beautifulsoup4库使用时是简写的bs4
import requests
r = requests.get('http://python123.io/ws/demo.html')
demo = r.text
soup = BeautifulSoup(demo,'html.parser')    #解析器：html.parser
print(soup.prettify())          #打印解析好的内容

