from selenium import webdriver
from requests import Session
from time import sleep
from bs4 import BeautifulSoup
import requests
req =requests.session()
web = webdriver.Chrome("E:/software/python3.6/chromedriver.exe")
'''
参数传递法
chromePath = r'D:\Python Program\chromedriver.exe'
wd = webdriver.Chrome(executable_path= chromePath)
'''
url = "https://www.zhihu.com/signin"
web.get(url)
web.find_element_by_xpath(".//*[@class='SignFlow-account']/div[2]/div[1]/input").send_keys("18328020353")
web.find_element_by_xpath(".//*[@class='Input-wrapper']/input").send_keys("520lkl")
web.find_element_by_xpath(".//*[@class='Login-content']/form/button").submit() #提交表单
cookies = web.get_cookies()
for cookie in cookies:
    req.cookies.set(cookie['name'], cookie['value'])
req.headers.clear()
with open("zhihu.html","wb") as f:
    soup = BeautifulSoup(web.page_source,"html.parser")
    f.write(soup.encode("utf-8"))