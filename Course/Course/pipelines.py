# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter
class CoursePipeline(object):
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('CaiNiao_File.xlsx')  # 创建一个名为‘Demo1.xlsx’的工作表
        self.worksheet = self.workbook.add_worksheet()  # 创建一个工作表对象
        self.worksheet.write('A1', '序号')
        self.worksheet.write('B1', '标题')
        self.worksheet.write('C1', '链接')
        self.worksheet.write('D1', '积分')
        self.cols = 1

    def process_item(self, item, spider):
        self.worksheet.write(self.cols, 0, self.cols)#第一行是横，第二行是竖
        #self.worksheet.write(self.cols, 1, item["type"])
        self.worksheet.write(self.cols, 1, item["title"])
        self.worksheet.write(self.cols, 2, item["href"])
        self.worksheet.write(self.cols, 3, item["score"])
        self.cols = self.cols+1
        return item

    def closed(self):
        self.workbook.close()
