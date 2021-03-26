import json
import os
from urllib import parse


class FileAnalysis:
    def fileAnalysis(self, date, init):
        i = 1
        for obj in date:
            i += 1
            jsonDate = self.work(obj['illustId'], init)
            obj['illustTitle'] = jsonDate['body']['illustTitle']
            obj['tags'] = jsonDate['body']['tags']['tags']
            obj['original'] = jsonDate['body']['urls']['original']
            obj['likeCon'] = jsonDate['body']['bookmarkCount']
            obj['pageCount'] = jsonDate['body']['pageCount']

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
        url = init.signUrl.replace("PixId", ID)
        while True:
            try:
                html = init.se.get(url, proxies=init.proxies, headers=init.headers).text
                jsonDate = json.loads(html)
                return jsonDate
            except Exception as e:
                print('获取' + url + '失败了错误原因: ')
                print(e, end=' 重试中\n')
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
        with open('.' + os.sep + parse.unquote(init.folderName) + os.sep + 'lastTask' + os.sep + threadInfo[
            'threadID'] + '.log', 'w',
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
