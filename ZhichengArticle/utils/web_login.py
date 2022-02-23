from selenium import webdriver
from requests import Session
from time import sleep
from bs4 import BeautifulSoup
import requests
import time
s = requests.Session()

import pdb
req =requests.session()
web = webdriver.Chrome("E:/software/python3.6/chromedriver.exe")
'''
参数传递法
chromePath = r'D:\Python Program\chromedriver.exe'
wd = webdriver.Chrome(executable_path= chromePath)
'''
url = "https://www.zhihu.com/people/run-tu-42/activities"
web.get(url)
s.headers.clear()#清除requests头部中的Python机器人信息，否则登录失败
time.sleep(3)
web.find_element_by_xpath(".//*[@class='AppHeader-profile']/div/button").click()

web.find_element_by_xpath(".//*[@class='SignFlow-account']/div[2]/div[1]/input").send_keys("18328020353")
web.find_element_by_xpath(".//*[@class='SignFlowInput']/div/input").send_keys("520lkl")
web.find_element_by_xpath(".//*[@class='SignFlow']/button").click() #提交表单



# web.find_element_by_xpath(".//*[@class='Login-content']/form/button").click() #提交表单
# web.find_element_by_xpath(".//*[@class='Login-content']/form/button").click() #提交表单
# web.find_element_by_xpath(".//*[@class='Login-content']/form/button").click() #提交表单
# web.find_element_by_xpath(".//*[@class='Login-content']/form/button").submit()
# web.find_element_by_xpath(".//*[@class='Login-content']/form/button").submit()
# pdb.set_trace()
# a = web.find_element_by_class_name('Captcha-englishImg')
# a = web.find_element_by_class_name('Captcha-chineseImg')

# xpath(".//*[@class='Login-content']/form/button").click() #提交表单
# cookies = web.get_cookies()
# for cookie in cookies:
#     req.cookies.set(cookie['name'], cookie['value'])
# req.headers.clear()
# with open("zhihu.html","wb") as f:
#     soup = BeautifulSoup(web.page_source,"html.parser")
#     f.write(soup.encode("utf-8"))