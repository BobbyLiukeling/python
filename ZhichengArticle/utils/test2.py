# import time
# # from http import cookiejar
# # import json
# # import requests
# # from bs4 import BeautifulSoup
# # # url = 'https://www.zhihu.com/people/run-tu-42/activities'
# #
# # headers = {
# #     "Host": "www.zhihu.com",
# #     "Referer": "https://www.zhihu.com/",
# #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
# # }
# #
# #
# #
# #
# # # 使用登录cookie信息
# # session = requests.session()
# # session.cookies = cookiejar.LWPCookieJar(filename='cookies.txt')
# # try:
# #     print(session.cookies)
# #     session.cookies.load(ignore_discard=True)
# #
# # except:
# #     print("还没有cookie信息")
# #
# #
# # def get_xsrf():
# #     response = session.get("https://www.zhihu.com", headers=headers, verify=False)
# #     soup = BeautifulSoup(response.content, "html.parser")
# #     xsrf = soup.find('input', attrs={"name": "_xsrf"}).get("value")
# #     return xsrf
# #
# #
# # def get_captcha():
# #     """
# #     把验证码图片保存到当前目录，手动识别验证码
# #     """
# #     t = str(int(time.time() * 1000))#验证码是按时间戳命名
# #     captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login&lang=cn"
# #     print(captcha_url)
# #     r = session.get(captcha_url, headers=headers)
# #     with open('captcha.gif', 'wb') as f:
# #         f.write(r.content)
# #         f.close()
# #
# #     # 自动打开刚获取的验证码
# #     from PIL import Image
# #     try:
# #         img = Image.open('captcha.gif')
# #         img.show()
# #         img.close()
# #     except:
# #         pass
# #
# #     captcha = {
# #         'img_size': [200, 44],
# #         'input_points': [],
# #     }
# #     points = [[22.796875, 22], [42.796875, 22], [63.796875, 21], [84.796875, 20], [107.796875, 20],
# #               [129.796875, 22], [150.796875, 22]]
# #     seq = input('请输入倒立字的位置\n>')
# #     for i in seq:
# #         captcha['input_points'].append(points[int(i) - 1])
# #     return json.dumps(captcha)
# #
# #
# # def login(email, password):
# #     login_url = 'https://www.zhihu.com/login/email'
# #     data = {
# #         'email': email,
# #         'password': password,
# #         '_xsrf': get_xsrf(),
# #         "captcha": get_captcha(),
# #         'captcha_type': 'cn',}
# #     print(session.cookies)
# #     response = session.post(login_url, data=data, headers=headers)
# #     login_code = response.json()
# #     print(login_code['msg'])
# #     print(session.cookies)
# #     r = session.get("https://www.zhihu.com/settings/profile", headers=headers)
# #     print(r.status_code)
# #     print(r.text)
# #     with open("xx.html", "wb") as f:
# #         f.write(r.content)
# #
# #
# # if __name__ == '__main__':
# #     email = "18328020353"
# #     password = "520lkl"
# #     login(email, password)
def la(name):
    print(name)
    return name