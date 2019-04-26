#!/usr/bin/python
# -*- coding: utf-8 -*-


from selenium import webdriver

driver_path = r'/usr/local/bin/chromedriver'

driver = webdriver.Chrome(executable_path=driver_path)

driver.get('https://www.google.com/')

kw = driver.find_element_by_name('q')

kw.send_keys('python')

su = driver.find_element_by_name('btnK')

su.submit()



print(driver.page_source)
