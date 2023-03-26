import sys
import zipfile
import imageio
from Util import *
from urllib import parse

'''
下载类 会分析和下载联系啊
'''
# 分级管理
def picDoDownloader(init, date, url, part, index):
    # print("URL ============= " + url)
    if int(init.classify) == 1:
        for tag in date['tags']:
            if 'R-18' == tag['tag'] or 'R-18G' == tag['tag']:
                print('分级制度拦截 R-18/R-18G')
                return
        ImgDownloader(init, date, url, part, index)
    elif int(init.classify) == 2:
        index = False
        for tag in date['tags']:
            if 'R-18G' == tag['tag']:
                print('分级制度拦截 R-18G')
                return
            if 'R-18' == tag['tag']:
                index = True
        if index:
            ImgDownloader(init, date, url, part, index, '' + os.sep + '' + os.sep + 'R-18')
        else:
            ImgDownloader(init, date, url, part, index)
    elif int(init.classify) == 3:
        for tag in date['tags']:
            if 'R-18G' == tag['tag']:
                print('分级制度拦截 R-18G')
                return
            if 'R-18' == tag['tag']:
                ImgDownloader(init, date, url, part, index)
    elif int(init.classify) == 4:
        index = 0
        for tag in date['tags']:
            if 'R-18' == tag['tag']:
                index = 2
            if 'R-18G' == tag['tag']:
                index = 1
                break

        if index == 2:
            ImgDownloader(init, date, url, part, index, '' + os.sep + '' + os.sep + 'R-18')
        elif index == 1:
            ImgDownloader(init, date, url, part, index, '' + os.sep + '' + os.sep + 'R-18G')
        else:
            ImgDownloader(init, date, url, part, index)

    elif int(init.classify) == 5:
        for tag in date['tags']:
            if 'R-18G' == tag['tag']:
                ImgDownloader(init, date, url, part, index, '' + os.sep + '' + os.sep + 'R-18G')
            if 'R-18' == tag['tag']:
                ImgDownloader(init, date, url, part, index, '' + os.sep + '' + os.sep + 'R-18')


def ImgDownloader(init, date, url, part, index, R='' + os.sep + '' + os.sep + ''):
    targeImg = None
    try:
        sty = url.split(".")[-1]
        PIC = init.se.get(url, proxies=init.proxies, headers=init.headers)
        if os.path.exists(parse.unquote(init.name) + R + '' + os.sep + 'gif'):
            pass
        else:
            os.makedirs(parse.unquote(init.name) + R + '' + os.sep + 'gif')
        if url.find('img-zip-ugoira') != -1:
            targeImg = '.' + os.sep + parse.unquote(init.name) + R + os.sep + 'gif' + os.sep + str(date['illustId']) + ' ' + \
                       str(date['userId']) + '.' + sty
        else:
            targeImg = '.' + os.sep + parse.unquote(init.name) + R + os.sep + str(date['illustId']) + ' ' + str(date[
                'userId']) + part + '.' + sty
        if os.path.exists(targeImg):
            print('图片 ' + url + ' 存在,跳过了!')
            return 0
        with open(targeImg, mode='wb') as pic:
            pic.write(PIC.content)

        """unzip zip file"""
        if url.find('img-zip-ugoira') != -1:
            # print('动图组 ' + url + ' 解压中')
            zip_file = zipfile.ZipFile(targeImg)
            targeImgz = targeImg + 'z'
            if os.path.isdir(targeImgz):
                pass
            else:
                os.mkdir(targeImgz)
            for names in zip_file.namelist():
                zip_file.extract(names, targeImgz)
            zip_file.close()
            # print('动图组 ' + url + ' 解压结束')
            # print('动图组 ' + url + ' 生成GIF中')
            img_paths = []
            for root, dirs, files in os.walk(targeImgz):
                img_paths = files
            gif_images = []
            for path in img_paths:
                gif_images.append(imageio.v2.imread(targeImgz + '' + os.sep + '' + path))
            imageio.mimsave(targeImgz + '' + os.sep + '' + "final.gif", gif_images, fps=24)
            # print('动图组 ' + url + ' 生成GIF结束')
            # print('动图组 ' + url + ' 垃圾文件处理中')
            for path in img_paths:
                os.remove(targeImgz + '' + os.sep + '' + path)
            # print('动图组 ' + url + ' 垃圾文件处理结束')
        # print('下载 ' + url + '结束了! 请自行检查文件是否成功!')
        return 0
    except Exception as e:
        print('下载/解压 ' + url + '失败了!', end='')
        print(e)
        PIC = init.se.get(url, proxies=init.proxies, headers=init.headers)
        if os.path.exists(parse.unquote(init.name) + R):
            pass
        else:
            os.makedirs(parse.unquote(init.name) + R)
        with open(targeImg, mode='wb') as pic:
            pic.write(PIC.content)
        # print('下载 ' + url + '结束了! 请自行检查文件是否成功!')
        return 0


class Downloader:
    @staticmethod
    def jsonLoadAnalysis(init, index):
        Url = init.targetUrl + str(index)
        print('分析链接: ' + Url)
        while True:
            try:
                html = init.se.get(Url, proxies=init.proxies, headers=init.headers, verify=False, ).text
                # print(init.headers)
                html = json.loads(html)
                # print(html)
                signPixivEntrys = []
                for dates in html['body']['illustManga']['data']:
                    pass
                    item = {
                        'illustId': dates['id'],
                        'illustTitle': dates['title'],
                        'tags': dates['tags'],
                        'pageCount': dates['pageCount'],
                        # 'isAdContainer': dates['isAdContainer'],
                        'userId': dates['userId'],
                        'userName': dates['userName'],
                        'width': dates['width'],
                        'height': dates['height']
                    }
                    signPixivEntrys.append(item)
                print('分析链接: ' + Url + '结束了!')
                return signPixivEntrys
            except TypeError as te:
                print('错误: ' + str(te) + '\n可能是登录失效了,请删除同级目录下的userinfo.json后重新登录')
                print('分析链接: ' + Url + '失败了!!')
                sys.exit(0)
            except Exception as e:
                print(e)
                print('分析链接: ' + Url + '失败了!! 准备重试')
                pass

    @staticmethod
    def rankJsonLoadAnalysis(init, threadID, modeType, content, primaryClassify, page):
        contentStr = None
        signPixivEntrys = []
        if content == '2':
            contentStr = 'illust'
        elif content == '3':
            contentStr = 'ugoira'
        elif content == '4':
            contentStr = 'manga'


        modeTypeStr = None
        if primaryClassify == '1':
            if modeType == '1':
                modeTypeStr = 'daily'
            elif modeType == '2':
                modeTypeStr = 'weekly'
            elif modeType == '3':
                modeTypeStr = 'monthly'
            elif modeType == '4':
                modeTypeStr = 'rookie'
            elif modeType == '5':
                modeTypeStr = 'original'
            elif modeType == '6':
                modeTypeStr = 'male'
            elif modeType == '7':
                modeTypeStr = 'female'
        elif primaryClassify == '3':
            if modeType == '1':
                modeTypeStr = 'daily_r18'
            elif modeType == '2':
                modeTypeStr = 'weekly_r18'
            # elif modeType == '3':
            #     modeTypeStr = 'monthly_r18'
            # elif modeType == '4':
            #     modeTypeStr = 'rookie_r18'
            # elif modeType == '5':
            #     modeTypeStr = 'original_r18'
            elif modeType == '6':
                modeTypeStr = 'male_r18'
            elif modeType == '7':
                modeTypeStr = 'female_r18'
        elif primaryClassify == '4':
            modeTypeStr = 'r18g'

        #
        if content == '1':
            url = init.rankUrl + '&mode=' + modeTypeStr + '&p=' + str(page)
        else:
            url = init.rankContentUrl + contentStr + '&mode=' + modeTypeStr + '&p=' + str(page)
        html = init.se.get(url, proxies=init.proxies, headers=init.headers, verify=False, ).text
        try:
            htmlJson = json.loads(html)
        except json.decoder.JSONDecodeError as e:
            print("cookie失效或者反扒机制更新")
            print(e)
            sys.exit(1)
        try:
            for datas in htmlJson['contents']:
                item = {
                    'illustId': datas['illust_id'],
                    'illustTitle': datas['title'],
                    'tags': datas['tags'],
                    'pageCount': datas['illust_page_count'],
                    # 'isAdContainer': dates['isAdContainer'],
                    'userId': datas['user_id'],
                    'userName': datas['user_name'],
                    'width': datas['width'],
                    'height': datas['height']
                }
                signPixivEntrys.append(item)
            return signPixivEntrys
        except KeyError as e:
            return []

    @staticmethod
    def penterJsonLoadAnalysis(init):
        Url = init.userPage.replace('USERID', init.name)
        print('分析链接: ' + Url)
        while True:
            try:
                html = init.se.get(Url, proxies=init.proxies, headers=init.headers, verify=False, ).text
                html = json.loads(html)

                PixIDs = []
                for key in html['body']['illusts']:
                    item = {'illustId': key, 'illustTitle': '', 'tags': '', 'pageCount': 0, 'isAdContainer': '',
                            'userId': '', 'userName': '', 'width': '', 'height': ''}
                    PixIDs.append(item)
                for key in html['body']['manga']:
                    item = {'illustId': key, 'illustTitle': '', 'tags': '', 'pageCount': 0, 'isAdContainer': '',
                            'userId': '', 'userName': '', 'width': '', 'height': ''}
                    PixIDs.append(item)
                print('分析链接: ' + Url + ' 结束了')
                return PixIDs
            except Exception as e:
                print(e)
                print('分析链接: ' + Url + ' 失败了')
                pass

    @staticmethod
    def rankPicDownloader(init, date):
        pass
    @staticmethod
    def picDownloader(init, date):
        judge = Judge()
        if judge.checkLikeNum(init.minlike, date['likeCon']):
            return 0

        illustId = str(date['illustId'])
        print("解析" + illustId + "中")
        url = 'https://www.pixiv.net/ajax/illust/' + illustId + '/pages'
        illust_pages = init.se.get(url, proxies=init.proxies, headers=init.headers).text
        illust_pages = json.loads(illust_pages)
        # print(illust_pages)
        imgs = illust_pages['body']
        i = 0
        for img in imgs:
            part = 'p' + str(i)
            original_url = img['urls']['original']
            if 'ugoira' in original_url:
                # print('即将下载动图文件包 1920 x 1080: ' + original_url)
                gifUrl = 'https://www.pixiv.net/ajax/illust/' + str(date['illustId']) + '/ugoira_meta?lang=zh'
                gifUrlJsonStr = init.se.get(gifUrl, proxies=init.proxies, headers=init.headers).text
                gifUrlJson = json.loads(gifUrlJsonStr)
                originalSrc = gifUrlJson['body']['originalSrc']
                picDoDownloader(init, date, originalSrc, part, i)
                i += 1
                pass
            else:
                print('即将下载: ' + original_url)
                picDoDownloader(init, date, original_url, part, i)
                i += 1
        # index = 0
        # while index < date['pageCount']:

            # if date['original'] is None:
                # return
            # if date['original'].find('p0') != -1:
            #     part = 'p' + str(index)
            #     url = date['original'].replace('p0', part)
            #     index += 1
            #     print('即将下载: ' + url)
            #     picDoDownloader(init, date, url, part, index)
            # if date['original'].find('ugoira0') != -1:
            #     gifUrl = 'https://www.pixiv.net/ajax/illust/' + str(date['illustId']) + '/ugoira_meta?lang=zh'
            #     gifUrlJsonStr = init.se.get(gifUrl, proxies=init.proxies, headers=init.headers).text
            #     gifUrlJson = json.loads(gifUrlJsonStr)
            #     # str(date['width'])
            #     # str(date['height'])
            #     url = gifUrlJson['body']['originalSrc']
            #     part = 'ugoira' + '1920' + 'x' + '1080' + '.zip'
            #     # url = date['original'].replace('img-original', 'img-zip-ugoira')
            #     # url = url.replace('ugoira0.jpg', part)
            #     print('即将下载动图文件包 1920 x 1080: ' + url)
            #     picDoDownloader(init, date, url, part, index)
            #     index += 1

    @staticmethod
    def penterDownloader(init, date):
        pass
