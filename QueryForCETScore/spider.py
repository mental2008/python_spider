from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def inputData():
    zkzh = input("准考证号: ")
    name = input("姓名: ")
    return zkzh, name

url = "http://www.chsi.com.cn/cet/"
th = ["姓名:", "学校:", "考试级别:", "准考证号:", "总分:", "听力:", "阅读:", "翻译:"]
td = []

def printResult(driver):
    for x in driver.find_elements_by_tag_name("td"):
        if not x.text == "--" and not x.text == "":
            td.append(x.text)
    length = len(td)
    if length == 0:
        print("错误的准考证号或姓名!")
        return
    print("\n\n------您的考试数据如下------")
    for i in range(length):
        print(th[i] + td[i])

if __name__ == "__main__":
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(10)
    driver.get(url)
    elem1 = driver.find_element_by_name("zkzh")
    elem1.clear()
    elem2 = driver.find_element_by_name("xm")
    elem2.clear()
    zkzh, name = inputData()
    elem1.send_keys(zkzh)
    elem2.send_keys(name)
    button = driver.find_element_by_id("submitCET")
    button.click()
    printResult(driver)
    #driver.save_screenshot('screenshot.png')
    driver.close()
