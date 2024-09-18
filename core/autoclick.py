import ast
import os
import pickle
import time
from urllib.parse import urlparse

import requests
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as uc
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

class AutoClick:
    def __init__(self, url, header=None):
        self.__setup(url, header)

    def __setup(self, url, header):
        # 利用undetected_chromedriver创建ChromeWebdriver实例
        # chromedriver_path = '/usr/local/bin/chromedriver'
        # self.driver = uc.Chrome(driver_executable_path=chromedriver_path, use_subprocess=True)

        # 创建ChromeWebdriver实例
        # chromedriver_path = '/usr/local/bin/chromedriver'
        edge_driver = webdriver.Edge()
        header = ast.literal_eval(header)
        def interceptor(request):
            if "Authorization" in header.keys():
                request.headers['Authorization'] = header['Authorization']
            if "Cookie" in header.keys():
                request.headers['Cookie'] = header['Cookie']
            if "Token" in header.keys():
                request.headers['Token'] = header['Token']
        # service = Service(chromedriver_path)
        # self.driver = webdriver.Chrome(service=service)
        self.driver = edge_driver
        self.driver.request_interceptor = interceptor
        self.driver.implicitly_wait(3)

    def find_click(self):
        self.driver.get(url)
        # 检查发送的请求
        time.sleep(1)
        links = self.driver.find_elements(By.XPATH, '//a[@href]')
        for link in links:
            print(f"Link text: {link.text}")
            print(f"Link href: {link.get_attribute('href')}\n")

        # 选择所有带有onclick属性的元素
        onclick_elements = self.driver.find_elements(By.XPATH,"//*[@onclick]")
        for element in onclick_elements:
            print(f"Element text: {element.text}")
            print(f"Element onclick: {element.get_attribute('onclick')}\n")

        # 选择所有<button>标签
        buttons = self.driver.find_elements(By.XPATH,"//button")
        for button in buttons:
            print(f"Button text: {button.text}\n")

        # 选择所有<input>类型为button或submit的标签
        input_buttons = self.driver.find_elements(By.XPATH,"//input[@type='button' or @type='submit']")
        for input_button in input_buttons:
            print(f"Input type: {input_button.get_attribute('type')}")  # 这里只打印类型，因为input没有文本内容
            print(f"Input value: {input_button.get_attribute('value')}\n")


if __name__ == '__main__':
    url = "http://192.168.31.17:8888/dashboard"
    header = "{'Host': '192.168.31.17:8888', 'Proxy-Connection': 'keep-alive', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJsaXhpb25nQG1haWxob2cubG9jYWwiLCJyb2xlIjoidXNlciIsImlhdCI6MTcyNjQ3NDI3OSwiZXhwIjoxNzI3MDc5MDc5fQ.WUg5Ujs_Mt_CMrisQqopl9fepTQC01W2IKsECTYrlzjX2U0PLp1haYDMAbwS21zsNEjQueQNse8iOF09wJR7_bfk3732T9Q94c0ZZJtj9sjhwn8UNLvrytJMdFRezgzVyO-r7xVRFaypJeFWxS9F7al3P4gt8k0GB7uuEGDMATbDBlt102WXll_FT3RWtdg99JJ2mECzOVskUT3SGYbEWl5M6JQAoQ_wW7ggyPQlK1o1kRyRxqHr6ls8ZXnfdCelE5y3bkXG5OQsBNBKOp-qi8S_PxbxqHXYTFBe3WNMdHAzNKN0IATObqNAu7dL2SXr2aJhNeBB0l3L-8Qc84D2hw', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0', 'Content-Type': 'application/json', 'Accept': '*/*', 'Referer': 'http://192.168.31.17:8888/dashboard', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}"
    A = AutoClick(url,header)
    A.find_click()