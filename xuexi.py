# -*- encoding: utf-8 -*-
from json import dumps
from ssl import SSLEOFError
from subprocess import call
from traceback import format_exc
from selenium.webdriver.edge.options import Options as EdgeOptions
from requests.exceptions import SSLError
from urllib3.exceptions import MaxRetryError
from random import randint
from custom.xuexi_edge import XuexiEdge
from getData import get_article, get_video
from getData.version import VERSION
from userOperation import login, check
from operation import scan_article, watch_video, exam, get_chromedriver, check_version
# import pyjion; pyjion.enable();pyjion.config(pgc=False)


def article_or_video():
    """
    伪随机(在随机浏览文章或视频的情况下，保证文章或视频不会连续2次以上重复出现)，浏览文章或视频
    :return: 1(文章)或2(视频)
    """
    rand = randint(1, 2)
    if len(randArr) >= 2 and randArr[len(randArr) - 1] + randArr[len(randArr) - 2] == 2:
        rand = 2
    elif len(randArr) >= 2 and randArr[len(randArr) - 1] + randArr[len(randArr) - 2] == 4:
        rand = 1
    randArr.append(rand)
    return rand


def user_login():
    """
    登录，循环执行，直到登录成功
    :return:
    """
    while not login.login(browser):
        print('--> 登录超时，正在尝试重新登录')
        continue


def run():
    """
    刷视频，刷题目主要部分
    通过check_task()函数决定应该执行什么任务，并调用相应任务函数
    :return: null
    """
    while True:
        checkRes = check.check_task(browser)
        if checkRes == check.CheckResType.NULL:
            break
        elif checkRes == check.CheckResType.ARTICLE:
            scan_article.scan_article(browser)
        elif checkRes == check.CheckResType.VIDEO:
            watch_video.watch_video(browser)
        elif checkRes == check.CheckResType.ARTICLE_AND_VIDEO:
            if article_or_video() == 1:
                scan_article.scan_article(browser)
            else:
                watch_video.watch_video(browser)
        else:
            exam.to_exam(browser, checkRes)


def finally_run():
    """
    程序最后执行的函数，包括打印信息、关闭浏览器等
    """
    browser.quit()
    print(r'''
      __/\\\\\\\\\\\\\____/\\\________/\\\__________/\\\\\\\\\\\\__/\\\\\\\\\\\\_____/\\\\\\\\\\\\\\\_        
       _\/\\\/////////\\\_\///\\\____/\\\/_________/\\\//////////__\/\\\////////\\\__\/\\\///////////__       
        _\/\\\_______\/\\\___\///\\\/\\\/__________/\\\_____________\/\\\______\//\\\_\/\\\_____________      
         _\/\\\\\\\\\\\\\\______\///\\\/___________\/\\\____/\\\\\\\_\/\\\_______\/\\\_\/\\\\\\\\\\\_____     
          _\/\\\/////////\\\_______\/\\\____________\/\\\___\/////\\\_\/\\\_______\/\\\_\/\\\///////______    
           _\/\\\_______\/\\\_______\/\\\____________\/\\\_______\/\\\_\/\\\_______\/\\\_\/\\\_____________   
            _\/\\\_______\/\\\_______\/\\\____________\/\\\_______\/\\\_\/\\\_______/\\\__\/\\\_____________  
             _\/\\\\\\\\\\\\\/________\/\\\____________\//\\\\\\\\\\\\/__\/\\\\\\\\\\\\/___\/\\\_____________ 
              _\/////////////__________\///______________\////////////____\////////////_____\///______________''')

    # call('pause', shell=True)
    input("Please press the Enter key to proceed")


if __name__ == "__main__":
    try:
        from sys import exit
        import ctypes
        from os import getcwd, remove, path
        if get_chromedriver.PLATFROME == 'win':
            ctypes.windll.kernel32.SetConsoleTitleW('xuexi-{}'.format(VERSION))

        try:
            check_version.check()
        except (SSLEOFError, MaxRetryError, SSLError):
            print(str(format_exc()))
            print('--> \033[31m网络连接失败，请检查是否开启了VPN或代理软件，如果开启了请关闭后再试\033[0m')
            print('--> \033[31m当前版本:{}\033[0m'.format(VERSION))
            call('pause', shell=True)
            exit(1)

        if not get_chromedriver.do(getcwd()):
            exit(1)

        options = EdgeOptions()
        options.use_chromium = True
        # 防止检测
        # options.add_argument("--headless")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option(
            'excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("detach", True)
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57')
        options.add_argument("--mute-audio")  # 静音
        options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])  # 禁止打印日志
        options.add_argument('--ignore-certificate-errors')  # 忽略证书错误
        options.add_argument('--ignore-ssl-errors')  # 忽略ssl错误
        options.add_argument('–log-level=3')
        if get_chromedriver.PLATFROME == 'linux':
            options.binary_location = '/opt/apps/com.browser.softedge.stable/files/msedge'

        browser = XuexiEdge(
            path.join(getcwd(), get_chromedriver.EDGEDIRVER), options=options)

        # browser = Edge(os.path.join(os.getcwd(), 'msedgedriver.exe'), options=options)
        browser.maximize_window()

        exam_temp_Path = './data/exam_temp.json'
    except:
        print(str(format_exc()))
        print('--> \033[31m程序异常，请尝试重启脚本\033[0m')
        print('--> \033[31m当前版本:{}\033[0m'.format(VERSION))
        # call('pause', shell=True)
        input("Please press the Enter key to proceed")
    else:
        try:
            with open(exam_temp_Path, 'w', encoding='utf-8') as f:
                dataDict = {
                    'DAILY_EXAM': 'true',
                    'WEEKLY_EXAM': 'true',
                    'SPECIAL_EXAM': 'true'
                }
                f.write(dumps(dataDict, ensure_ascii=False, indent=4))

            get_article.get_article()
            get_video.get_video()
            user_login()
            randArr = []  # 存放并用于判断随机值，防止出现连续看文章或者看视频的情况
            run()
            print('--> 任务全部完成，程序已结束')
        except (SSLEOFError, MaxRetryError, SSLError):
            print(str(format_exc()))
            print('--> \033[31m网络连接失败，请检查是否开启了VPN或代理软件，如果开启了请关闭后再试\033[0m')
            print('--> \033[31m当前版本:{}\033[0m'.format(VERSION))
        except:
            print(str(format_exc()))
            print('--> \033[31m程序异常，请尝试重启脚本\033[0m')
            print('--> \033[31m当前版本:{}\033[0m'.format(VERSION))
        finally:
            remove(exam_temp_Path)
            finally_run()
