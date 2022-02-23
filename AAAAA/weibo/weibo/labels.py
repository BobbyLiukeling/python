# -*- encoding: utf-8 -*-
# @author : bobby
# @time : 2020/2/22 20:17

'''
将URL 转换为 最后的数字
'''
import pdb
import sys,os
import numpy
# pwd = os.getcwd()
# s = os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")

file = open('../try.txt')

temp = file.readlines()
text = temp[0].split('$')
url = open('spiders/urls.py','w')

url.write('temp = [')

for i in text:
    i = i.split('/')[-1]
    if len(i)==16:
        url.write("'"+i +"'"+ ',\n')
url.write(']')
file.close()
url.close()