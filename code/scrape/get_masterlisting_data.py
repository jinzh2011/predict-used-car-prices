
# coding: utf-8

# Author: Jin Zhang

# setup 

from __future__ import print_function, division

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import os



chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

driver = webdriver.Chrome(chromedriver)



# setup
master_url = 'https://www.truecar.com/used-cars-for-sale/listings/location-94040/?searchRadius=75&sortOrder=PRICE_DESC'
car_url_list= []

# load first page
driver.get(master_url)

# get last page's link
for i in range(10):
        try:
            last_page_url = driver.find_element_by_xpath("//span[@aria-label='Last']/ancestor::a").get_attribute("href")
            break
        except StaleElementReferenceException as e:
            print('StaleElementReferenceException occurs', i+1, ' times')
            

print('last page has link: ', last_page_url)


# loop process from first page to last page

## setup for loop
current_url = master_url
counter = 0

#for i in range(20):
    
while (True):
    
    counter += 1
    print('Current URL is:' + current_url)
    
    driver.get(current_url)

    # save html file
    filename = './data/master_listing/'+ str(counter)+'.txt' 

    with open(filename, 'w+') as f:
        f.write(driver.page_source)

    driver.implicitly_wait(100)

    # scrape links of indivisual car listings
    for i in range(10):
        try:
            link_element = driver.find_elements_by_xpath("//a[@class='vdp-link']")
            break
        except StaleElementReferenceException as e:
            print('StaleElementReferenceException occurs', i+1, ' times')

    print('This page has ', len(link_element), 'car listings.')
    
    ## save links to txt files
    linkfile_path = './data/car_urls.txt'
    if os.path.isfile(linkfile_path):
        carfile = open(linkfile_path, 'a')
    else:
        carfile = open(linkfile_path, 'w')
        
    for item in link_element:
        item_url = item.get_attribute("href")
        car_url_list.append(item_url)
        carfile.write("%s\n" % item_url)
    carfile.close()

    if current_url != last_page_url:
        # click to next page
        for i in range(10):
            try:
                current_url = driver.find_element_by_xpath("//span[@aria-label='Next']/ancestor::a").get_attribute("href")
                break
            except StaleElementReferenceException as e:
                print('StaleElementReferenceException occurs', i+1, ' times')


        print('Finished scraping page ' + str(counter) + ' of master listings')
        print('Updated next URL is:' + current_url)
        print('------------------------------------------------------')
    
    else:
        print('Finished scraping page ' + str(counter) + ' of master listings')
        print('This is the last page of URL:' + current_url)
        break
    




print(len(car_url_list))
print('unique numbers of cars:', len(set(car_url_list)))
print(car_url_list[:5])



