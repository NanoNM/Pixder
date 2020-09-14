import shutil, threading

import StaticDateInit
from pageDownloader import *
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

'''
请勿将本程序用于商业用途！
请勿将本程序用于商业用途！
请勿将本程序用于商业用途！

出事我不负责 一点责任都没有 网警来找你 那是你的事 这个别找我 我没钱付罚款!!!!
出事我不负责 一点责任都没有 网警来找你 那是你的事 这个别找我 我没钱付罚款!!!!
出事我不负责 一点责任都没有 网警来找你 那是你的事 这个别找我 我没钱付罚款!!!!
出事我不负责 一点责任都没有 网警来找你 那是你的事 这个别找我 我没钱付罚款!!!!
出事我不负责 一点责任都没有 网警来找你 那是你的事 这个别找我 我没钱付罚款!!!!
出事我不负责 一点责任都没有 网警来找你 那是你的事 这个别找我 我没钱付罚款!!!!
出事我不负责 一点责任都没有 网警来找你 那是你的事 这个别找我 我没钱付罚款!!!!

我写的代码 我自己都不赚钱 也不是给你用来赚钱的!!! 

'''
'''
新版本特性 增加设置文件 自动生成用户文件
增加代码长度 让我看起来比较NB
注释代码 我下个版本更好修复BUG
'''

BaseData = None
NewTask = True

name = ''
minlike = ''
pagenum = ''
thread = ''
classify = ''
mode = ''


def start(Name):
    Index = True
    while Index:
        print("PixSpider by Nanometer")
        print("建议不要自行关闭程序 强行关闭可能会导致图片下载异常")
        print("网络问题也会导致图片下载异常")
        print("配置文件加载中 . . .")
        if os.path.exists('.\\userInfo.config'):
            global BaseData, NewTask
            Index = False
            with open('.\\userInfo.config', 'r', encoding='utf-8') as file:
                content = file.read()
                config = json.loads(content)
            if os.path.exists(parse.unquote(name) + '\\lastTask\\main.log'):
                x = input('检测到上次的未完成任务 是否继续未完成的任务(Y/N)') or 'y'
                if x == 'Y' or x == 'y':
                    NewTask = False
                    with open(parse.unquote(name) + '\\lastTask\\main.log', 'r', encoding='utf-8') as file:
                        last = file.read()
                        last = json.loads(last)
                    openThread = last['thread']
                    if int(openThread) < 2:
                        BaseData = StaticDateInit.init(config['Cookie'], Name, last['minlike'], last['MaxPage'],
                                                       last['thread'], last['classify'], config['user-agent'])
                        realStart(last['nowPage'], last['MaxPage'])
                    else:
                        print("检测到需要开启多线程! 正在处理线程问题! 请稍等 ... ")
                        BaseData = StaticDateInit.init(config['Cookie'], Name, last['minlike'], last['MaxPage'],
                                                       last['thread'], last['classify'], config['user-agent'])
                        thrIndex = 0
                        print("线程准备启动了! 请稍等 ... ")
                        while thrIndex < int(openThread):
                            path = 'thread' + str(thrIndex)
                            print(path + '文件读取尝试!')
                            with open(parse.unquote(name) + '\\lastTask\\%s.log' % path, 'r', encoding='utf-8') as file:
                                last = file.read()
                                threadLast = json.loads(last)
                            if threadLast['threadStart'] == threadLast['threadStop']:
                                print('在之前任务中, 此线程的任务已结束')
                            print('线程: ' + path + '启动成功并开始从: ' + str(threadLast['threadStart']) + ' 到 ' + str(
                                threadLast['threadStop']) + ' 区间继续任务')
                            work(1, "Thread" + str(thrIndex), threadLast['threadStart'],
                                 threadLast['threadStop']).start()
                            thrIndex += 1
                else:
                    shutil.rmtree(parse.unquote(name) + '\\lastTask')
                    BaseData = StaticDateInit.init(config['Cookie'], Name, minlike, pagenum, thread, classify,
                                                   config['user-agent'])
            else:
                BaseData = StaticDateInit.init(config['Cookie'], Name, minlike, pagenum, thread, classify,
                                               config['user-agent'])
            print("欢迎使用本程序!")
        else:
            print("您是第一次使用本程序? 请按照要求输入信息.")
            item = {"projectName": 'settingFile',
                    'Cookie': input("输入您的Cookie\n"),
                    'user-agent': input("输入您的user-agent\n")}
            #
            with open('.\\userInfo.config', 'w', encoding='utf-8') as file:
                file.write(json.dumps(item, ensure_ascii=False))
            print("请稍等 ..")


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
        while Start <= int(Stop):
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
        self.threadID = threadID
        self.name = name
        self.page = page
        self.stopPage = stopPage

    def run(self):
        # 释放锁，开启下一个线程
        print("开始线程：" + self.name)
        realStart(self.page, self.stopPage, self.name, self.page, self.stopPage)
        print("退出线程：" + self.name)


def panterStart(userID):
    Index = True
    while Index:
        print("配置文件加载中 . . .")
        if os.path.exists('.\\userInfo.config'):
            global BaseData, NewTask
            Index = False
            with open('.\\userInfo.config', 'r', encoding='utf-8') as file:
                content = file.read()
                config = json.loads(content)
            if os.path.exists(userID + '\\lastTask\\main.log'):
                x = input('检测到上次的未完成任务 是否继续未完成的任务(Y/N)') or 'y'
                if x == 'Y' or x == 'y':
                    NewTask = False
                    with open(userID + '\\lastTask\\main.log', 'r', encoding='utf-8') as file:
                        last = file.read()
                        last = json.loads(last)
                    openThread = last['thread']
                    if int(openThread) < 2:
                        with open(userID + '\\lastTask\\None.log', 'r', encoding='utf-8') as file:
                            lastT = file.read()
                            lastT = json.loads(lastT)
                        BaseData = StaticDateInit.init(config['Cookie'], userID, last['minlike'], last['MaxPage'],
                                                       last['thread'], last['classify'], config['user-agent'])
                        realStart(last['nowPage'], last['MaxPage'], None, None, None, lastT['this'])
                        return 0
                    else:
                        print("检测到需要开启多线程! 正在处理线程问题! 请稍等 ... ")
                        BaseData = StaticDateInit.init(config['Cookie'], userID, last['minlike'], last['MaxPage'],
                                                       last['thread'], last['classify'], config['user-agent'])
                        thrIndex = 0
                        print("线程准备启动了! 请稍等 ... ")
                        while thrIndex < int(openThread):
                            path = 'thread' + str(thrIndex)
                            print(path + '文件读取尝试!')
                            with open(parse.unquote(name) + '\\lastTask\\%s.log' % path, 'r', encoding='utf-8') as file:
                                last = file.read()
                                threadLast = json.loads(last)
                            if threadLast['threadStart'] == threadLast['threadStop']:
                                print('在之前任务中, 此线程的任务已结束')
                            print('线程: ' + path + '启动成功并开始从: ' + str(threadLast['threadStart']) + ' 到 ' + str(
                                threadLast['threadStop']) + ' 区间继续任务')
                            work(1, "Thread" + str(thrIndex), threadLast['threadStart'],
                                 threadLast['threadStop']).start()
                            thrIndex += 1
                            return 0
                else:
                    shutil.rmtree(userID + '\\lastTask')
                    BaseData = StaticDateInit.init(config['Cookie'], userID, minlike, pagenum, thread, classify,
                                                   config['user-agent'])
            else:
                BaseData = StaticDateInit.init(config['Cookie'], userID, minlike, pagenum, thread, classify,
                                               config['user-agent'])
            print("欢迎使用本程序!")
        else:
            print("您是第一次使用本程序? 请按照要求输入信息.")
            item = {"projectName": 'settingFile',
                    'Cookie': input("输入您的Cookie\n")}
            with open('.\\userInfo.config', 'w', encoding='utf-8') as file:
                file.write(json.dumps(item, ensure_ascii=False))
            print("请稍等 ..")


if __name__ == '__main__':
    # 执行初始化操作
    mode = input('模式选择 \n1. 遍历模式(默认)\n2. 画师模式\n3. 画模式\n') or '1'
    if mode == '1':
        print('当前模式 遍历模式 如果是想继续上次任务 只需要输入名字 其他全部空白')
        name = input('输入爬取插图的名字: ')
        minlike = input('最小点赞数量 默认5000: ') or '5000'
        pagenum = input('最大爬取页面 默认100: ') or '100'
        thread = input('启用线程数 注意 线程数一定要被最大爬取页面整除并且不能等于最大页面数!!!! 1除外 默认20: ') or '20'
        classify = '1'
        # classify = input('分级模式选择 1: 大众级 2: 限制级+大众级 3: 限制级 默认1: ') or '1'
        start(parse.unquote(name))
        # 模拟登陆 需要人机验证 我不会
        # doLogin(BaseData)
        if int(BaseData.thread) > 1 and NewTask:
            print("检测到需要开启多线程! 正在处理线程问题! 请稍等 ... ")
            evPage = int(BaseData.pagenum) // int(BaseData.thread)
            index = 0
            print("线程准备启动了! 请稍等 ... ")
            while index < int(BaseData.thread):
                # Thread =
                work(1, "Thread" + str(index), evPage * index + 1, evPage * (index + 1)).start()
                index += 1
        else:
            realStart(1, BaseData.pagenum)
    elif mode == '2':
        print('当前模式 画师模式 如果是想继续上次任务 只需要输入画师ID 其他全部空白')
        userID = input('请输入画师ID') or None
        minlike = input('最小点赞数量 默认5000: ') or '5000'
        # thread = input('输入启用线程线程 默认1: ') or '1'
        thread = '1'
        classify = '1'
        # classify = input('分级模式选择 1: 大众级 2: 限制级+大众级 3: 限制级 默认1: ') or '1'
        ints = panterStart(userID)
        if ints == 0:
            pass
        else:
            if int(BaseData.thread) > 1 and NewTask:
                print("检测到需要开启多线程! 正在处理线程问题! 请稍等 ... ")
                evPage = int(BaseData.pagenum) // int(BaseData.thread)
                index = 0
                print("线程准备启动了! 请稍等 ... ")
                while index < int(BaseData.thread):
                    # Thread =
                    work(1, "Thread" + str(index), evPage * index + 1, evPage * (index + 1)).start()
                    index += 1
            else:
                realStart()
    elif mode == '3':
        print('当前模式 画模式(未制作) 如果是想继续上次任务 只需要输入画师ID 其他全部空白')
        pass