import os
import sys
import time
import random
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
'''
模拟登陆需要输入验证码 我不会破解 哭哭哭哭

'''


def seleLogin(init=None):
    while True:
        account = input("输入您的账户：")
        password = input("输入您的密码：")
        str = input(
                    "警告！\n"
                    "模拟登陆行为是通过selenium webdriver来进行的\n"
                    "webdriver主流版本下载地址\n"
                    "Firefox浏览器驱动：https://github.com/mozilla/geckodriver/releases\n"
                    "Chrome浏览器驱动：https://npm.taobao.org/mirrors/chromedriver , "
                    "https://sites.google.com/a/chromium.org/chromedriver/home\n"
                    "IE浏览器驱动：http://selenium-release.storage.googleapis.com/index.html\n"
                    "opera浏览器驱动：https://github.com/operasoftware/operachromiumdriver/releases\n"
                    "Edge浏览器驱动：https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver\n"
                    "PhantomJS浏览器驱动：https://phantomjs.org/\n"
                    "具体浏览器版本查看方式请自行百度\n"
                    "请将下载好的webdriver程序的名字变更为webdriver\n"
                    "等待浏览器启动后\n"
                    "重要！！！ 请确保您的浏览器与webdriver版本一一对应 请做好准备后输入浏览器名称\n"
                    "1.Edge(win10自带)\n"
                    "2.Chrome(谷歌)\n"
                    "3.Firefox(火狐)\n"
                    "4.opera(欧朋)\n"
                    "5.IE(不会去测试了)\n"
                    "6.safari(苹果自带) 不需要下载webdriver\n"
                    "不输入或者输入其他则为退出程序"
                    ",请输入：")
        # if str is "y" or str is "Y":
        #     pass
        # else:
        #     sys.exit(0)

        try:
            if str is "1":
                driver = webdriver.Edge('.' + os.sep + 'webdriver' + os.sep + 'webdriver')
            elif str is "2":
                driver = webdriver.Chrome('.' + os.sep + 'webdriver' + os.sep + 'webdriver')
            elif str is "3":
                driver = webdriver.Firefox('.' + os.sep + 'webdriver' + os.sep + 'webdriver')
            elif str is "4":
                driver = webdriver.Opera('.' + os.sep + 'webdriver' + os.sep + 'webdriver')
            elif str is "5":
                driver = webdriver.Ie('.' + os.sep + 'webdriver' + os.sep + 'webdriver')
            elif str is "6":
                driver = webdriver.Safari()
            else:
                sys.exit(0)
            driver.get(
                'https://accounts.pixiv.net/login?return_to=https%3A%2F%2Fwww.pixiv.net%2F&lang=zh&source=pc'
                '&view_type=page')
            break
        except Exception as e:
            print(e)
            print("出现异常")
            flap = input("重新选择 Y 退出程序 N")
            if flap is 'N' or flap is 'n':
                sys.exit(0)
    LoginComponent = driver.find_element_by_id('LoginComponent')
    inputFields = LoginComponent.find_elements_by_class_name('input-field')
    inputFields[0].find_element_by_tag_name('input').send_keys(account)
    inputFields[1].find_element_by_tag_name('input').send_keys(password)
    LoginComponent.find_element_by_tag_name('button').click()
    print("请等待浏览器窗口的加载 程序记录您的Cookie数据 并不会记录账户和密码")
    while True:
        time.sleep(1)
        if driver.current_url == 'https://www.pixiv.net/':
            driver.get('https://www.pixiv.net/ajax/search/tags/miku?lang=zh')
            cookiesStr = ''
            for cookie in driver.get_cookies():
                cookiesStr = cookiesStr + cookie['name'] + '=' + cookie['value'] + '; '
            driver.close()
            break
    return cookiesStr


# 废弃的
def doLogin(init):
    index = 1
    while index < 6:
        print("尝试登陆... 尝试" + str(index) + "次")
        # init.se.cookies = CookieJar()
        try:
            postKeyHtml = init.se.get(init.baseUrl, proxies=init.proxies, headers=init.headers, verify=False).text
            postKeySoup = BeautifulSoup(postKeyHtml, 'lxml')
            init.postKey = postKeySoup.find('input')['value']
            # 上面是去捕获postkey
            data = {
                'pixiv_id': init.pixivId,
                'password': init.password,
                'return_to': init.returnTo,
                'post_key': init.postKey,
                'captcha': '',
                'g_reaptcha_response': '',
                'source': 'pc',
                'ref': 'wwwtop_accounts_indes',
            }
            html = init.se.post(init.loginUrl, data=data, headers=init.headers).text
            print(html)
            print('成功等待下一步操作!!')
            return 0
        except Exception as e:
            index += 1
            print('失败! 原因', end='')
            print(e)
    if index == 6:
        print('抱歉! 五次尝试均失败! 请检查网路! \n按回车键退出程序...')
        input()
        sys.exit()
