# -*-coding:utf-8 -*-
import json
import os
import pickle
import time
from urllib.parse import urlparse

import requests
from requests.cookies import RequestsCookieJar
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from lib.ocr import *
from lib.read_json import write_data_to_file


class AutoLogin:
    # 用于获取登录成功的Cookie等凭据
    def __init__(self):
        self.__setup()

    def __setup(self):
        # 利用undetected_chromedriver创建ChromeWebdriver实例
        # chromedriver_path = '/usr/local/bin/chromedriver'
        # self.driver = uc.Chrome(driver_executable_path=chromedriver_path, use_subprocess=True)

        # 创建ChromeWebdriver实例
        # chromedriver_path = '/usr/local/bin/chromedriver'
        self.original_url = None
        edge_driver = webdriver.Edge()
        # service = Service(chromedriver_path)
        # self.driver = webdriver.Chrome(service=service)
        self.driver = edge_driver
        self.driver.implicitly_wait(2)

    def test_login(self, url, username, password):
        self.original_url = url
        while True:
            login_page_url = ''
            cookies_jar = self.is_exist_domain(url)
            if cookies_jar:
                return cookies_jar

            self.driver.get(url=url)
            login_page_url = self.driver.current_url
            time.sleep(3)
            cookies = self.driver.get_cookies()
            cookies_jar = RequestsCookieJar()
            for cookie in cookies:
                cookies_jar.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])
            input_names = self.get_input_name()
            if len(input_names) < 3:
                #username and password
                #TODO:置信度
                username_input = input_names[0]
                password_input = input_names[1]
            else:
                # username and password
                # TODO:置信度
                username_input = input_names[0]
                password_input = input_names[1]
                relevant_inputs = self.get_verify_input()
                if len(relevant_inputs) > 1:
                    verification_code_input = relevant_inputs[0]
                    session = requests.session()
                    session.cookies.update(cookies_jar)
                    verification_code = self.get_verification_code(session)
                    # verification_code_input = self.driver.find_element(By.NAME, 'yzm')
                    if verification_code:
                        verification_code_input.send_keys(verification_code)
            username_input.send_keys(username)
            password_input.send_keys(password)
            login_buttons = self.get_submit_name()
            login_button = login_buttons[0]
            login_button.click()
            time.sleep(1)
            if login_page_url == self.driver.current_url:
                print("faild")
            else:
                print("success login")
                break
        time.sleep(1)
        login_header = self.get_valid_header(self.driver.current_url)
        parse_header = self.parse_headers(str(login_header))
        return parse_header

    def get_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def get_valid_header(self,current_url):
        last_matched_headers = None
        for request in self.driver.requests:
            if request.url.endswith('.js') or request.url.endswith('.css') or request.url.endswith('.ico') or request.url.endswith('.png') or request.url.endswith('.jpg') or request.url.endswith('.jpeg') or request.url.endswith('.gif') or request.url.endswith('.txt') or request.url.endswith('.json'):
                continue
            if self.get_domain(request.url) != self.get_domain(current_url):
                continue
            last_matched_headers = request.headers
        return last_matched_headers
    def get_verification_code(self, session):
        try:
            driver = self.driver
            # 获取验证码图片的src属性
            captcha_img = driver.find_element(By.CLASS_NAME, 'img_verif')
            captcha_src = captcha_img.get_attribute('src')
            verification_code = identify(captcha_src, session)
            print(f'[+] 验证码为: {verification_code}')
            return verification_code
        except:
            return False
    def get_input_name(self):
        # 获取所有的 input 元素
        input_elements = self.driver.find_elements(By.TAG_NAME, "input")
        # 遍历 input 元素,找出 type 不为 hidden 的
        visible_input_elements = []
        for input_element in input_elements:
            input_type = input_element.get_attribute("type")
            if input_type != "hidden" and input_type != "checkbox":
                visible_input_elements.append(input_element)
        return visible_input_elements


    def get_submit_name(self):
        # self.driver.get(url=url)
        # 找出所有可点击的按钮元素
        clickable_buttons = []
        # 查找 input 框中 type 为 "submit" 或 "button" 的元素
        input_elements = self.driver.find_elements(By.TAG_NAME,"input")
        buttons_elements = self.driver.find_elements(By.TAG_NAME, "button")
        for input_element in input_elements:
            input_type = input_element.get_attribute("type")
            if input_type in ["button"]:
                clickable_buttons.append(input_element)
        for button_element in buttons_elements:
            input_type = button_element.get_attribute("type")
            if input_type in ["submit"]:
                clickable_buttons.append(button_element)
        if clickable_buttons == []:
            # 查找直接使用 <button> 标签的元素
            button_elements = self.driver.find_elements(By.TAG_NAME,"button")
            clickable_buttons.extend(button_elements)
        return clickable_buttons

    def get_verify_input(self):
        # self.driver.get(url=url)
        # 查找包含关键词的 input 元素
        input_elements = self.driver.find_elements(By.TAG_NAME, "input")
        relevant_inputs = []
        for input_element in input_elements:
            # 检查父元素是否存在 'display: none' 或 'hidden' 属性
            parent_element = input_element.find_element(By.XPATH, "..")
            parent_style = parent_element.get_attribute("style")
            if "display: none" in parent_style or "hidden" in parent_style:
                continue
            attributes = [
                input_element.get_attribute("class"),
                input_element.get_attribute("name"),
                input_element.get_attribute("id"),
                input_element.get_attribute("placeholder")
            ]
            for attribute in attributes:
                if attribute and (
                        "code" in attribute.lower() or
                        "verify" in attribute.lower() or
                        "yzm" in attribute.lower() or
                        "验证码" in attribute or
                        "captcha" in attribute.lower()
                ):
                    relevant_inputs.append(input_element)
        return relevant_inputs

    def is_exist_domain(self,url):
        # 使用 urllib.parse.urlparse() 函数解析 URL
        parsed_url = urlparse(url)
        # 获取 domain 部分
        domain = parsed_url.netloc
        file_name = f"{domain}.pkl"
        # 检查 temp 文件夹中是否存在对应的 cookie 文件
        cookie_file_path = os.path.join("../temp", file_name)
        if os.path.isfile(cookie_file_path):
            # 从文件中读取 RequestsCookieJar 对象
            with open(cookie_file_path, "rb") as f:
                cookies_jar = pickle.load(f)
            return cookies_jar

    def parse_headers(self, headers):
        # 将文件内容按行分割
        lines = headers.strip().split("\n")
        # 创建字典用于存储键值对
        headers_dict = {}
        # 遍历每一行，解析键值对
        for line in lines:
            key, value = line.split(": ")
            headers_dict[key] = value
        return headers_dict

    def get_difference(self, list1, list2):
        difference = [item for item in list1 if item not in list2]
        return difference

    def click_element(self,element):
        """尝试点击一个元素，并处理可能的异常。"""
        try:
            original_url = self.driver.current_url
            # # 悬停前获取所有元素
            # initial_elements = self.driver.find_elements(By.XPATH, "//*")
            # initial_count = len(initial_elements)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click(element).perform()
            # # 悬停后获取所有元素
            # final_elements = self.driver.find_elements(By.XPATH, "//*")
            # final_count = len(final_elements)
            if original_url != self.driver.current_url:
                self.find_click_main()
        except Exception as e:
            pass

    def click_all_elements(self, element):
        """递归点击所有元素，包括嵌套的子元素。"""
        # 尝试点击当前元素
        self.click_element(element)

        # 获取当前元素下的所有子元素
        child_elements = element.find_elements(By.XPATH, './*')
        for child in child_elements:
            self.click_all_elements(child)

    def get_request(self):
        request_response_pairs = []
        for request in self.driver.requests:
            if request.url.endswith('.js') or request.url.endswith('.css') or request.url.endswith('.ico') or request.url.endswith('.png') or request.url.endswith('.jpg') or request.url.endswith('.jpeg') or request.url.endswith('.gif') or request.url.endswith('.txt') or request.url.endswith('.json') or request.url.endswith('.svg'):
                continue
            if self.get_domain(request.url) != self.get_domain(self.original_url):
                continue
            if request.response:  # 确保响应存在
                # 构建包含请求和响应信息的字典
                request_info = {
                    'url': request.url,
                    'method': request.method,
                    'headers': dict(request.headers),
                    'body': request.body.decode('utf-8') if request.body else None,
                    'params': dict(request.params),
                    'response_status_code': request.response.status_code,
                    'response_headers': dict(request.response.headers),
                    'response_body': request.response.body.decode('utf-8') if request.response.body else None
                }
                # 将字典添加到列表中
                request_response_pairs.append(request_info)

            # 打印所有请求和响应信息
            # for data in request_response_pairs:
            #     print(data['url'])
            # 将所有请求和响应信息存储为JSON文件
            write_data_to_file("request_response_pairs.json",request_response_pairs)

    def find_click_navi(self):
        original_url = self.driver.current_url
        # 获取<header>元素
        header_element = self.driver.find_element(By.TAG_NAME, "header")
        # 递归点击<header>元素下的所有元素
        self.click_all_elements(header_element)
        self.get_request()

    def find_click_main(self):
        try:
            original_url = self.driver.current_url
            # 提取所有<a>标签
            links = self.driver.find_elements(By.XPATH, '//a[@href]')
            # 提取所有带有onclick属性的元素
            onclick_elements = self.driver.find_elements(By.XPATH, "//*[@onclick]")
            # 提取所有<button>标签
            buttons = self.driver.find_elements(By.XPATH, "//button")
            # 提取所有<input>类型为button或submit的标签
            input_buttons = self.driver.find_elements(By.XPATH, "//input")
            # 合并所有元素到一个列表中
            all_elements = links + onclick_elements + buttons + input_buttons
            # 去重，这里使用集合的原因是集合不允许重复元素
            unique_elements = set(all_elements)
            self.find_textarea()
            self.find_text_input()
            self.find_file_upload()
        except Exception as e:
            pass
        # 遍历去重后的元素并点击
        for element in unique_elements:
            try:
                print(f"Element text: {element.text}")
                element.click()
                if original_url != self.driver.current_url:
                    print("内容页面跳转")
                    self.find_click_main()
                try:
                    dropdown_button_first = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-select-dropdown .ant-select-item-option:nth-child(1)"))
                    )
                    if dropdown_button_first:
                        dropdown_button_first.click()
                        print("下拉已选择")
                except Exception as e:
                    pass

                try:
                    text_inputs = WebDriverWait(self.driver, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='text']")))
                    if text_inputs:
                        for input_element in text_inputs:
                            if "email" in input_element.get_attribute("id"):
                                input_element.clear()
                                input_element.send_keys("caso@mailhog.local")
                            else:
                                input_element.clear()
                                input_element.send_keys("test")
                except Exception as e:
                    pass

                try:
                    confirm_button = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".ant-modal-confirm-btns button.ant-btn-primary"))
                    )
                    # 遍历所有找到的输入框
                    if confirm_button:
                        confirm_button.click()
                        print("弹窗已处理")
                except Exception as e:
                    pass

            except Exception as e:
                pass
    def find_textarea(self):
        try:
            # 查找页面上所有的textarea元素
            textareas = self.driver.find_elements(By.TAG_NAME,"textarea")
            if textareas:
                # 遍历所有找到的textarea元素
                for textarea in textareas:
                    # 填充文本，你可以替换为你需要填充的内容
                    textarea.send_keys("12313131")
        except Exception as e:
            pass

    def find_text_input(self):
        try:
            # 获取页面上所有type为text的input输入框
            text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
            # 遍历所有找到的输入框
            for input_element in text_inputs:
                # 填充值，这里以"test"为例，你可以根据实际情况修改
                input_element.send_keys("test")
        except Exception as e:
            pass

    def find_file_upload(self):
        try:
            # 获取页面上所有type为text的input输入框
            file_inputs = self.driver.find_element(By.CSS_SELECTOR,'input[type="file"]')
            # 遍历所有找到的输入框
            for file_element in file_inputs:
                if file_element.get_attribute("accept") == "image/*":
                    file_element.send_keys('"C:\\Users\\75215\\Desktop\\pythonProject\\API-security-main\\20221106-API安全01-crAPI漏洞靶场.assets\\image-20221031204205370.png"')
        except Exception as e:
            pass



if __name__ == '__main__':
    url = "http://192.168.31.17:8888/login"
    uestcurl = "https://hq.uestc.edu.cn/dormitory/dormitoryOnlineChooseRoom/index"
    edge = AutoLogin()
    logined_headers = edge.test_login(url,'caso4@mailhog.local','Admin@123')
    edge.find_click_navi()