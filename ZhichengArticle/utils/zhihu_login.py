import requests
import http.cookiejar
import re
session =requests.session()

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": agent #之间是短线短线！！！！，不是下划线
}

def get_xsrf():
    response = requests.get('https://www.zhihu.com',headers =header)
    xsrf = response.request._cookies._cookies.get('.zhihu.com').get('/').get('_xsrf').value
    return xsrf

def zhihu_login(account,password):
    post_url = 'https://www.zhihu.com/login/phone_num'
    post_data = {
        '_xsrf':get_xsrf(),
        'phone':account,
        'password':password
    }
    response_text = session.post(post_url, data=post_data, headers=header)
    if response_text.status_code == 200:
        print('登陆成功')
    else:
        print('登陆失败')


def index():

    inbox_url = 'https://www.zhihu.com/inbox'
    inbox_response = session.get(inbox_url, headers=header, allow_redirects=False)
    pass


zhihu_login('18328020353','520lkl')
index()