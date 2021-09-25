# -*- encoding: utf-8 -*-
from requests import get
from re import compile
from subprocess import Popen, PIPE, call
from traceback import format_exc
from zipfile import ZipFile
import winreg
from json import loads


def do(program_path):
    """
    检测并更新ChromeDriver
    :param program_path: ChromeDriver路径（文件夹路径）
    :return: 执行结果 True：执行成功，False：执行失败
    """
    settingsPath = 'data/settings.json'
    with open(settingsPath, 'r', encoding='utf-8') as f:
        settings = f.read()
    settings = loads(settings)
    if settings['自动更新ChromeDriver'] != "true":
        return True
    try:
        return True
    except:
        print(str(format_exc()))
        print('--> 程序异常，请确保你的chrome浏览器是最新版本，然后重启脚本')
        call('pause', shell=True)
        return False


def get_download_version(current_version, url):
    """
    根据本地Chrome版本号获取可下载的ChromeDriver版本号
    :param current_version: 当前本地Chrome版本号前三位
    :param url: ChromeDriver链接
    :return: 完整版本号
    """
    rep = get(url).text
    version_list = []  # 存放版本号
    result = compile(r'\d.*?/</a>.*?Z').findall(rep)  # 匹配文件夹（版本号）和时间
    for i in result:
        version = compile(r'.*?/').findall(i)[0][:-1]  # 提取版本号
        version_list.append(version)
    version_list.reverse()
    download_version = version_list[0]
    for v in version_list:
        if compile(r'^[1-9]\d*\.\d*.\d*').findall(v)[0] == current_version:
            download_version = v
            break
    return download_version


def download_chromedriver(download_url):
    """
    下载chromedriver
    :param download_url: 下载链接
    """
    file = get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:  # 保存文件到脚本所在目录
        zip_file.write(file.content)
        print('--> ChromeDriver下载成功')


def get_version(path):
    """
    获取当前ChromeDriver版本号前三位
    :param path: chromedriver文件夹路径
    :return: 版本号前三位
    """
    import os
    version_info = Popen([os.path.join(path, 'msedgedriver.exe'), '--version'], shell=True,
                         stdout=PIPE).stdout.read().decode()
    return compile(r'^[1-9]\d*\.\d*.\d*').findall(version_info.split(' ')[1])[0]


def unzip_file(path):
    """
    解压chromedriver.zip到指定目录
    :param path: 解压目录
    """
    f = ZipFile('chromedriver.zip', 'r')
    for file in f.namelist():
        f.extract(file, path)
    f.close()
    print('--> 解压成功')
    import os
    os.remove('chromedriver.zip')
    print('--> 压缩包已删除')


def get_chrome_version():
    """
    获取当前Chrome浏览器版本号
    :return: 版本号前三位
    """
    version_re = compile(r'^[1-9]\d*\.\d*.\d*')
    try:
        # 从注册表中获得版本号
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
        version, _ = winreg.QueryValueEx(key, 'version')
        return version_re.findall(version)[0]  # 返回前3位版本号
    except WindowsError as e:
        print('Chrome版本检查失败:{}'.format(e))
