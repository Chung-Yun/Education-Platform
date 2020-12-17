import os
from pathlib import Path # for file saving
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd
import datetime

# Chrome driver setup 
# Make sure you have already the driver in your $PATH.
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
if chromedriver_path ==None:
    chromedriver_path = 'chromedriver'

# initialise dataframe
df = pd.DataFrame({"標題":[], "url": [], "星數" : [], "日期" : [], "評論標題" : [], "評論內文" : []})

# Define total page
first_url = 'https://hahow.in/courses?search=python'
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
total_page = findTotalPage(first_url)

page = 0
while (page < total_page ):
    page += 1
    url = 'https://hahow.in/courses?search=python&page='+str(page)
    mydriver = webdriver.Chrome(chromedriver_path , options=chrome_options)
    gettingurl = mydriver.get(url)
    print("資料爬起來! >>> 第"+str(page)+"/"+str(total_page)+"頁：")
    time.sleep(3)
    source = mydriver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    class_block = soup.find_all('div',{'class':"sc-10r5mg2-0 fVNHJD hh-course-brief relative block"}) 
    for class_ in class_block :
        #print(class_)
        class_href = class_.find('div','cover-wrap relative').find('a')
        class_url ='https://hahow.in'+ class_href.get('href')
        class_img = class_.find('div', {'class':'cover-image-wrap relative'}).find('img')
        if class_img!= None and class_img.has_attr('src'):
            print(class_img['src'])
        response = mydriver.get(class_url)
        time.sleep(3)
        response_source = mydriver.page_source
        response_soup= BeautifulSoup(response_source, 'html.parser')
        title = response_soup.find('h1').text
        print(title)
        #print(class_img)
        #print(class_url)
        if 'Python' in title :
            seeMoreButton = mydriver.find_elements_by_xpath("//button[@class='sc-1a6j6ze-0 cYdxxq b21euj-2 gMMXlv']")
            if len(seeMoreButton) != 0 :
                press = seeMoreButton[0]
                press.click()
            comments= response_soup.find_all('div',class_='wei2cc-1 gUylJK marg-b-25')

            # Initialisation
            count = 0
            stars = []; dates = []; shortTitles = []; longComments = []
            for comment in comments :
                #print('-----------'+ str(count)+ '-----------')                
                rating = comment.find('div',{'class':'star-ratings'})
                star = rating.attrs['title']
                date = comment.find('time').text
                shortTitle = comment.find('p',{'class':'text-strong marg-b-5'}).text
                longComment = comment.find('p',class_='marg-b-0').text
                #print(stars, course_time, shortTitle)
                #print(longComment.strip())
                stars.append(star)
                dates.append(date)
                shortTitles.append(shortTitle)
                longComments.append(longComment)
                count += 1
            if count!=0:
                df_of_1_course = pd.DataFrame({"標題": title, \
                                   "url": class_url, \
                                   "星數" : stars, \
                                   "日期" : dates, \
                                   "評論標題" : shortTitles, \
                                   "評論內文" : longComments} )
                # update the dataframe
                df = df.append(df_of_1_course, ignore_index = True) 
            print('--------收錄'+ str(count)+ '個評論-----------') 
    mydriver.quit()


current_date = datetime.datetime.now().strftime ('%d%b%Y-%H%M%S')
current_folder = Path('.')
csv_name = str(page)+'page_result_'+str(current_date)+'.csv'
path_to_file = current_folder / csv_name 
df.to_csv(path_to_file)


