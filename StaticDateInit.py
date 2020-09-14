import requests
from urllib import parse


class StaticDateInit(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, Cookie, name, minlike, pagenum, thread, classify, UserID='null', userAgent=None):
        self.baseUrl = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        self.loginUrl = 'https://accounts.pixiv.net/api/login?lang=zh'
        self.mainUrl = 'http://www.pixiv.net'
        self.pixivId = ''
        self.password = ''
        self.postKey = []
        self.returnTo = 'http://www.pixiv.net/'
        self.loadPath = ''
        self.ipList = []
        self.token = ''
        self.proxies = {}
        self.se = requests.session()
        self.name = parse.quote(name)
        self.minlike = minlike
        self.pagenum = pagenum
        self.thread = thread
        self.targetUrl = 'https://www.pixiv.net/ajax/search/artworks/' \
                         + self.name + '?word=' \
                         + self.name + '&order=date_d&mode=all&s_mode=s_tag&type=all&lang=zh&p='
        self.signUrl = 'https://www.pixiv.net/ajax/illust/PixId?ref=https%3A%2F%2Fwww.pixiv.net%2Fartworks%2FPixId' \
                       '&lang=zh '
        self.headers = {
            'Cookie': Cookie,
            'Referer': self.targetUrl,
            'User-Agent': userAgent,
        }
        self.classify = classify

        self.userPage = 'https://www.pixiv.net/ajax/user/USERID/profile/all?lang=zh'
        self.userID = UserID


def init(Cookie, name, minlike, pagenum, thread, classify, userAgent):
    return StaticDateInit(Cookie, name, minlike, pagenum, thread, classify, userAgent)