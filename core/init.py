# -*-coding:utf-8 -*-
from lib.config import *
from lib.getmsg import *
from core.autologin import *


class Init:
    def __init__(self):
        read_config_file()
        self.urls = read_urls()
        self.credentials = read_credentials()
        self.login_parameters = read_login_parameters()
        self.login_credential = self.__default_login_credential()
        self.login_url = self.__default_url()

    def __default_login_credential(self):
        # 获取第一个credential作为登录信息
        if self.credentials is not None:
            return self.credentials[0]['username'], self.credentials[0]['password']
        else:
            return '', ''

    def __default_url(self):
        # 获取第一个url作为测试目标
        if self.urls is not None:
            return self.urls[0]['url']
        else:
            return ''

    def set_login_credential(self):
        # 设置登录用户名密码
        if self.credentials is None:
            print('[!] credentials is None')
        else:
            print(f'[+] {self.credentials}')
        login_info = login_credential(self.credentials)

        if isinstance(login_info, str):
            self.login_credential = login_info.split(':')[0], login_info.split(':')[1]

    def set_login_url(self):
        # 设置测试目标, 获取登录后的Cookie
        if self.urls is None:
            print('[!] urls is None')
        else:
            print(f'[+] {self.urls}')
        url = target_url(self.urls)

        if isinstance(url, str):
            username, password = self.login_credential
            auto_login = AutoLogin()
            auto_login.test_login(url, username, password)

