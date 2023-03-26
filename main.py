import shutil, threading
import time
import datetime

import StaticDateInit
from pageDownloader import *
from Login import seleLogin
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

'''
主方法 包含main函数,网络测试,用户数据采集等一些前期准备

请勿将本程序用于商业用途！
请勿将本程序用于商业用途！
请勿将本程序用于商业用途！
出事我不负责 一点责任都没有 网警来找你 那是你的事 这个别找我
我写的代码 我自己都不赚钱 也不是给你用来赚钱的!!! 
'''

BaseData = None
NewTask = True

BaseConfig = None

name = ''
minlike = ''
pagenum = ''
thread = ''
classify = ''
mode = ''
threads = []
safeStop = True
gcdindex = False

# 进程完成指示 用来指示任务全部完成
allDone = False


def initDate():
    global BaseData, NewTask, gcdindex, name, minlike, pagenum, thread, classify, mode, threads, safeStop, allDone
    BaseData = None
    NewTask = True
    gcdindex = False
    name = ''
    minlike = ''
    pagenum = ''
    thread = ''
    classify = ''
    mode = ''
    threads = []
    safeStop = True
    allDone = False


def userInfoGe():
    print("您是第一次使用本程序? 请按照要求输入信息.")
    print("程序将使用您cookie来登录pixiv， 程序在运行时会获取你的cookie，关于cookie你可能想了解 https://baike.baidu.com/item/cookie/1119?fr=aladdin")
    flap = input("同意使用Cookie Y 退出程序 N")
    if flap == 'N' or flap == 'n':
        sys.exit(0)

    # yuchuli
    isNeedProxies = __preConnectTest()
    if not isNeedProxies:
        while True:
            address = input("请输入代理地址 默认127.0.0.1") or '127.0.0.1'
            port = input("请输入代理端口 默认7890") or '7890'
            proxies = {
                "http": "http://" + address + ":" + port,
                "https": "http://" + address + ":" + port,
            }
            #
            # BaseData.proxiesAddr = address
            # BaseData.proxiesPort = port
            if not __connectTest(proxies):
                i = input('连接失败 输入E停止程序, 输入其他重启测试\n')
                if i == 'E' or i == 'e':
                    sys.exit(1001)
            else:
                break
    else:
        proxies = ""
    loginMod = input('你已经知道你的cookie了? y/n') or 'n'
    if loginMod == 'n' or loginMod == 'N':
        print("确定你所使用的浏览器对应webdriver")
        cookie = seleLogin(isNeedProxies)
    else:
        cookie = input("输入您的Cookie\n")
    item = {"projectName": 'settingFile',
            'proxies': proxies,
            'Cookie': cookie,
            'user-agent': '废弃了的'}
    with open('.' + os.sep + 'userInfo.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(item, ensure_ascii=False))
    print("请稍等 ..")


def start(Name):
    folderName = name.replace(':', '').replace('?', '').replace('\\', '').replace('/', '').replace('*', '').replace('|',
                                                                                                                    '').replace(
        '<', '').replace('>', '')
    Index = True
    while Index:
        print("配置文件加载中 . . .")
        if os.path.exists('.' + os.sep + 'userInfo.json'):
            # if os.path.exists('.\\userInfo.json'):
            global BaseData, NewTask
            Index = False
            # with open('.' + os.sep + 'userInfo.json', 'r', encoding='utf-8') as file:
            #     content = file.read()
            #     config = json.loads(content)
            if os.path.exists(parse.unquote(folderName) + '' + os.sep + 'lastTask' + os.sep + 'main.log'):
                x = input('检测到上次的未完成任务 是否继续未完成的任务(Y/N)') or 'y'
                if x == 'Y' or x == 'y':
                    NewTask = False
                    with open(parse.unquote(folderName) + '' + os.sep + 'lastTask' + os.sep + 'main.log', 'r',
                              encoding='utf-8') as file:
                        last = file.read()
                        last = json.loads(last)
                    openThread = last['thread']
                    if int(openThread) < 2:
                        BaseData = StaticDateInit.init(BaseConfig['Cookie'], Name, last['minlike'], last['MaxPage'],
                                                       last['thread'], last['classify'], BaseConfig['proxies'],
                                                       BaseConfig['user-agent'])
                        realStart(last['nowPage'], last['MaxPage'])
                    else:
                        print("检测到需要开启多线程! 正在处理线程问题! 请稍等 ... ")
                        BaseData = StaticDateInit.init(BaseConfig['Cookie'], Name, last['minlike'], last['MaxPage'],
                                                       last['thread'], last['classify'], BaseConfig['proxies'],
                                                       BaseConfig['user-agent'])
                        thrIndex = 0
                        print("线程准备启动了! 请稍等 ... ")
                        while thrIndex < int(openThread):
                            path = 'thread' + str(thrIndex)
                            print(path + '文件读取尝试!')
                            with open(parse.unquote(folderName) + '' + os.sep + 'lastTask' + os.sep + path + '.log',
                                      'r',
                                      encoding='utf-8') as file:
                                last = file.read()
                                threadLast = json.loads(last)
                            if threadLast['threadStart'] == threadLast['threadStop']:
                                print('在之前任务中, 此线程的任务已结束')
                            print('线程: ' + path + '启动成功并开始从: ' + str(threadLast['threadStart']) + ' 到 ' + str(
                                threadLast['threadStop']) + ' 区间继续任务')
                            thr = work(1, "Thread" + str(thrIndex), threadLast['threadStart'], threadLast['threadStop'])
                            thr.start()
                            threads.append(thr)
                            thrIndex += 1
                else:
                    shutil.rmtree(parse.unquote(folderName) + '' + os.sep + 'lastTask')
                    BaseData = StaticDateInit.init(BaseConfig['Cookie'], Name, minlike, pagenum, thread, classify,
                                                   BaseConfig['proxies'],
                                                   BaseConfig['user-agent'])
            else:
                BaseData = StaticDateInit.init(BaseConfig['Cookie'], Name, minlike, pagenum, thread, classify,
                                               BaseConfig['proxies'],
                                               BaseConfig['user-agent'])

            print("欢迎使用本程序!")
        else:
            userInfoGe()


def realStart(Start='null', Stop='null', threadID=None, threadStart=0, threadStop=0, this=None):
    pageDownloader = Downloader()
    if Start == 'null':
        dates = pageDownloader.penterJsonLoadAnalysis(BaseData)
        fileAnalysis = FileAnalysis()
        fileAnalysis.fileAnalysis(dates, BaseData)
        threadInfo = {
            'threadID': threadID,
            'this': [],
            'finish': []
        }
        if this is None:
            for obj in dates:
                threadInfo['this'].append(obj['illustId'])
            for obj in dates:
                Downloader.picDownloader(BaseData, obj)
                threadInfo['this'].remove(obj['illustId'])
                threadInfo['finish'].append(obj['illustId'])
                FileAnalysis.panterUnfinishedTask(BaseData, Start, threadInfo, mode)
        else:
            threadInfo['this'] = this
            for obj in dates:
                for key in this:
                    if key == obj['illustId']:
                        Downloader.picDownloader(BaseData, obj)
                        threadInfo['this'].remove(obj['illustId'])
                        threadInfo['finish'].append(obj['illustId'])
                        FileAnalysis.panterUnfinishedTask(BaseData, Start, threadInfo, mode)
    else:
        while (Start <= int(Stop)) & safeStop:
            for thr in threads:
                if threadID == thr.name:
                    thr.unfinished = int(Stop) - Start
            dates = pageDownloader.jsonLoadAnalysis(BaseData, Start)
            # 细致分析
            fileAnalysis = FileAnalysis()
            fileAnalysis.fileAnalysis(dates, BaseData)
            threadInfo = {
                'threadID': threadID,
                'threadStart': Start,
                'threadStop': threadStop,
            }
            FileAnalysis.UnfinishedTask(BaseData, Start, threadInfo, mode)
            for obj in dates:
                Downloader.picDownloader(BaseData, obj)
            Start += 1


class work(threading.Thread):
    def __init__(self, threadID, name, page, stopPage):
        threading.Thread.__init__(self)
        self.safeStop = True
        self.threadID = threadID
        self.name = name
        self.page = page
        self.unfinished = None
        self.stopPage = stopPage

    def run(self):
        print("开始线程：" + self.name)
        realStart(self.page, self.stopPage, self.name, self.page, self.stopPage, self.safeStop)
        print("退出线程：" + self.name)
        i = 0
        for thr in threads:
            if thr.is_alive():
                i += 1
        if i == 1:
            global allDone
            allDone = True
            print("任务结束 输入r进行新一轮的任务或者使用q来结束程序")


class RankWork(threading.Thread):
    def __init__(self, threadID, page, stopPage, modeType, content, primaryClassify):
        threading.Thread.__init__(self)
        self.primaryClassify = primaryClassify
        self.modeType = modeType
        self.content = content
        self.safeStop = True
        self.threadID = threadID
        self.name = name
        self.page = page
        self.unfinished = None
        self.stopPage = stopPage

    def run(self):
        print("开始线程：" + self.threadID)
        rankStart(self.threadID, self.modeType, self.content, self.primaryClassify, self.page, self.stopPage)
        print("退出线程：" + self.threadID)
        i = 0
        for thr in threads:
            if thr.is_alive():
                i += 1
        if i == 1:
            global allDone
            allDone = True
            print("任务结束 输入r进行新一轮的任务或者使用q来结束程序")


# 未完成的方法 有问题 问题贼大 未完成项目的问题
def panterStart(userID):
    Index = True
    while Index:
        print("配置文件加载中 . . .")
        if os.path.exists('.' + os.sep + 'userInfo.json'):
            global BaseData, NewTask
            Index = False
            # with open('.' + os.sep + 'userInfo.json', 'r', encoding='utf-8') as file:
            #     content = file.read()
            #     config = json.loads(content)
            if os.path.exists(userID + '' + os.sep + 'lastTask' + os.sep + 'main.log'):
                x = input('检测到上次的未完成任务 是否继续未完成的任务(Y/N)') or 'N'
                if x == 'Y' or x == 'y':
                    NewTask = False
                    with open(userID + '' + os.sep + 'lastTask' + os.sep + 'main.log', 'r', encoding='utf-8') as file:
                        last = file.read()
                        last = json.loads(last)
                    openThread = 1
                    if int(openThread) < 2:
                        with open(userID + '' + os.sep + 'lastTask' + os.sep + 'main.log', 'r',
                                  encoding='utf-8') as file:
                            lastT = file.read()
                            lastT = json.loads(lastT)
                        BaseData = StaticDateInit.init(BaseConfig['Cookie'], userID, last['minlike'], last['MaxPage'],
                                                       last['thread'], last['classify'], BaseConfig['proxies'],
                                                       BaseConfig['user-agent'])
                        realStart(last['nowPage'], last['MaxPage'], None, None, None, lastT['this'])
                        return 0
                    else:
                        print("检测到需要开启多线程! 正在处理线程问题! 请稍等 ... ")
                        BaseData = StaticDateInit.init(BaseConfig['Cookie'], userID, last['minlike'], last['MaxPage'],
                                                       last['thread'], last['classify'], BaseConfig['proxies'],
                                                       BaseConfig['user-agent'])
                        thrIndex = 0
                        print("线程准备启动了! 请稍等 ... ")
                        while thrIndex < int(openThread):
                            path = 'thread' + str(thrIndex)
                            print(path + '文件读取尝试!')
                            with open(parse.unquote(name) + '' + os.sep + 'lastTask' + os.sep + path + '.log', 'r',
                                      encoding='utf-8') as file:
                                last = file.read()
                                threadLast = json.loads(last)
                            if threadLast['threadStart'] == threadLast['threadStop']:
                                print('在之前任务中, 此线程的任务已结束')
                            print('线程: ' + path + '启动成功并开始从: ' + str(threadLast['threadStart']) + ' 到 ' + str(
                                threadLast['threadStop']) + ' 区间继续任务')
                            thr = work(1, "Thread" + str(thrIndex), threadLast['threadStart'], threadLast['threadStop'])
                            thr.start()
                            threads.append(thr)
                            thrIndex += 1
                            return 0
                else:
                    shutil.rmtree(userID + '' + os.sep + 'lastTask')
                    BaseData = StaticDateInit.init(BaseConfig['Cookie'], userID, minlike, pagenum, thread, classify,
                                                   BaseConfig['proxies'],
                                                   BaseConfig['user-agent'])
            else:
                BaseData = StaticDateInit.init(BaseConfig['Cookie'], userID, minlike, pagenum, thread, classify,
                                               BaseConfig['proxies'],
                                               BaseConfig['user-agent'])
            print("欢迎使用本程序!")
        else:
            userInfoGe()


def rankStart(thid, modeType, content, primaryClassify, page, stopPage):
    Index = True
    indexTime = ''
    if modeType == '1':
        indexTime = 'today ' + str(datetime.date.today())
    if modeType == '2':
        indexTime = 'week ' + str(datetime.date.today())
    if modeType == '3':
        indexTime = 'month ' + str(datetime.date.month)
    if modeType == '4':
        indexTime = 'rookie ' + str(datetime.date.today())
    if modeType == '5':
        indexTime = 'original ' + str(datetime.date.today())
    if modeType == '6':
        indexTime = 'male ' + str(datetime.date.today())
    if modeType == '7':
        indexTime = 'female ' + str(datetime.date.today())
    if modeType == '8':
        indexTime = 'r18g ' + str(datetime.date.today())

    while Index:
        if os.path.exists('.' + os.sep + 'userInfo.json'):
            global BaseData, NewTask
            Index = False
            BaseData = StaticDateInit.init(BaseConfig['Cookie'], indexTime, -1, 10, 5, 4,
                                           BaseConfig['proxies'],
                                           BaseConfig['user-agent'])
            pageDownloader = Downloader()
            while page < stopPage:
                datas = pageDownloader.rankJsonLoadAnalysis(BaseData, thid, modeType, content, primaryClassify, page)
                # 细致分析
                fileAnalysis = FileAnalysis()
                fileAnalysis.fileAnalysis(datas, BaseData)
                for obj in datas:
                    Downloader.picDownloader(BaseData, obj)
                page = page+1
        else:
            userInfoGe()


def __preConnectTest():
    print("PixSpider by Nanometer")
    print(" PreConnectTest !!! ")
    print("网络连通性检查中", end=' ...  ')
    try:
        html = requests.session().get("https://www.pixiv.net", headers={
            'Referer': 'https://www.pixiv.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56'},
                                      verify=False, timeout=5)
    except Exception as e:
        print("网络检查失败了, 需要网络代理, 原因: ", end='')
        print(e)
        return False
    print("网络连通性检查通过")
    return True


def __connectTest(proxies):
    # while True:

    print("PixSpider by Nanometer")
    print("建议不要自行关闭程序,强行关闭可能会导致图片下载异常, 网络问题也会导致图片下载异常!")
    print("网络连通性检查中", end=' ...  ')
    try:
        html = requests.session().get("https://www.pixiv.net", proxies=proxies, headers={
            'Referer': 'https://www.pixiv.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56'},
                                      verify=False, timeout=5)
        return True
    except Exception as e:
        print("网络检查失败了, 原因: ", end='')
        print(e)
        return False
    print("网络连通性检查通过")
    return True


def __destructor():
    pass


if __name__ == '__main__':
    # 执行初始化操作
    if not os.path.exists('.' + os.sep + 'userInfo.json'):
        userInfoGe()
    with open('.' + os.sep + 'userInfo.json', 'r', encoding='utf-8') as file:
        content = file.read()
        BaseConfig = json.loads(content)
        proxies = None
        if BaseConfig['proxies'] != '' and not __connectTest(proxies):
            proxies = BaseConfig['proxies']
            print('启用配置文件中提供的代理')
            if not __connectTest(proxies):
                print('代理失效 登出')
                sys.exit(1001)
            print('成功')
        else:
            BaseConfig['proxies'] = None
    while True:
        initDate()
        #
        mode = input('模式选择 \n1. 标签遍历模式(默认) 2. 画师模式 3. 热榜模式\n') or '1'
        if mode == '1':
            print('当前模式:标签遍历模式(如果是想继续上次任务只需要输入名字其他全部空白)')
            name = input('输入爬取插图的名字: ')
            minlike = input('最小点赞数量 默认2000: ') or '2000'
            pagenum = input('最大爬取页面 默认100: ') or '100'
            thread = input('启用线程数 注意 线程数一定要被最大爬取页面整除并且不能等于最大页面数!!!! 1除外 默认20: ') or '20'
            classify = input('分级模式选择  '
                             '\n1: 大众级 '
                             '\n2: R18+大众级(默认) '
                             '\n3: R18 '
                             '\n4: R18+R18G+大众级(全部)'
                             '\n5: R18G'
                             '\n请输入：') or '2'
            start(parse.unquote(name))
            # 模拟登陆 需要人机验证 我不会
            # doLogin(BaseData)
            if int(BaseData.thread) > 1 and NewTask:
                print("检测到需要开启多线程! 正在处理线程问题! 请稍等 ... ")
                evPage = int(BaseData.pagenum) // int(BaseData.thread)
                index = 0
                print("线程准备启动了! 请稍等 ... ")
                while index < int(BaseData.thread):
                    thr = work(1, "Thread" + str(index), evPage * index + 1, evPage * (index + 1))
                    thr.start()
                    threads.append(thr)
                    index += 1
            elif NewTask:
                realStart(1, BaseData.pagenum)

        elif mode == '2':
            print('当前模式:画师模式(继续上次任务未完成)')
            userID = input('请输入画师ID') or None
            minlike = input('最小点赞数量 默认5000: ') or '5000'
            # thread = input('输入启用线程线程 默认1: ') or '1'
            thread = '1'
            classify = '1'
            classify = input('分级模式选择 1: 大众级 2: 限制级+大众级(默认) 3: 限制级') or '2'
            ints = panterStart(userID)
            realStart()
        elif mode == '3':
            def r18d(modeType, content, primaryClassify):
                if primaryClassify == '2':
                    primaryClassify = '3'
                evPage = 10 // 5
                index = 0
                while index < 5:
                    thr = RankWork("Thread" + str(index), evPage * index + 1, evPage * (index + 1), modeType,
                                   content, primaryClassify)
                    thr.start()
                    threads.append(thr)
                    index += 1
                pass


            def nomd(modeType, content, primaryClassify):
                evPage = 10 // 5
                index = 0
                while index < 5:
                    thr = RankWork("Thread" + str(index), evPage * index + 1, evPage * (index + 1), modeType,
                                   content, '1')
                    thr.start()
                    threads.append(thr)
                    index += 1
                pass


            print('当前模式 热榜模式(迭代中)')
            modeType = input('模式选择  '
                             '\n1: daily (日榜) '
                             '\n2: weekly (周榜) (默认)'
                             '\n3: monthly (月榜) (无R18)'
                             '\n4: rookie (新人) (无R18)'
                             '\n5: original (原创) (无R18)'
                             '\n6: male (受男性欢迎)'
                             '\n7: female (受女性欢迎)'
                             '\n8: R18G (无动图)'
                             '\n请输入：') or '2'
            content = input('模式选择  '
                            '\n1: 综合 (默认) '
                            '\n2: illust (插画)'
                            '\n3: ugoira (动图) '
                            '\n4: manga (漫画)'
                            '\n5: /novel/ranking (小说) (暂不支持)'
                            '\n请输入：') or '1'

            primaryClassify = input('分级模式选择  '
                                    '\n1: 大众级 '
                                    '\n2: R18+大众级(默认) '
                                    '\n3: R18'
                                    '\n4: R18G 务必选择这个 其他禁止选这个'
                                    '\n请输入：') or '2'

            if primaryClassify == '1':
                nomd(modeType, content, primaryClassify)
            if primaryClassify == '2':
                r18d(modeType, content, primaryClassify)
                nomd(modeType, content, primaryClassify)
            if primaryClassify == '3':
                r18d(modeType, content, primaryClassify)
            if primaryClassify == '4':
                r18d(modeType, content, primaryClassify)

            # print(thdNum)

            pass

        while True:
            time.sleep(0.25)
            cmd = input()
            if cmd == "status":
                for thr in threads:
                    status = 'Stopped'
                    if thr.is_alive():
                        status = 'Alive'
                    else:
                        status = 'Stopped'
                    print('线程' + thr.name + '的状态是: ' + status)
            elif cmd == "stops":
                safeStop = False
                print("请等待所有线程退出后即可安全退出")

            elif cmd == "r":
                break
            elif cmd == "msn":
                unfinishedall = 0
                index = False
                for thr in threads:
                    if thr.unfinished is None:
                        print('还没有计算完成 稍后再试')
                        break
                    unfinishedall = unfinishedall + thr.unfinished
                    index = True
                if index:
                    print(
                        '任务完成了: ' + str(((int(BaseData.pagenum) - unfinishedall) / int(BaseData.pagenum)) * 100) + '%')
            elif cmd == 'about':
                print('===========================\n'
                      'Pixder V0.6.1 by Nanometer\n'
                      '释怀失败！！！！\n'
                      '===========================\n')
            elif cmd == 'q':
                if allDone:
                    sys.exit(1)
                else:
                    print("当前退出是不安全程序不允许 请先使用stops指令")
            else:
                print('没有一个名为' + cmd + '的命令')
