# -*- coding: utf-8 -*-
# @Time : 2021/7/2 0002 10:13
# @Author : Bobby_Liukeling
# @File : scrapy_autophagy.py



import time
from selenium import webdriver
import requests
import json
import pdb
from lxml import etree
from scrapy.selector import Selector
import pandas as pd


Acc_path = "Acc_data1.xlsx"
start = 0
end = 100



error_path = "error_data.txt"
miss_path = "miss_data.txt"



class handle_data():

    def __init__(self):
        self.df = pd.read_excel("autophagy-GO-treat1.xls")

    def get_AccId(self):
        AccId = list(self.df[self.df.columns[0]]) #取出所有的acc(id),等待查询
        return AccId

class web_get():

    def __init__(self):
        self.web = webdriver.Chrome('E:/software/python3.6/chromedriver.exe')

    def query_AccId(self,AccId):
        str1 = 'https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22parameters%22%3A%7B%22value%22%3A%22'
        str2 = '%22%7D%2C%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22node_id%22%3A0%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22pager%22%3A%7B%22start%22%3A0%2C%22rows%22%3A25%7D%2C%22scoring_strategy%22%3A%22combined%22%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%7D%2C%22request_info%22%3A%7B%22src%22%3A%22ui%22%2C%22query_id%22%3A%229864d5366f9c5ea73da2af15dd7152e5%22%7D%7D'
        Acc_data = pd.DataFrame(columns=['AccId','pro_type'])
        error_list = []
        miss_list = []

        count = 0

        for id in AccId:
            try:
                print("id:",id)
                path = str1+id+str2
                self.web.get(path)
                time.sleep(5)
                self.web.refresh()
                time.sleep(10)
                totle = self.web.find_element_by_xpath('//div[contains(text(),"Displaying")]/span').text.split(' ')[0]  # 取出当前数据总数
                Acc_list = []
                contents = self.web.find_elements_by_xpath(
                    '//div[contains(@class,"row") and contains(@class,"results-item-row")]')  # 一页的量
                for content in contents:
                    Acc_list.append(content.find_element_by_xpath('.//table').find_element_by_xpath('.//a').text)

                #当前数据分页数
                page_number = self.web.find_element_by_xpath('//div[contains(text(),"Displaying")]/following-sibling::div').text.split(" ")[-1] #取出最大页码
                page_number = int(page_number)

                if page_number>1:
                    while(page_number):
                        page_number = page_number-1
                        #翻到下一页,点击下一页
                        self.web.find_element_by_xpath('//div[contains(text(),"Displaying")]/following-sibling::div/following-sibling::div/div[2]').click()
                        time.sleep(15)#这里不可以再刷新
                        #获取内容
                        contents = self.web.find_elements_by_xpath(
                            '//div[contains(@class,"row") and contains(@class,"results-item-row")]')  # 一页的量
                        for content in contents:
                            Acc_list.append(content.find_element_by_xpath('.//table').find_element_by_xpath('.//a').text)
                # pdb.set_trace()

                Acc_list = set(Acc_list)
                if len(Acc_list) != int(totle): #数据没爬完,要set一下，可能数据会有重复提交
                    print("数据有缺失")
                    miss_list.append(id)

                Acc_list = ",".join(Acc_list)
                df = pd.DataFrame([[id, Acc_list]],columns=['AccId','pro_type'])
                Acc_data = Acc_data.append(df,ignore_index=True)
                Acc_data.to_excel(Acc_path) #每次运行都保存一下

            except Exception as e:
                print(e)
                error_list.append(id) #将出错的id保存下来，

            print("count:",count)
            count = count+1

        #记录错误日志
        with open(error_path, "a") as file:  #
            file.write(",".join(error_list))
        with open(miss_path, "a") as file:  #
            file.write(",".join(miss_list))







if __name__ == "__main__":


     handle = handle_data()
     AccId = handle.get_AccId()


     web = web_get()
     wrong_data = ['Q9Y484', 'Q8N682', 'Q96S99', 'A8K0Z3', 'H7C152', 'Q96BY7', 'B3EWF7', 'Q96DM3', 'P54257', 'Q6UXG2']

     # pdb.set_trace()

     web.query_AccId(AccId[start:end])
     #  temp = ['P0CG48',]
     # web.query_AccId(temp)



