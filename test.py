# -*-coding:utf-8 -*-

# import requests
#
# url = 'https://cdn.jsdelivr.net/gh/requireCool/stealth.min.js/stealth.min.js'
# html_data = requests.get(url).text
# File = open('/Users/alphag0/Desktop/Code/Python/pythonProject/config/stealth.min.js', 'w+')
# File.write(html_data)
# File.close()

from selenium import webdriver
import time


from selenium import webdriver
import time

# 建立配置Chrome浏览器的选项，Edge浏览器改为"webdriver.EdgeOptions()"
chrome_options = webdriver.ChromeOptions()
# 接管端口号9222的Chrome浏览器
chrome_options.add_experimental_option('debuggerAddress', '127.0.0.1:9515')
# Edge浏览器改为"webdriver.Edge(options=chrome_options)"
browser = webdriver.Chrome(options=chrome_options)
# 访问爬虫检测网站
browser.get('https://bot.sannysoft.com/')
# 60后退出浏览器
time.sleep(60)
browser.quit()