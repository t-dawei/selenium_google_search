#!/usr/bin/python
# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
# 使用无头谷歌浏览器模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver_path = r'/usr/local/bin/chromedriver'
driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)
# driver = webdriver.Chrome(executable_path=driver_path)
# 隐式等待 设置一次 全局有效
driver.implicitly_wait(10)
locator = (By.ID, 'search')


'''
只请求英文结果
https://www.google.com/search?hl=en&q=google
hl 是语言
q 是字段
'''

'''
存在问题：
    采用无头模式会导致请求网页中文乱码
    selenium 解析网页 容错较差 不如bs4
'''


def search(ls_keyword):

    try:
        driver.get('https://www.google.com/search?hl=en&q=google')
        for keyword in ls_keyword:
            kw = driver.find_element_by_name('q')
            su = driver.find_element_by_class_name('Tg7LZd')
            kw.clear()
            kw.send_keys(keyword)
            su.click()
            results = extractResultsByBs4(driver.page_source.encode('UTF-8').decode())
            print(keyword)
            print(results)
    except Exception as e:
        print(e)
    finally:
        driver.quit()


def extractResultsByBs4(html):

    results = []
    try:
        soup = BeautifulSoup(html, 'html.parser')
        search = soup.find('div', id='search')
        if search:
            lis = search.findAll('div', {'class': 'g'})
            for li in lis:
                out = {}
                rc = li.find('div', {'class': 'rc'})
                if rc:
                    h3 = rc.find('h3', {'class': 'LC20lb'})
                    if not h3:
                        continue
                    out["name"] = h3.getText()

                    link = rc.find('a')
                    out["url"] = link.get('href') if link else ''

                    span = rc.find('span', {'class': 'st'})
                    out["snippet"] = span.getText() if span else ''
                results.append(out)
    except Exception as e:
        print(e)

    return results



def search_Bylink(ls_keyword):

    base_url = 'https://www.google.com/search?q='
    try:
        for keyword in ls_keyword:
            driver.get(base_url + keyword)
            # print(driver.page_source)
            elment = WebDriverWait(driver, 5, 1).until(
                EC.presence_of_element_located(locator)
            )
            results = extractResultsByselenium(elment)
            print(keyword)
            print(results)
    except Exception as e:
        print(e)
    finally:
        driver.quit()


'''
find_elements_by_class_name --- 没有返回空
find_element_by_class_name --- 没有抛出异常
容错性差
'''
def extractResultsByselenium(elment):
    results = []
    try:
        lis = elment.find_elements_by_class_name('g')
        for li in lis:
            out = {}
            # rc 可能不存在
            rc = li.find_elements_by_class_name('rc')
            if rc:
                # h3 可能不存在
                h3 = rc[0].find_elements_by_class_name('LC20lb')
                if h3:
                    out["name"] = h3[0].text

                # link 是否一定存在
                link = rc[0].find_elements_by_tag_name('a')
                if link:
                    out["url"] = link[0].get_attribute('href') if link else ''

                # span 可能不存在
                span = rc[0].find_elements_by_class_name('st')
                if span:
                    out["snippet"] = span[0].text if span else ''
            results.append(out)
    except Exception as e:
        print(e)


    return results


if __name__ == '__main__':
    # 方法1：（隐式等待 + bs4） + 输入框输入搜索
    search(['Google', 'Huawei', 'Apple'])

    # 方法2：（显式等待 + bs4）+ 链接构造搜索
    # search_Bylink(['google', 'Huawei', 'Apple'])