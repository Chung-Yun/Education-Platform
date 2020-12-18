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


def findTotalPage(my_url):
    """ Calculates the total page of the search """
    driver = webdriver.Chrome(chromedriver_path, options=chrome_options)
    page = driver.get(my_url)
    time.sleep(3) 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    page_block = soup.find_all('ul',{'class':"rc-pagination gbga9a-0 jYLVph"})
    assert len(page_block)==1
    pages_plus_arrows = page_block[0].find_all('li') # 這邊會多算兩個箭頭
    driver.quit()
    return len(pages_plus_arrows) - 2

def findPrice(my_soup):
    """ Drinks the soup and finds the price of the course"""
    the_price = 'None'
    if my_soup.find('h4',class_='marg-tb-0')  == None and my_soup.find('h1',class_='price') == None :
        the_price = my_soup.find('h2').text
    elif my_soup.find('div',class_='text-sm marg-tb-0') == None and my_soup.find('div',class_='proposal-pricing') == None :
        the_price = my_soup.find('h1',class_='price').text
    else:
        the_price = my_soup.find('h4',class_='marg-tb-0').text 
    return the_price

def findTeacher(my_soup):
    """ Drinks the soup and finds out who teaches the course"""
    teacher_data = my_soup.find_all('div',class_='sc-1l1teqs-0 iFCjAI')
    the_teacher_name = 'None'
    for teacher in teacher_data:
        teacher_list = teacher.text
        if '老師' in teacher_list :
            the_teacher_name = teacher_list[5:]
    return the_teacher_name

def rollOutThePage(my_driver):
    """ Presses "看更多" button until we see the end of the page
        then returns the number of times that the button is pressed 
    :param my_driver: selenium driver that is loading the page
    """
    haveButton = True
    n_press = 0
    while haveButton == True:
        try: # when there is the continue button
            actions = ActionChains(my_driver)
            seeMoreButton = my_driver.find_elements_by_xpath("//button[@class='sc-1a6j6ze-0 cYdxxq b21euj-2 gMMXlv']")[0] 
            actions.click(seeMoreButton)
            n_press+=1
            actions.perform()
            time.sleep(3)
        except:
            haveButton = False
    print('pressed '+str(n_press)+' times')

def crawlFeedbackPage(my_url):
    """ Crawls the feedback page and return number of comments found and their info """
    url_feedback = my_url +'/feedbacks'
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    gettingurl = driver.get(url_feedback)
    time.sleep(3)

    rollOutThePage(driver)

    soup = BeautifulSoup(driver.page_source, 'html.parser')            
    comments = soup.find_all('div',{'class':'wei2cc-1 gUylJK marg-b-25'})
    count = 0 
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
    driver.quit()
    return count, stars, dates, shortTitles, longComments 

def updateDataFrame(my_df, title,class_url,img_url,stars,teacher_name,price,dates,shortTitles,longComments):
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
    # add to the existing dataframe
    my_df = my_df.append(df_of_1_course, ignore_index = True) 
    return my_df

def crawlCoursePage(my_df,course):
    class_href = course.find('div','cover-wrap relative').find('a')
    class_url ='https://hahow.in'+ class_href.get('href')
    driver = webdriver.Chrome(chromedriver_path , options=chrome_options)
    gettingurl = driver.get(class_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')  
    title = soup.find('h1').text

    if 'Python' in title: 

        img = soup.find('div',class_='plyr__video-wrapper').find('video')
        img_url = img.get('poster')

        price = findPrice(soup)

        teacher_name = findTeacher(soup)

        count, stars, dates, shortTitles, longComments = crawlFeedbackPage(class_url)

        if count!=0: # if there is any comments found
            my_df = updateDataFrame(my_df, title,class_url,img_url,stars,teacher_name,price,dates,shortTitles,longComments)
            print('---------收錄'+ str(count)+ '個評論-----------') 
        else:
            print('---------此課程還沒有評論-----------')
    else:
        print('---------沒有需要爬此課程-----------')
    driver.quit()
    return my_df


def allCommentResearch(my_target):
    # initialise dataframe
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

    search_page_url = 'https://hahow.in/courses?search='+my_target

    total_page = findTotalPage(search_page_url)
    page = 0
    n_class = 0
    while (page < total_page):
        page += 1
        url = 'https://hahow.in/courses?search=python&page='+str(page)
        driver = webdriver.Chrome(chromedriver_path , options=chrome_options)
        gettingurl = driver.get(url)  
        print("資料爬起來! >>> 第"+str(page)+"/"+str(total_page)+"頁：")
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        class_block = soup.find_all('div',{'class':'sc-10r5mg2-0 fVNHJD hh-course-brief relative block'}) # might need (or not) a blank space at the end of 'class' 
        for class_ in class_block :
            df = crawlCoursePage(df,class_)
            n_class+=1
            
        driver.quit()
    return df

def saveDataframe(df):
    """ Saves the dataframe into csv format with a timestamp in the current folder """
    current_date = datetime.datetime.now().strftime ('%d%b%Y-%H%M%S')
    current_folder = Path('.')
    csv_name = 'Comments_'+str(current_date)+'.csv'
    path_to_file = current_folder / csv_name 
    df.to_csv(path_to_file)
    print("file saved: " + str(path_to_file))


def main():
    target = 'python'
    my_dataframe = allCommentResearch(target)
    saveDataframe(my_dataframe)

if __name__ == "__main__":
    main()
