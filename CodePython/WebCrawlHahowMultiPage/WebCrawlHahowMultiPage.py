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
if os.environ.get("CHROMEDRIVER_PATH")==None:
    mydriver = webdriver.Chrome('chromedriver', options=chrome_options)
else: 
    mydriver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)


page = 0
df = pd.DataFrame({"標題":[], "url": [], "星數" : [], "日期" : [], "評論標題" : [], "評論內文" : []})

while (page < 1):
    page += 1
    url = 'https://hahow.in/courses?search=python&page='+str(page)
    gettingurl = mydriver.get(url)
    print("資料爬起來! >>> 第"+str(page)+"頁：")
    time.sleep(3)
    source = mydriver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    #print(soup.prettify())
    class_block = soup.find_all('div',{'class':"sc-10r5mg2-0 fVNHJD hh-course-brief relative block"}) 
    #print(class_block)
    for class_ in class_block :
        #print(class_)
        class_href = class_.find('div','cover-wrap relative').find('a')
        class_url ='https://hahow.in'+ class_href.get('href')
        class_img = class_.find('div', {'class':'cover-image-wrap relative'}).find('img')
        #print(class_.find('div', {'class':'cover-image-wrap relative'}))
        if class_img!= None and class_img.has_attr('src'):
          print(class_img['src'])
        # if class_img!= None and class_img.has_attr('alt'): # another way to find title
        #  print(class_img['alt'])
        response = mydriver.get(class_url)
        time.sleep(3)
        response_source = mydriver.page_source
        response_soup= BeautifulSoup(response_source, 'html.parser')
        #title = response_soup.find('h1',{'class':'title text-center'}).text
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

current_date = datetime.datetime.today().strftime ('%d-%b-%Y')
current_folder = Path('.')
csv_name = str(page)+'page_result_'+str(current_date)+'.csv'
path_to_file = current_folder / csv_name 
df.to_csv(path_to_file)

mydriver.quit()


