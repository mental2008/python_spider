# -*- coding: utf-8 -*-
import requests
import bs4
from bs4 import BeautifulSoup
import time

def getHtmlText(url):
    try:
        hd = {'user-agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout = 30, headers = hd)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        return ""

def dealData(ulist, html):
    soup = BeautifulSoup(html, 'html.parser')
    for university in soup.find('tbody').children:
        if isinstance(university, bs4.element.Tag):
            temp = university('td')
            #print(temp)
            ulist.append([temp[0].string, temp[1].string, temp[2].string, temp[3].string])

def printResult(ulist):
    tplt = "{0:{4}<8}\t{1:{4}<10}\t{2:{4}<8}\t{3:<10}"
    print(tplt.format("排名", "学校名称", "省市", "总分", chr(12288)))
    for i in range(len(ulist)):
    #for i in range(50):
        element = ulist[i]
        print(tplt.format(i + 1, element[1], element[2], element[3], chr(12288)))

if __name__ == "__main__":
    start = time.time()
    url = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming2017.html"
    ulist = []
    html = getHtmlText(url)
    dealData(ulist, html)
    printResult(ulist)
    end = time.time()
    print('\n' + "本次查询时间:", end - start, '秒')