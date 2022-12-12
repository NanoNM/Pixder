from main import *

'''
更多指令 暂时没用
'''
def command(cmd):
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
        return 0
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
              'Pixder V0.5.0 by Nanometer\n'
              '血源诅咒真好玩！！！！\n'
              '===========================\n')
    elif cmd == 'q':
        if allDone:
            sys.exit(1)
        else:
            print("当前退出是不安全程序不允许 请先使用stops指令")
    else:
        print('没有一个名为' + cmd + '的命令')
