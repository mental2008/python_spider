import requests
import bs4
from bs4 import BeautifulSoup

def getHtmlText(url):
    try:
        hd = {'user-agent': 'Mozilla/5.0'}
        response = requests.get(url, timeout = 30, headers = hd)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except:
        print("")

def printResult(html):
    soup = BeautifulSoup(html, 'html.parser')
    info = soup.find('p', 'WhwtdWrap bor-b1s col-gray03')
    if info == None:
        print("Ip address/Domain name is incorrect")
        return
    cnt = 0
    ulist = ['Ip address/Domain name:', 'Ip address which is queried:', 'Digital address:', 'IP physical location:']
    for i in info.children:
        if isinstance(i, bs4.element.Tag):
            temp = '{0:<40}{1:<100}'
            print(temp.format(ulist[cnt], i.string))
            cnt = cnt + 1



if __name__ == "__main__":
    url = "http://ip.chinaz.com/"
    ip = input("Please input the ip address or domain name which you want to query: ")
    url += ip
    html = getHtmlText(url)
    printResult(html)
