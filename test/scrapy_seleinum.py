# coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from icecream import ic
import re
import time
from functools import reduce
from pprint import pprint
import pickle

"""
note: 需要使用selenium，chrome版本需要与chromedriver版本对应。具体见https://chromedriver.storage.googleapis.com/
该文件仅作测试用，可能失效
"""


def login(username='', password=''):
    # 打开微信公众号登录页面
    driver.get("https://mp.weixin.qq.com/")
    driver.maximize_window()
    # time.sleep(1)
    # 自动填充帐号密码
    # driver.find_element(By.XPATH,
    #     '//*[@id="header"]/div[2]/div/div/div[2]/a'
    # ).click()
    # driver.find_element(By.XPATH,
    #     # '//*[@id="header"]/div[2]/div/div/form/div[1]/div[1]/div/span/input'
    #     '//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input'
        
    # ).clear()
    # driver.find_element(By.XPATH,
    #     # '//*[@id="header"]/div[2]/div/div/form/div[1]/div[1]/div/span/input'
    #     '//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[1]/div/span/input'
    # ).send_keys(username)
    # driver.find_element(By.XPATH,
    #     # '//*[@id="header"]/div[2]/div/div/form/div[1]/div[2]/div/span/input'
    #    '//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input'
    # ).clear()
    # driver.find_element(By.XPATH,
    #     # '//*[@id="header"]/div[2]/div/div/form/div[1]/div[2]/div/span/input'
    #    '//*[@id="header"]/div[2]/div/div/div[1]/form/div[1]/div[2]/div/span/input'
    # ).send_keys(password)

    # time.sleep(1)
    # # 自动点击登录按钮进行登录
    # driver.find_element(By.XPATH,
    #     # '//*[@id="header"]/div[2]/div/div/form/div[4]/a'
    #     '//*[@id="header"]/div[2]/div/div/div[1]/form/div[4]/a'
    # ).click()
    # 拿手机扫二维码！
    time.sleep(10)


def open_link(nickname, start_page=1):
    # 写新的图文
    driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[3]/div[2]/div/div[2]').click()

    # 切换到新窗口
    for handle in driver.window_handles:
        if handle != driver.current_window_handle:
            driver.switch_to.window(handle)

    # 点击超链接
    driver.find_element(By.XPATH,'//*[@id="js_editor_insertlink"]').click()
    time.sleep(10)
    # 选择其他公众号
    driver.find_element(By.XPATH,'//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[4]/div/div/p/div/button').click()
    # 输入公众号名称
    input_name = driver.find_element(By.XPATH,
        '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[4]/div/div/div/div/div[1]/span/input'
    )
    input_name.clear()
    input_name.send_keys(nickname)
    input_name.send_keys(Keys.ENTER)
    time.sleep(3)
    # 点击第一个公众号
    driver.find_element(By.XPATH,
        '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[4]/div/div/div/div[2]/ul/li[1]/div[1]'
    ).click()
    time.sleep(3)

    # pages
    total_pages = driver.find_element(By.XPATH, 
                                        '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[5]/div/div/div[3]/span[1]/span/label[2]').text
    current_page = driver.find_element(By.XPATH, 
                                        '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[5]/div/div/div[3]/span[1]/span/label[1]').text
    total_pages = int(total_pages)
    current_page = int(current_page)
    ic(total_pages, current_page)
    
    if start_page > current_page:
        current_page = start_page
    ic(current_page)
    # 跳转到第几页
    driver.find_element(By.XPATH, '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[5]/div/div/div[3]/span[2]/input').send_keys(Keys.END, Keys.BACK_SPACE)
    driver.find_element(By.XPATH, '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[5]/div/div/div[3]/span[2]/input').send_keys(current_page)
    driver.find_element(By.XPATH, '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[5]/div/div/div[3]/span[2]/a').click()
    time.sleep(5)
    # 开始采集
    url_list = []
    url_list.append('url')
    
    while True:
        try:
            # 查看有几篇文章
            parent = driver.find_element(By.XPATH,
                                        '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[5]/div/div/div[2]/div/div')
            children = parent.find_elements(By.CLASS_NAME, "inner_link_article_item")
            count = len(children)
            ic(count)
            if count <= 0:
                break
            
            for i in range(count):
                href = driver.find_element(By.XPATH,
                    '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[5]/div/div/div[2]/div/div/label[{}]/div/div[2]/span[2]/a'.format(i+1)
                    )
                url = href.get_attribute("href")
                ic(url)
                url_list.append(url)
            
            if current_page >= total_pages:
                # 保存csv
                data_file = "data\{}_p{}.csv".format(nickname, current_page)
                ic(data_file)
                with open(data_file, "a") as f:
                    f.write("\n".join(url_list))
                break
            
            # 点击下一页 
            current_page += 1
            ic(current_page)
            driver.find_element(By.XPATH, '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[5]/div/div/div[3]/span[2]/input').send_keys(Keys.END, Keys.BACK_SPACE)
            driver.find_element(By.XPATH, '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[5]/div/div/div[3]/span[2]/input').send_keys(current_page) 
            driver.find_element(By.XPATH, '//*[@id="vue_app"]/div[2]/div[1]/div/div[2]/div[2]/form[1]/div[5]/div/div/div[3]/span[2]/a').click()
            
            time.sleep(5+current_page%5)
        except:
            # 保存csv
            data_file = "data\{}_p{}.csv".format(nickname,current_page)
            ic(data_file)
            with open(data_file, "a") as f:
                f.write("\n".join(url_list))
            break


def get_url_title(html):
    lst = []
    for item in driver.find_elements_by_class_name("my_link_item"):
        temp_dict = {
            "date": item.text.split("\n")[0],
            "url": item.find_element_by_tag_name("a").get_attribute("href"),
            "title": item.text.split("\n")[1],
        }
        lst.append(temp_dict)
    return lst


# 用webdriver启动谷歌浏览器
driver = webdriver.Chrome()

nickname = "李继刚"  # 公众号名称
start_page = 0  # 开始页码
ic(login())
ic(open_link(nickname, start_page))
