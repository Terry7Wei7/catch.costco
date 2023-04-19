import os
import re
import time
import requests
#import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import ssl
import urllib3
from time import sleep
urllib3.disable_warnings()
#ssl證書
os.environ['WDM_SSL_VERIFY']='0'
if __name__ == '__main__':
    #可調整頁面滾動次數
    scroll_time = 5
    driver = webdriver.Chrome()
    # 最大化視窗
    driver.maximize_window()
    driver.get('https://www.facebook.com/groups/1260448967306807')
    sleep(1)
    for now_time in range(1, scroll_time+1):
        sleep(2)
        print(f"now scroll {now_time}/{scroll_time}")
        driver.implicitly_wait(10)
        total_page_height = driver.execute_script("return document.body.scrollHeight")
        browser_window_height = driver.get_window_size(windowHandle='current')['height']
        current_position = driver.execute_script('return window.pageYOffset')
        while total_page_height - current_position > browser_window_height:
            driver.execute_script(f"window.scrollTo({current_position}, {browser_window_height + current_position});")
            current_position = driver.execute_script('return window.pageYOffset')
            sleep(1)  # It is necessary here to give it some time to load the content
root = BeautifulSoup(driver.page_source, "html.parser")
# 定位文章標題
titles = root.find_all(
    "div", class_="x1iorvi4 x1pi30zi x1swvt13 x1l90r2v")
for title in titles:
    # 定位每一行標題
    posts = title.find_all("div", dir="auto")
    # 如果有文章標題才印出
    if len(posts) != 0:
        for post in posts: 
            file = open("Costco_Get_title.txt", "a", encoding="utf-8")
            file.write(post.text+"\n") 
            #file.write("-" * 30+"\n")    
            print(post.text)
    print("-" * 30)
    #file.write("-" * 30+"\n")
    #file.close()
# 定位文章留言
messages = root.find_all(
    "div", class_="x1y1aw1k xn6708d xwib8y2 x1ye3gou")
for message in messages:
    # 定位每一行標題
    posts = message.find_all("div", dir="auto")
    # 如果有文章留言才印出
    if len(posts) != 0:
        for post in posts:
            file = open("Costco_Get_message.txt", "a", encoding="utf-8")
            file.write(post.text+"\n")          
            print(post.text)
    print("-" * 30)
    file.write("-" * 30+"\n")
    #file.close()
# 建立資料夾
if not os.path.exists("images"):
    os.mkdir("images")
# 下載圖片
images = root.find_all(
    "img", class_=["x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r"])
if len(images) != 0:
    for index, image in enumerate(images):
        img = requests.get(image["src"])
        with open(f"images/img{index+1}.jpg", "wb") as file:
            file.write(img.content)
        print(f"第 {index+1} 張圖片下載完成!")
# 等待5秒
time.sleep(5)
# 關閉瀏覽器
#driver.quit()
