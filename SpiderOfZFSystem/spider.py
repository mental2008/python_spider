import requests
import os
from urllib import parse
from bs4 import BeautifulSoup
import bs4

def getResponse(url, hd):
    try:
        response = requests.get(url, timeout = 30, headers = hd)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response
    except:
        return "Error"

def downloadCheckCode(url):
    url = url + "CheckCode.aspx"
    hd = {'user-agent': 'Mozilla/5.0'}
    response = getResponse(url, hd)
    if response == "Error":
        print("验证码下载错误...")
        return "Error"
    else:
        print("正在下载验证码...")
    with open("CheckCode.png", 'wb') as f:
        f.write(response.content)
    print("验证码已下载")
    os.startfile("CheckCode.png")

def getViewState(soup):
    return soup.find('input', attrs = {'name': '__VIEWSTATE'})['value']


def login(url):
    url = url + "default2.aspx"
    hd = {'user-agent': 'Mozilla/5.0'}
    response = getResponse(url, hd)
    if response == "Error":
        print("登陆失败...")
    else:
        html = response.text
    soup = BeautifulSoup(html, "html.parser")
    __viewstate = getViewState(soup)
    data = {'__VIEWSTATE': '',
            'txtUserName': '',
            'TextBox2': '',
            'txtSecretCode': '',
            'RadioButtonList1': '\xd1\xa7\xc9\xfa',
            'Button1': '',
            'lbLanguage:': '',
            'hidPdrs': '',
            'hidsc': ''}
    data['__VIEWSTATE'] = __viewstate
    studentID = input("请输入学号: ")
    data['TextBox2'] = input("请输入密码: ")
    data['txtSecretCode'] = input("请输入图片中的验证码: ")
    data['txtUserName'] = studentID
    print("登陆中...")
    s = requests.session()
    s.post(url, data = data)
    try:
        r = s.get("http://xsweb.scuteo.com/(klbbxierheaus4ftnggitnuz)/xs_main.aspx?xh=" + studentID, timeout = 30, headers = hd)
        newsoup = BeautifulSoup(r.text, 'html.parser')
        name = newsoup.find('span', attrs = {'id': 'xhxm'}).text[:-2]
        print("登陆成功!欢迎你,{0}同学".format(name))
    except:
        print("登陆失败...")
        return "Error"
    
    return s, studentID, name

def queryScore(s, studentID, name):
    url = "http://xsweb.scuteo.com/(klbbxierheaus4ftnggitnuz)/xscjcx.aspx?xh=" + studentID + "&xm=" + parse.quote(name.encode('gb2312')) + "&gnmkdm=N121605"
    hd = {'Referer': url, 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
          'Upgrade-Insecure-Requests': '1', 'Host': 'xsweb.scuteo.com',
          'Origin': 'http://xsweb.scuteo.com', 'Content-Type': 'application/x-www-form-urlencoded',
          'Connection': 'keep-alive', 'Cache-Control': 'max-age=0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.8'}
    response = s.get(url, headers = hd)
    soup = BeautifulSoup(response.text, 'html.parser')
    print("正在查询成绩...")
    __viewstate = getViewState(soup)
    data = {'__EVENTTARGET': '', '__EVENTARGUMENT': '',
            '__VIEWSTATE': __viewstate, 'hidLanguage': '',
            'ddlXN': '', 'ddlXQ': '','ddl_kcxz': '',
            'btn_zcj': '\xc0\xfa\xc4\xea\xb3\xc9\xbc\xa8'}
    r = s.post(url, headers = hd, data = data)
    return r.text

def printFormat(text, width):
    def is_chinese(char):
        if char >= u'\u4e00' and char <= u'\u9fa5':
            return True
        else:
            if  char == 'Ⅰ' or char == '（' or char == '）' or char == 'Ⅲ' or char == 'Ⅱ':
                return True
            else :
                return False
    stext = str(text)
    cn_count = 0
    for u in stext:
        if is_chinese(u):
            cn_count = cn_count + 1
    return stext + " " * (width - cn_count - len(stext))

def printScore(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', attrs = {'class': 'datelist'})
    #tpt = '{0:{9}<10}{1:{9}<3}{2:{9}<20}{3:{9}<7}{4:{9}<5}{5:{9}<5}{6:{9}<5}{7:{9}<15}{8:{9}<3}'
    mp = [2, 3, 5, 6, 8, 9, 10, 14, 17]
    num = 1
    for tr in table.contents:
        count = 1
        ulist = []
        if isinstance(tr, bs4.element.Tag):
            for td in tr.contents:
                if count in mp:
                    ulist.append(td.string)
                count = count + 1
            #print(tpt.format(ulist[0], ulist[1], ulist[2], ulist[3], ulist[4], ulist[5], ulist[6], ulist[7], ulist[8], chr(12288)))
            if not num == 1:
                ulist[5] = ulist[5][3:]
            print(printFormat(ulist[0], 10) + printFormat(ulist[1], 5) +
                  printFormat(ulist[2], 30) + printFormat(ulist[3], 10) +
                  printFormat(ulist[4], 10) + printFormat(ulist[5], 10) +
                  printFormat(ulist[6], 10) + printFormat(ulist[7], 25) +
                  printFormat(ulist[8], 5))
            num = num + 1

if __name__ == "__main__":
    url = "http://xsweb.scuteo.com/(klbbxierheaus4ftnggitnuz)/" #original url
    if not downloadCheckCode(url) == "Error":
        loginData = login(url)
        if not loginData == "Error":
            s = loginData[0]
            studentID = loginData[1]
            name = loginData[2]
            html = queryScore(s, studentID, name)
            printScore(html)
    
