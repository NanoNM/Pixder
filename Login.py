import sys


import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
'''
模拟登陆需要输入验证码 我不会破解 哭哭哭哭

'''


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
