# How I set up my LINE bot

I built a bot for a tiny project. As a noob in programming who has goldfish's memory, I decided to note down my work. Here's how:

>In one sentence: this is a **LINE bot** written in **Python** deployed to **Heroku** and connected to a **MariaDB**.

The note is organised in three sections:

There are three parts in this note: First, there is an introduction on main code of the [LINE Bot](#LINE-Bot) which is written in Python. Then, there are some intstructions on how to deploy the app to [Heroku](#Heroku). Lastly, we can add [Other Functionalities](#Other-Functionalities) to make the bot more powerful, such as: webcrawling and databases.

### Before started

Must have:
- [x] **Line** account
- [x] **Heroku** account
- [x] A computer with **Git** installed.

Not essential but better to have:
- [ ] **Python** installed on your computer (well, I mean you can simply just write the code without testing locally...)
- [ ] **MySQLWorkbench** (make debugging easier)

## LINE Bot
- [Account Creation](#Account-Creation)
- [Basic Setup](#Basic-Setup)
- [The Code](#The-Code)

### Account Creation
1. You need to have a LINE account.
2. Go to the [LINE developers page](https://account.line.biz/login?redirectUri=https%3A%2F%2Fdevelopers.line.biz%2Fconsole%2F) and sign in with your LINE account (the same one).

|![](https://i.imgur.com/nQqlex7.png) |![](https://i.imgur.com/YkSxceG.png)|![](https://i.imgur.com/Qol5BCI.png)|
|:---:|:---:|:---:|

3. Create a **provider**.
4. Create a **messenging API channel**. We will need to fill out the following informations:
    1. Channel type : Messenging API 
    2. Provider : The one you just created for example.
    3. Channel icon (optional)
    4. Channel name (the name of your bot)
    6. Channel description
    7. Category (scrolling list)
    8. Subcategory (scrolling list)
    9. Email address
    10. Privacy policy URL (optional)
    11. Terms of use URL (optional)
    12. [LINE Official Account Terms of Use](https://terms2.line.me/official_account_terms_tw?lang=zh-Hant)
    13. [LINE Official Account API Terms of Use](https://terms2.line.me/official_account_api_terms_tw?lang=zh-Hant)
    
5. There wil be additional privacy agreement that you need to agree to.

|![](https://i.imgur.com/OOfCWhn.png)| ![](https://i.imgur.com/wLf2jN2.png) | ![](https://i.imgur.com/Mpfnb8n.png) |
|:---:|:---:|:---:|


After these steps, we have created a LINE account for our LINE bot.
### Basic Setup

- [Secret Keys](#Secret-Keys)
- [Modifiable Features](#Modifiable-Features)

#### Secret Keys

There are two impotant keys that we note down for [later use](#Hiding-the-Keys): 
1. Channel secret
    - You can find this key under **basic settings**
2. Channel access token
    - You can find this key under **Messenging API** click on **issue** if it is not generated yet.

The keys are high secret and should not be communicated to anyone else.

#### Modifiable Features

The following is my setting for my line bot, these are optional. Do whatever that suites your need.

| | Default | My Choice |
|-|-|-|
| Allow bot to join group chats | Disabled | Enable | 
| Auto-reply messages | Enable | Disabled | 
| Greeting messages | Enable | Disabled | 

>You can change your these features (including app name and icon) in LINE Official Account Manager 
>```=url
>https://manager.line.biz/account/{YOUR-BOT-BASIC-ID}/setting
>```
>YOUR-BOT-BASIC-ID
>: It can be found under Messaging API/Messaging API settings/Bot information/Bot basic ID. It is a sequence of number and letter that starts with an @.


### The Code
There are three [examples](line-bot-sdk-python/examples/) on the GitHub repository, line/line-bot-sdk-python, when I write this note. I started from downloading one of them and make changes to it.

Here is an minimalist example of an echo bot that repeat whatever it receives as a message. We create a file named *app<i></i>.py*, which is the main file of the application. Inside, we can write:

##### app<i></i>.py 
```python=
from decouple import config
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler 
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__) # This is a Flask app.

# get KEYS from your environment variable
channel_secret = config('LINE_CHANNEL_SECRET')
channel_access_token = config('LINE_CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text))
     

if __name__ == "__main__":
    app.run()
```


###### Hiding the Keys
This piece of code will work if you simply replace **config(LINE_CHANNEL_SECRET)** and **config(LINE_CHANNEL_ACCESS_TOKEN)** with the keys that we noted [previously](#Secret-Keys). However, it is not safe to hard code your secrets inside the script.

> If someone knows the two keys, they are able to create a app using those keys and do goofy stuff in the name of your LINE bot.

There exists several methods to hide keys and one can choose whatever they are used to. Here, we import the function **config** from **decouple** and the variable are saved in a file named *.env*. When running the app, the varaibles defined in *.env* becomes temporary environment variables. The function **config** searches the variables from the environment and the application can make use of the variables.

A typical **.env** file looks like:
```shelle = zsh
LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN_HERE
LINE_CHANNEL_SECRET=Your_LINE_CHANNEL_SECRET_HERE
```

#### Test Things Locally

Once everything mentioned in this section is set and if Python is installed locally, we can test the application locally.
```shell=zsh
python app.py
```
If everthing is installed correctly, the Flask app will start running locally. However when you add your bot as a friend and send messages, it won't reply because the [webhook](https://en.wikipedia.org/wiki/Webhook) is not configured yet. In the next section, we will deploy the app to Heroku.


>### Reference : LINE Bot Basics
>1. [LINE developers website](https://developers.line.biz/zh-hant/reference/messaging-api/)
>1. [Github: line/line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
>1. [[Python Linebot]教你如何使用Python成功串接Linebot(2020版)](https://medium.com/@zx2515296964/python-linebot-%E6%95%99%E4%BD%A0%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8python%E6%88%90%E5%8A%9F%E4%B8%B2%E6%8E%A5linebot-2020%E7%89%88-c98672eec44e) (Mandarin)


## Heroku

Some [additional files](#Additional-Files) are required before [deploying to Heroku](#Deploy-to-Heroku). Once the app is up and running on Heroku, we can [configure the Webhook](#Configure-Webhook) at LINE developers website.

### Additional Files
When deploying to the cloud, you may need some additional files.

- [requirements.txt](#1.-requirements.txt) 
- [runtime.txt](#2.-runtime.txt)
- [Procfile](#3.-Procfile)

#### 1. requirements.txt

The *requirements.txt* file to tell Heroku the dependencies that you need for the app.

For the aformentioned example, the *requirements.txt* file may look like:
```=requirements.txt
certifi==2020.12.5
chardet==4.0.0
click==7.1.2
decouple==0.0.7
Flask==1.1.2
future==0.18.2
gunicorn==20.0.4
idna==2.10
itsdangerous==1.1.0
Jinja2==2.11.2
line-bot-sdk==1.18.0
MarkupSafe==1.1.1
requests==2.25.1
urllib3==1.26.2
Werkzeug==1.0.1
```

I am using [pipenv](https://pypi.org/project/pipenv/) in my Python workflow and I use it to generate *requirements.txt*.

#### 2. runtime.txt

The *runtime.txt* file tells heroku which python version we want to use. In my case, I wrote:

```=runtime.txt
python-3.6.12
```
>I experienced problems when I want to install numpy and pandas package when I use Python 3.9. So I picked an older Python version.

#### 3. Procfile
The *Procfile* doesn't have any extension! To the file we write the following line:
```=Procfile
web: gunicorn app:app –preload 
```
This [Procfile](https://devcenter.heroku.com/articles/procfile) specifies the commands that are executed by the Heroku app on startup as a web process. 

---------------
Until now, locally we have a folder with the following files inside:

>app<i></i>.py
>: the main application
>
>.env
>: where we hide the keys
>
>requirements.txt
>: indicates the dependencies
>
>runtime.txt
>: specify which python to use
>
>Procfile
>: tells Heroku how to run our app


---------------------

### Deploy to Heroku 

Login to [Heroku](https://dashboard.heroku.com/apps) and **create a new app**.

|![](https://i.imgur.com/Q8ncf4p.png)|![](https://i.imgur.com/hEwoNJK.png)|
|:-:|:-:|

In the dashboard of the Heroku app, there are several tabs:
![](https://i.imgur.com/PsSTGgH.png)
Under *Settings/config vars*, put your **LINE_CHANNEL_ACCES_TOKEN** and  **LINE_CHANNEL_SECRET** here.
> We will not deploy *.env* to Heroku. Instead, we store all the keys here and Heroku can fetch them when the app needs them.

|![](https://i.imgur.com/RwJhaAr.png)|![](https://i.imgur.com/xBZoeh5.png)|
|:-:|:-:|



After configuring the variables, we deploy the local files to Heroku. The following is a step by step guide:
- Download and install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- login to Heroku from the command line
```shell=zsh
heroku login
```
- This will redirect to a webpage for login.
- Create a git repository and link it to the app.
```shell=zsh
cd path_to_project_directory
git init # initialize the directory as a local git repository
heroku git:remote -a {name_of_heroku_app} # link your local git repository to your heroku app
```

- Add a *.gitignore* file to ignore *.env.* file in the same directory. Write the following line in the file.
```=.gitignore
.env
```
- Deploy the files to Heroku.
```shell=zsh
#(in the same directory)
git add . # keep track of all files excluding the one in .gitignore (i.e. .env)
git commit -m "first commit to heroku" # commit with a message
git push heroku master # pushes the files in master branch to heroku
```

>You can also refer to your Heroku app's dashboeard, under *Deploy/Deploy using Heroku Git*, there is a short tutorial on how to deploy your app to Heroku.




### Configure Webhook


The webhook suggested by [LINE Developers website](https://developers.line.biz/zh-hant/docs/messaging-api/building-sample-bot-with-heroku/#%E9%83%A8%E7%BD%B2-kitchensink-%E7%AF%84%E4%BE%8B%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BA-app) is:
```
https://{HEROKU_APP_NAME}.herokuapp.com/callback
```

Replace **HEROKU_APP_NAME** with the app's name then place it into **Messenging API/Webhook settings/Webhook URL** and **update** to see if successfully connects to Heroku.
|![](https://i.imgur.com/eGcsJaY.png)|![](https://i.imgur.com/PY05ThS.png)|
|:-:|:-:|

Now, the app is up running and we can expand our code, keep track of it with git and push changes to Heroku for updates.

>### Reference : Deploy to Heroku
>1. [《Line Bot教學》用 Heroku、Python 建立自己的 Line Bot](https://cruelshare.com/line-bot-second/) (Mandarin)
>1. [LINE:使用 Heroku 建立範例聊天機器人](https://developers.line.biz/zh-hant/docs/messaging-api/building-sample-bot-with-heroku/#%E9%83%A8%E7%BD%B2-echo-%E7%AF%84%E4%BE%8B%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BA) (Mandarin)


## Other Functionalities

### Webcrawling with Selenium

We need additional setup in our app. We can either place this in the app.py or put it in another file and call it as a module.

```python=
from decouple import config
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver

# Chrome driver setup 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chromedriver_path = os.environ.get('CHROMEDRIVER_PATH')

chrome_options.binary_location = config('GOOGLE_CHROME_BIN')
chromedriver_path = config('CHROMEDRIVER_PATH')
```

- If you are running the app locally, you need to configure the *.env* file. Here is an example where I configure the variables on a mac:
```=.env
CHROMEDRIVER_PATH = /usr/local/bin/chromedriver 
GOOGLE_CHROME_BIN = /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome
```
- If you are running the app on Heroku, remember to configure the variables accordingly
```=.env
CHROMEDRIVER_PATH = /app/.chromedriver/bin/chromedriver
GOOGLE_CHROME_BIN = /app/.apt/usr/bin/google-chrome
```
![](https://i.imgur.com/wrFiYzU.png)

These variables tells Heroku where to find Google Chrome and its driver on the cloud server. In addition, we need to provide two **buildpacks** to Heroku. It is under *Settings/Buildpacks*. 

|![](https://i.imgur.com/WNpxP9l.png)|![](https://i.imgur.com/m5qzUSh.png)|
|:-:|:-:|
Click on **Add buildpack** and paste the following links one at a time.

1. [heroku/heroku-buildpack-google-chrome](https://github.com/heroku/heroku-buildpack-google-chrome)
```https://github.com/heroku/heroku-buildpack-google-chrom```
2. [heroku/heroku-buildpack-chromedriver](https://github.com/heroku/heroku-buildpack-chromedriver)
```https://github.com/heroku/heroku-buildpack-chromedrive```

At the end, the screen should look like this picture:
![](https://i.imgur.com/RsMGto0.png)

With these being set, we can write web crawling code with Python using Selenium and run the app on Heroku.

>### Reference : Selenium on Heroku 
>1. [How to deploy python selenium script on Heroku](https://www.youtube.com/watch?v=rfdNIOYGYVI)


### Database with MariaDB

I am using [JawsDB Maria](https://elements.heroku.com/addons/jawsdb-maria) as my database.


At your app's page, under *Resources/Add ons*
|Find JawsDB Maria and choose the free version|![](https://i.imgur.com/2HMsNAt.png)|
|:-:|:-:|
![](https://i.imgur.com/usCg7bC.png)|![](https://i.imgur.com/rsuUeuq.png)|


You can also done this by [using command line](https://devcenter.heroku.com/articles/jawsdb-maria#provisioning-the-add-on).

Our Python application is now connected to MariaDB.
Then, we can find a new variable at *Settings/Config Vars*.
![](https://i.imgur.com/CW8SKhx.png)

Now we decompose the new variable from
```
mysql://username:password@hostname:port/default_schema
```
to

```=.env
MARIA_HOST=hostname
MARIA_USER=username
MARIA_PASSWD=password
MARIA_DB_NAME=default_schema                         
```
add these to *.env* for running the app locally and add these to *Settings/Config Vars* for running the app on Heroku.

![](https://i.imgur.com/4sIXT9V.png)


Meanwhile, in *app<i></i>.py*. I added the [PyMySQL](https://pymysql.readthedocs.io/en/latest/) package. Here is how I define a function that connects our app to our database:

```python=
from decouple import config
import pymysql
import pymysql.cursors
      
def connectToDatabase():
    """ Connects to the database """
    conn = pymysql.connect(host=config('MARIA_HOST'),
                             user=config('MARIA_USER'),
                             password=config('MARIA_PASSWD'),
                             db=config('MARIA_DB_NAME'),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return conn
```

And here is an example of a function that connects to our database, executes some SQL queries, returns the results of the query and closes the connection.
For PyMySQL, the autocommit is off by default. We need to call **commit** to make real changes to the Database.

```python=
def executeQuery(query):
    """ Executes a random sql query and returns the results if there is one 
    :param query <string>: sql query
    """
    conn = connectToDatabase()
    cursor = conn.cursor()
    answer = 'executeQuery start'
    try:
        cursor.execute(query)
        try:
            answer = cursor.fetchall() # will return () is nothing is expected
        except:
            answer = "Not valid"
    except:
        answer = 'ERR: executeQuery not working'
    conn.commit() # commit the change
    conn.close() 
    return answer 
````

We can also turn the SQL result into Pandas DataFrame for more flexible manipulation. For example:
```python=
import pandas as pd
query = "SELECT * FROM orders WHERE user_id = ?"
df = pd.read_sql(query, connection,  params=(USER_ID))
```
or
```python=
def fetchTable2Dataframe(table_name):
    """ Fetches a table and turn it to dataframe
    : param table_name <string>: name of the table in the database
    return type : pandas dataframe 
    """
    conn = connectToDatabase()
    query = "SELECT * FROM " + str(table_name)
    df = pd.read_sql(query, conn) # Transform SQL to Pandas DF
    conn.close() 
    return df
```

Now, the app is able to access to the database for information and modify them.

>### Reference : Cloud Database
>1. [MariaDB for Heroku](https://devcenter.heroku.com/articles/jawsdb-maria#using-jawsdb-maria-with-python-django)
>1. [Tutorial: How to Create a MySQL Database with Heroku](https://www.youtube.com/watch?v=aEm0BN493sU)
>1. [How to deploy Python Flask MySQL based application in Heroku Cloud](https://roytuts.com/how-to-deploy-python-flask-mysql-based-application-in-heroku-cloud/)
>1. [MySQL Data Types](https://www.w3schools.com/sqL/sql_datatypes.asp)



