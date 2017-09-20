# coding: utf-8

#combine data

from __future__ import print_function, division
import requests
from bs4 import BeautifulSoup
import re
import pprint
import json
import os
import pandas as pd

# combine master listing data

master_path = './data/master_listing/'
master_file_list = [master_path+f for f in os.listdir(master_path) if f.endswith('.txt')]

master_dict = {}
counter = 0
for file in master_file_list:
    counter += 1
    print(counter, file)
    script_list = []
    soup = BeautifulSoup(open(file, 'r+'),'lxml')

    for icon in soup.find_all('script'):
        if 'window.__INITIAL_STATE__=' in icon.text:
            script_list.append(icon.text)
    assert len(script_list) == 1
    js_script = script_list[0]
    json_text_list = list(filter(lambda x: 'window.__INITIAL_STATE__=' in x,                                  js_script.replace('&amp;','&').replace('&#38;','&').split(';')))
    assert len(json_text_list) == 1
    json_text = json_text_list[0].replace('window.__INITIAL_STATE__=','')
    data_dict = json.loads(json_text)
    
    for item in data_dict['searchVehicles']:
        if item['vin'] not in master_dict:
            master_dict[item['vin']] = item
    

# save master listing 
master_json_file = './data/consolidated/master_listing.json'
with open(master_json_file, 'w') as fp:
    json.dump(master_dict, fp)


# combine individual car listing data
car_path = './data/car_listing/'
car_file_list = [car_path+f for f in os.listdir(car_path) if f.endswith('.txt')]

car_listing_dict = {}
counter = 0
    
for file in car_file_list:
    counter += 1
    print(counter, file)
    soup = BeautifulSoup(open(file, 'r+'),'lxml')
    
    # vin is None if the page is empty
    vin = soup.find('li', { 'data-qa' : 'VehicleDetails-vin' }).contents[-2] \
          if soup.find('li', { 'data-qa' : 'VehicleDetails-vin' }) is not None else None 
        
    transmission = soup.find('li', { 'data-qa' : 'VehicleDetails-transmission' }).contents[-2] \
                        if soup.find('li', { 'data-qa' : 'VehicleDetails-transmission' }) is not None else None
        
    engine = soup.find('li', { 'data-qa' : 'VehicleDetails-engine' }).contents[-2] \
                 if soup.find('li', { 'data-qa' : 'VehicleDetails-engine' }) is not None else None
        
    driveTrain = soup.find('li', { 'data-qa' : 'VehicleDetails-drivetrain' }).contents[-2] \
                      if soup.find('li', { 'data-qa' : 'VehicleDetails-drivetrain' }) is not None else None
        
    bodyStyle = soup.find('li', { 'data-qa' : 'VehicleDetails-bodyStyle' }).contents[-2] \
                     if soup.find('li', { 'data-qa' : 'VehicleDetails-bodyStyle' }) is not None else None
    
    
    fuelType = soup.find('li', { 'data-qa' : 'VehicleDetails-fuelType' }).contents[-2] \
                    if soup.find('li', { 'data-qa' : 'VehicleDetails-fuelType' }) is not None else None
        
    mpgCity = soup.find('li', { 'data-qa' : 'VehicleDetails-mpg' }).contents[-8] \
                   if soup.find('li', { 'data-qa' : 'VehicleDetails-mpg' }) is not None else None
        
    mpgHwy = soup.find('li', { 'data-qa' : 'VehicleDetails-mpg' }).contents[-2] \
                  if soup.find('li', { 'data-qa' : 'VehicleDetails-mpg' }) is not None else None
        
    features = soup.find('div', { 'data-qa' : 'DividedList' }).text \
                  if soup.find('div', { 'data-qa' : 'DividedList' }) is not None else None
    
    
    car_listing_dict[vin] = {'transmission': transmission,
                             'engine': engine,
                             'driveTrain': driveTrain,
                             'bodyStyle': bodyStyle,
                             'fuelType': fuelType,
                             'mpgCity': mpgCity,
                             'mpgHwy': mpgHwy,
                             'features': features                         
                            }
    

# save individual car listing data

car_json_file = './data/consolidated/car_listing.json'
with open(car_json_file, 'w') as fp:
    json.dump(car_listing_dict, fp)


