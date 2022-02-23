from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
req =requests.session()

wd = webdriver.Chrome('E:/software/python3.6/chromedriver.exe')
#打开知乎首页
wd.get('https://www.zhihu.com/')
#进入登陆页面
wd.find_element_by_xpath(".//*[@class='SignContainer-switch']/span").click()
#点击社交网络账号登陆
wd.find_element_by_xpath(".//*[@class='Login-socialLogin']/button").click()#点击微博登陆
wd.find_element_by_xpath(".//*[@class='Login-socialButtonGroup']/button[3]").click()#点击微博登陆
time.sleep(10)
wd.refresh()
with open("zhihu.html","wb") as f:
    soup = BeautifulSoup(wd.page_source,"html.parser")
    f.write(soup.encode("utf-8"))
# import time
# time.sleep(2)
# web = webdriver.Chrome('E:/software/python3.6/chromedriver.exe')
# a = 'https://graph.qq.com/oauth2.0/show?which=Login&display=pc&scope=get_user_info%2Cget_info%2Cadd_t%2Cadd_pic_t%2Cget_other_info%2Cget_fanslist%2Cget_idollist%2Cadd_idol%2Cadd_share&state=6b7476517232474571716770496352623033466b4767364c7131463638425048&redirect_uri=https%3A%2F%2Fwww.zhihu.com%2Foauth%2Fcallback%2Fqqconn&response_type=code&client_id=100490701'
# web.get(a)
# # web.find_element_by_xpath(".//*[@class='face']").click()
# print(web.page_source)



#输入微博账号，将value 里面的值换成你的微博账号。
# try:
#     wd.execute_script("document.getElementById('userId').value='我的微博账号';")
# except:
#     pass
#
# #输入微博密码, 将value 里面的值换成你的微博密码。
# try:
#     wd.execute_script("document.getElementById('passwd').value='我的微博密码)';")
# except:
#     pass
#
# #点击登陆按钮
# wd.find_element_by_xpath('//*[@id="outer"]/div/div[2]/form/div/div[2]/div/p/a[1]').click()
# #点击允许访问按钮
# wd.find_element_by_id('//*[@id="outer"]/div/div[2]/div/div[2]/div[2]/p/a[1]').click()

# time.sleep(2)

# cookies = wd.get_cookies()
# for cookie in cookies:
#     req.cookies.set(cookie['name'], cookie['value'])
# req.headers.clear()
# with open("zhihu.html","wb") as f:
#     soup = BeautifulSoup(wd.page_source,"html.parser")
#     f.write(soup.encode("utf-8"))


