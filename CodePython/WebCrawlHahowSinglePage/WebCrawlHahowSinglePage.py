import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

# Chrome driver setup 
# Make sure you have already the driver in your $PATH.
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
mydriver = webdriver.Chrome('chromedriver', options=chrome_options)

# URL of our pick
url = 'https://hahow.in/courses/5d77176845639e00212bc562/main'
gettingurl = mydriver.get(url)
print("URL get!")
time.sleep(3)
source = mydriver.page_source

# Parse it with bs4
soup = BeautifulSoup(source, 'html.parser')

classTitle1 = soup.body.div.div.main.div.div.div.h1

print("Raw output: " + str(classTitle1))
print("Without tag: " + classTitle1.text)

classTitle2 = soup.find('h1',{'class':"title text-center"})
print("Raw output: " + str(classTitle2))
print("Without tag: " + classTitle2.text)

aboutCourseTitle = soup.find('div',{'class':'sc-1l1teqs-0 iFCjAI'})
aboutCourse = soup.find('pre',{'class':'sc-1l1teqs-2 iOONJS'}).find_all('div')

print(aboutCourseTitle.text)
for tt in aboutCourse:
    print(tt)

mydriver.quit()

