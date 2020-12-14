import os
import sys
from decouple import config
#from pathlib import Path # for file saving
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
#import pandas as pd
#import datetime

# Chrome driver setup 
# Make sure you have already the driver in your $PATH.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')
#if chrome_options.binary_location is None:
#    print('Specify GOOGLE_CHROME_BIN as environment variable.')
#    sys.exit(1)
#if chromedriver_path  is None:
#    print('Specify CHROMEDRIVER_PATH as environment variable.')
#    sys.exit(1)
chrome_options.binary_location = config('GOOGLE_CHROME_BIN')
chromedriver_path = config('CHROMEDRIVER_PATH')


def findTotalPage(myurl):
    first_driver = webdriver.Chrome(chromedriver_path, options=chrome_options)
    first_page = first_driver.get(myurl)
    time.sleep(3) 
    first_soup = BeautifulSoup(first_driver.page_source, 'html.parser')
    page_block = first_soup.find_all('ul',{'class':"rc-pagination gbga9a-0 jYLVph"})
    assert len(page_block)==1
    pages_plus_arrows = page_block[0].find_all('li') # 這邊會多算兩個箭頭
    first_driver.quit()
    return len(pages_plus_arrows) - 2
