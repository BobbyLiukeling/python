# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/5/17 10:44

import requests

red = requests.get('https://www.baidu.com')
# print(red.text)
print(red.headers)