# -*- coding: utf-8 -*-
# @Time : 2021/7/7 0007 9:51
# @Author : Bobby_Liukeling
# @File : Scrapy.py




import time
from selenium import webdriver
import requests
import json
import pdb
from lxml import etree
from scrapy.selector import Selector
import pandas as pd



Acc_path = "Acc_data_suppliment.xlsx"
start = 400
end = 400


error_path = "error_data.txt"
miss_path = "miss_data.txt"



class handle_data():

    def __init__(self):
        self.df = pd.read_excel("../autophagy-GO-treat1.xls")

    def get_AccId(self):
        AccId = list(self.df[self.df.columns[0]]) #取出所有的acc(id),等待查询
        return AccId

class web_get():

    def __init__(self):
        self.web = webdriver.Chrome('E:/software/python3.6/chromedriver.exe')

    def query_AccId(self,AccId):
        str1 = 'https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22parameters%22%3A%7B%22value%22%3A%22'
        str2 = '%22%7D%2C%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%2C%22node_id%22%3A0%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22pager%22%3A%7B%22start%22%3A0%2C%22rows%22%3A25%7D%2C%22scoring_strategy%22%3A%22combined%22%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%7D%2C%22request_info%22%3A%7B%22src%22%3A%22ui%22%2C%22query_id%22%3A%229864d5366f9c5ea73da2af15dd7152e5%22%7D%7D'
        Acc_data = pd.DataFrame(columns=['AccId','pro_type']) #
        error_list = []
        miss_list = []

        count = 0
        for id in AccId:

            print("count:", count)
            print("id:",id)
            path = str1+id+str2
            self.web.get(path)
            time.sleep(5)
            # self.web.refresh()
            # time.sleep(5)
            try:
                #如果可以取出totle则有数据否则没数据
                totle = self.web.find_element_by_xpath('//div[contains(text(),"Displaying")]/span').text.split(' ')[0]  # 取出当前数据总数
                totle = int(totle)
                self.web.find_element_by_xpath('//div[contains(text(),"Download Files")]').click()
                time.sleep(5)
                Acc_temp = self.web.find_elements_by_xpath('//textarea[@id = "downloadsIdList"]')[0].text #数据类型是str
                Acc_num = len(Acc_temp.split(',')) #当前数据个数
                if Acc_num != totle: #数据量有误
                    # pdb.set_trace()
                    print("data is error")
                    error_list.append(id)
                    count = count + 1
                    continue
                print("data_num:",Acc_num)

            except Exception as e:
                print("no result")
                miss_list.append(id)
                count = count + 1
                continue

            Acc_data = Acc_data.append([{'AccId':id,'pro_type':Acc_temp}],ignore_index=True)
            Acc_data.to_excel(Acc_path) #每次运行都保存一下\
            count = count + 1


        # #记录错误日志
        # with open(error_path, "a") as file:  #
        #     file.write(",".join(error_list))
        # with open(miss_path, "a") as file:  #
        #     file.write(",".join(miss_list))







if __name__ == "__main__":


     handle = handle_data()
     AccId = handle.get_AccId()


     web = web_get()
     AccId = ['A8K0Z3', 'Q96DM3', 'H7C152', 'Q96BY7']
     web.query_AccId(AccId)




