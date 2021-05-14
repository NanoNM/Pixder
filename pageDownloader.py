import os
import zipfile
import imageio
from Util import *
from urllib import parse


def picDoDownloader(init, date, url, part, index):
    if int(init.classify) == 1:
        for tag in date['tags']:
            if 'R-18' == tag['tag']:
                print('分级制度拦截')
                return
        ImgDownloader(init, date, url, part, index)
    elif int(init.classify) == 2:
        index = False
        for tag in date['tags']:
            if 'R-18' == tag['tag']:
                index = True
        if index:
            ImgDownloader(init, date, url, part, index, '' + os.sep + '' + os.sep + 'R-18')
        else:
            ImgDownloader(init, date, url, part, index)
    elif int(init.classify) == 3:
        for tag in date['tags']:
            if 'R-18' == tag['tag']:
                ImgDownloader(init, date, url, part, index)


def ImgDownloader(init, date, url, part, index, R='' + os.sep + '' + os.sep + ''):
    global targeImg
    try:
        sty = url.split(".")[-1]
        PIC = init.se.get(url,proxies=init.proxies, headers=init.headers)
        if os.path.exists(parse.unquote(init.name) + R + '' + os.sep + 'gif'):
            pass
        else:
            os.makedirs(parse.unquote(init.name) + R + '' + os.sep + 'gif')
        if url.find('img-zip-ugoira') != -1:
            targeImg = '.' + os.sep + parse.unquote(init.name) + R + os.sep + 'gif' + os.sep + date['illustId'] + ' ' + date['userId'] + '.' + sty
        else:
            targeImg = '.' + os.sep + parse.unquote(init.name) + R + os.sep + date['illustId']+ ' ' + date['userId'] + part +'.' + sty
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
                gif_images.append(imageio.imread(targeImgz + '' + os.sep + '' + path))
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
        PIC = init.se.get(url,proxies=init.proxies, headers=init.headers)
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
            except Exception as e:
                print(e)
                print('分析链接: ' + Url + '失败了!! 准备重试')
                pass

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
    def picDownloader(init, date):
        judge = Judge()
        if judge.checkLikeNum(init.minlike, date['likeCon']):
            return 0
        index = 0
        while index < date['pageCount']:
            if date['original'].find('p0') != -1:
                part = 'p' + str(index)
                url = date['original'].replace('p0', part)
                index += 1
                print('即将下载: ' + url)
                picDoDownloader(init, date, url, part, index)
            if date['original'].find('ugoira0') != -1:
                # str(date['width'])
                # str(date['height'])
                part = 'ugoira' + '1920' + 'x' + '1080' + '.zip'
                url = date['original'].replace('img-original', 'img-zip-ugoira')
                url = url.replace('ugoira0.jpg', part)
                # print('即将下载动图文件包 1920 x 1080: ' + url)
                picDoDownloader(init, date, url, part, index)
                index += 1
    @staticmethod
    def penterDownloader(init, date):
        pass
