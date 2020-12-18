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
# df = pd.DataFrame({'圖片':[],'價格':[],'講師':[],"標題":[], "url": [], "星數" : [], "日期" : [], "評論標題" : [], "評論內文" : []})
df = pd.DataFrame({\
"class_title"   : [], \
"class_url"     : [], \
"class_figure"  : [], \
"stars"         : [], \
"teacher_name"  : [], \
"price"         : [], \
"comment_date"  : [], \
"comment_title" : [], \
"comment_text"  : []}) 

target = 'python'
first_url = 'https://hahow.in/courses?search='+target

# Define total page
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
n_class = 0
while (page < total_page ):
    page += 1
    url = 'https://hahow.in/courses?search=python&page='+str(page)
    mydriver0 = webdriver.Chrome(chromedriver_path , options=chrome_options)
    gettingurl0 = mydriver0.get(url)  #
    print("資料爬起來! >>> 第"+str(page)+"/"+str(total_page)+"頁：")
    time.sleep(3)
    source = mydriver0.page_source
    soup = BeautifulSoup(source, 'html.parser')
    class_block = soup.find_all('div',{'class':'sc-10r5mg2-0 fVNHJD hh-course-brief relative block'})  # 在ＧＤ上跑，最後面需要空格（我不知道為什麼）
    for class_ in class_block :
        n_class+=1
        class_href = class_.find('div','cover-wrap relative').find('a')
        class_url ='https://hahow.in'+ class_href.get('href')
        mydriver1 = webdriver.Chrome(chromedriver_path , options=chrome_options)
        gettingurl1 = mydriver1.get(class_url)
        time.sleep(3)
        response_source = mydriver1.page_source
        response_soup = BeautifulSoup(response_source, 'html.parser')  
        title = response_soup.find('h1').text
        if 'Python' in title : # 有符合條件才找
            img = response_soup.find('div',class_='plyr__video-wrapper').find('video')
            # img_url
            img_url = img.get('poster')
            # price
            if response_soup.find('h4',class_='marg-tb-0')  == None and response_soup.find('h1',class_='price') == None :
                price = response_soup.find('h2').text
            elif response_soup.find('div',class_='text-sm marg-tb-0') == None and response_soup.find('div',class_='proposal-pricing') == None :
                price = response_soup.find('h1',class_='price').text
            else:
                price = response_soup.find('h4',class_='marg-tb-0').text      
            # teacher_name  
            teacher_data = response_soup.find_all('div',class_='sc-1l1teqs-0 iFCjAI')
            for teacher in teacher_data:
                teacher_list = teacher.text
                if '老師' in teacher_list :
                    teacher_name = teacher_list[5:]

            url_feedback = class_url +'/feedbacks'
            mydriver2 = webdriver.Chrome('chromedriver', options=chrome_options)
            gettingurl2 = mydriver2.get(url_feedback)
            time.sleep(3)

            haveButton = True
            n_press = 0
            while haveButton == True:
                try: # when there is the continue button
                    actions = ActionChains(mydriver2)
                    seeMoreButton = mydriver2.find_elements_by_xpath("//button[@class='sc-1a6j6ze-0 cYdxxq b21euj-2 gMMXlv']")[0] # 看更多
                    actions.click(seeMoreButton)
                    n_press+=1
                    actions.perform()
                    time.sleep(3)
                except:
                    haveButton = False 
            # After pressing button 'n_press' times ...
            source2 =  mydriver2.page_source
            soup2 = BeautifulSoup(source2, 'html.parser')            
            comments = soup2.find_all('div',{'class':'wei2cc-1 gUylJK marg-b-25'})
            count = 0 # reinitialize nc
            stars = []; dates = []; shortTitles = []; longComments = []
            for comment in comments:
                count+=1
                starRating = comment.find('p',{'class':'marg-b-0'})
                rating = comment.find('div',{'class':'star-ratings'})
                star = rating.attrs['title']
                date = comment.find('time').text
                shortTitle = comment.find('p',{'class':'text-strong marg-b-5'}).text
                longComment = comment.find('p',class_='marg-b-0').text
                stars.append(star)
                dates.append(date)
                shortTitles.append(shortTitle)
                longComments.append(longComment)
            if count!=0: # 如果有搜到評論 
                df_of_1_course = pd.DataFrame({\
                                   "class_title"   : title, \
                                   "class_url"     : class_url, \
                                   "class_figure"  : img_url, \
                                   "stars"         : stars, \
                                   "teacher_name"  : teacher_name, \
                                   "price"         : price, \
                                   "comment_date"  : dates, \
                                   "comment_title" : shortTitles, \
                                   "comment_text"  : longComments}) 
                # update the dataframe
                df = df.append(df_of_1_course, ignore_index = True) 
            print('---第'+str(n_class)+'筆------按了'+str(n_press)+'次------收錄'+ str(count)+ '個評論-----------') 
            mydriver2.quit() 
        else:
            print('---第'+str(n_class)+'筆-----課程名稱沒有'+target)
        mydriver1.quit() 
    mydriver0.quit()

current_date = datetime.datetime.now().strftime ('%d%b%Y-%H%M%S')
current_folder = Path('.')
csv_name = 'Comments_'+str(current_date)+'.csv'
path_to_file = current_folder / 'output' / csv_name 
df.to_csv(path_to_file)
print("file saved: " + str(path_to_file))
