# -*- encoding: utf-8 -*-
from selenium.webdriver import Edge
from random import uniform
from time import sleep


class XuexiEdge(Edge):
    """
    自定义webdriver
    """

    def __init__(self, executable_path="msedgedriver", port=0, options=None, service_args=None, capabilities=None, service_log_path=None, service=None,
                 keep_alive=False,  verbose=False):
        super().__init__(executable_path, port, options, service_args, capabilities, service_log_path, service,
                         keep_alive, verbose)

    def xuexi_get(self, url):
        """
        自定义webdriver的get请求；
        发起请求前先移除Chrome的window.navigator.webdriver参数，并随机等待，减少被检测的风险
        :param url:
        :return:
        """
        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                window.alert = function() {
                    return;
                }
            '''
        })
        self.get(url)
        self.implicitly_wait(10)
        sleep(round(uniform(1.5, 2.5), 2))
