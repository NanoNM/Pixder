import requests
from urllib import parse
# from faker import Faker


'''
静态量 存放一些基本不会改变的常量
'''
class StaticDateInit(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    """
        'https://www.pixiv.net/ranking.php?format=json&p='
        'https://www.pixiv.net/ranking.php?mode=weekly&p=2&format=json
        
        'https://www.pixiv.net/ranking.php?mode=daily_r18&format=json&p='
        'https://www.pixiv.net/ranking.php?mode=weekly_r18&p=2&format=json'
        '
    """

    def __init__(self, Cookie, name, minlike, pagenum, thread, classify, proxies, UserID='null', userAgent=None):
        # 基础地址
        self.baseUrl = 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
        # 登陆地址
        self.loginUrl = 'https://accounts.pixiv.net/api/login?lang=zh'
        # 主站地址
        self.mainUrl = 'http://www.pixiv.net'
        # 热榜地址
        self.rankUrl = 'https://www.pixiv.net/ranking.php?format=json'
        # 热榜带种类地址
        self.rankContentUrl = 'https://www.pixiv.net/ranking.php?format=json&content='
        # 用户账户
        self.pixivId = ''
        # 用户密码
        self.password = ''
        # Pixiv登录验证Key
        self.postKey = []
        self.returnTo = 'http://www.pixiv.net/'
        self.loadPath = ''
        self.ipList = []
        self.token = ''
        self.proxies = proxies
        self.se = requests.session()
        self.name = parse.quote(name)
        self.folderName = name.replace(':', '').replace('?', '').replace('\\', '').replace('/', '').replace('*',
                                                                                                            '').replace(
            '|', '').replace('<', '').replace('>', '')
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
        # 代理设置
        self.proxiesAddr = None
        self.proxiesPort = None


def init(Cookie, name, minlike, pagenum, thread, classify, proxies, userAgent):
    # print('随机获取一个UA池的UA')
    # ua = Faker()
    # 过低的UA会导致爬取失败!!!!
    # fakeUa = ua.user_agent()
    fakeUa = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 ' \
             'Safari/537.36 '

    # print('当前UA: ' + fakeUa)
    return StaticDateInit(Cookie, name, minlike, pagenum, thread, classify, proxies, None, fakeUa)
    # return StaticDateInit(Cookie, name, minlike, pagenum, thread, classify,"" ,fakeUa)
