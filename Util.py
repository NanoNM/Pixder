import json
import os
import time
from ssl import SSLError
from urllib import parse

import requests


'''
工具包 存放一些公用组件
'''
class FileAnalysis:
    def fileAnalysis(self, date, init):
        i = 1
        for obj in date:
            i += 1
            # 避免风控加的延迟
            ids = obj['illustId']
            while True:
                print('解析ID: '+ids)
                jsonDate = self.work(obj['illustId'], init)
                if not jsonDate['error']:
                    break
                print('解析错误 可能被风控: ' + ids)
                time.sleep(3)
            obj['illustTitle'] = jsonDate['body']['illustTitle']
            obj['tags'] = jsonDate['body']['tags']['tags']
            obj['original'] = jsonDate['body']['urls']['original']
            obj['likeCon'] = jsonDate['body']['bookmarkCount']
            obj['pageCount'] = jsonDate['body']['pageCount']
            print('解析完成: ' + ids)

    # def panterAnalysis(self, date, init):
    #     i = 1
    #     for obj in date:
    #         i += 1
    #         jsonDate = self.work(obj['illustId'], init)
    #         obj['illustTitle'] = jsonDate['body']['illustTitle']
    #         obj['tags'] = jsonDate['body']['tags']['tags']
    #         obj['original'] = jsonDate['body']['urls']['original']
    #         obj['likeCon'] = jsonDate['body']['likeCount']

    @staticmethod
    def work(ID, init):
        # print("分析"+ID)
        ID = str(ID)
        url = init.signUrl.replace("PixId", ID)
        while True:
            try:
                # response = init.se.get(url, proxies=init.proxies, headers=init.headers, verify=False, ).text
                response = requests.request("GET", url, proxies=init.proxies).text
                # print(response.text)
                # html = init.se.get(url, proxies=init.proxies, headers=init.headers).text
                jsonDate = json.loads(response)
                # print("分析结束" + ID)
                return jsonDate
            except Exception as e:
                print('获取' + ID + '图片信息失败了错误原因: ')
                print('地址' + url + str(e), end='\n重试中\n')
                pass
            except requests.exceptions.SSLError as e:
                print('获取' + ID + '图片信息失败了错误原因: ')
                print('地址' + url + str(e), end='\n重试中\n')
                pass


    @staticmethod
    def UnfinishedTask(init, index, threadInfo, mode):
        unfinishedTaskInfo = {
            "name": init.name,
            "projectName": "log",
            "MaxPage": init.pagenum,
            "minlike": init.minlike,
            "thread": init.thread,
            "classify": init.classify,
            "nowPage": index,
            "mode": mode,

        }
        if os.path.exists(parse.unquote(init.folderName) + '' + os.sep + 'lastTask'):
            pass
        else:
            os.makedirs(parse.unquote(init.folderName) + '' + os.sep + 'lastTask')
        with open('.' + os.sep + parse.unquote(init.folderName) + os.sep + 'lastTask' + os.sep + 'main.log', 'w',
                  encoding='utf-8') as file:
            file.write(json.dumps(unfinishedTaskInfo, ensure_ascii=False))

        if os.path.exists(parse.unquote(init.folderName) + '' + os.sep + 'lastTask'):
            pass
        else:
            os.makedirs(parse.unquote(init.folderName) + '' + os.sep + 'lastTask')
        with open('.' + os.sep + parse.unquote(init.folderName) + os.sep + 'lastTask' + os.sep + str(threadInfo[
            'threadID']) + '.log', 'w',
                  encoding='utf-8') as file:
            file.write(json.dumps(threadInfo, ensure_ascii=False))

    @staticmethod
    def panterUnfinishedTask(init, index, threadInfo, mode):
        unfinishedTaskInfo = {
            "name": init.name,
            "projectName": "log",
            "MaxPage": init.pagenum,
            "minlike": init.minlike,
            "thread": 1,
            "classify": init.classify,
            "nowPage": index,
            "all": mode,

        }

        try:
            if os.path.exists(init.name + '' + os.sep + 'lastTask'):
                pass
            else:
                os.mkdir(init.name + '' + os.sep + 'lastTask')
        except OSError as error:
            print(error)
        if os.path.exists(init.name + '' + os.sep + 'lastTask'):
            pass
        else:
            os.makedirs(init.name + '' + os.sep + 'lastTask')
        with open('.' + os.sep + init.name + os.sep + 'lastTask' + os.sep + 'main.log', 'w', encoding='utf-8') as file:
            file.write(json.dumps(unfinishedTaskInfo, ensure_ascii=False))

        if os.path.exists(init.name + '' + os.sep + 'lastTask'):
            pass
        else:
            os.makedirs(init.name + '' + os.sep + 'lastTask')
        with open('.' + os.sep + init.name + os.sep + 'lastTask' + os.sep + 'main.log', 'w',
                  encoding='utf-8') as file:
            file.write(json.dumps(threadInfo, ensure_ascii=False))


class Judge:
    @staticmethod
    def checkLikeNum(num, date):
        if int(date) > int(num):
            return False
        else:
            return True
