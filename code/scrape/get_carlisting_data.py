#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 15:35:46 2017

@author: Jin
"""

# Author: Jin Zhang

from __future__ import print_function, division

import requests
from bs4 import BeautifulSoup
import re
import pprint
import json
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

import time

import os

chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)


# import link data
linkfile = './data/car_urls.txt'
with open(linkfile) as f:
    car_link_list = f.readlines()

# get unique car link
car_link_list = sorted(list(set([link.strip() for link in car_link_list])))
print(len(car_link_list))
print(car_link_list[:5])


# scrape carfax links


counter = 0
car_given_list = car_link_list[16348:]

for car_link in car_given_list:
    counter += 1
    print('Current URL is:' + car_link)
    
    driver.get(car_link)

    vin = re.search(r"listing/(\w+)/", car_link).group(1)
    
    # save html file
    filename = './data/car_listing/'+ vin +'.txt'
    with open(filename, "w") as text_file:
        text_file.write(driver.page_source)
    
    driver.implicitly_wait(100)
    
    if driver.title != 'Error':

        # get carfax link information]
        has_element = True
        for i in range(10):
            try:
                link_element = driver.find_element_by_xpath("//img[@class ='logo_morn4t']//preceding-sibling::a")
                
                break
            except StaleElementReferenceException as e:
                print('StaleElementReferenceException occurs', i+1, ' times')
            except NoSuchElementException:
                has_element = False
                break
        if has_element:
            carfax_link = link_element.get_attribute("href")
            carfax_link_desc = 1 if 'Free' in link_element.find_element_by_xpath(".//span").text else 0

            ## save carfax link to file

            carfax_link_file = './data/carfax_urls.txt'

            if os.path.isfile(carfax_link_file):
                carfax_file = open(carfax_link_file, 'a')
            else:
                carfax_file = open(carfax_link_file, 'w')

            carfax_file.write(vin + ' ' + str(carfax_link_desc) + ' ' + carfax_link + '\n')
            carfax_file.close()
        print('Can find the carfax link:' , has_element)
        print('Finished scraping car listing for car with vin: ' + vin)
        print('Finished scraping ', counter, ' cars.')
        print('------------------------------------------------------')
    
    else:
        print('This page does not exists!')
        print('Finished scraping car listing for car with vin: ' + vin)
        print('Finished scraping ', counter, ' cars.')
        print('------------------------------------------------------')

    
    


    
    
    