import requests
from bs4 import *
import bs4
import re

def getHTMLtext(url):
    try:
        r=requests.get(url,timeout=10)
        r.raise_for_status()
        '''这一条命令的意思是，测试其上面的网络爬虫代码能否返回正确值“200”
        （只有返回200时，才说明服务器访问成功，返回其他数值都说明访问失败）。
        如果能的话，无反应；如果不能，抛出requests失败。'''
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return "产生异常"

def fillUnivList(ulist,html):
    soup=BeautifulSoup(html,"html.parser")
    for tr in soup.find("tbody").contents:
        
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            a=[tds[1].text, tds[3].text]
            ulist.append(a)   
           

def printUnivList(uList,num):#num需要打印的前num个
    tplt="{0:^10}\t{1:{3}^15}\t{2:^10}"
    print(tplt.format("排名","大学名称","分数",chr(12288)))
    for i in range(num):
        u=uList[i]
        print(tplt.format(i+1,u[0],u[1],chr(12288)))
        

def main():
    unifo=[]
    url="http://www.zuihaodaxue.cn/zuihaodaxuepaiming2017.html"
    num=10
    html=getHTMLtext(url)
    fillUnivList(unifo,html)
    printUnivList(unifo,num)
    print("lalalla")
main()



