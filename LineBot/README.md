# LINE Bot

We created a LINE bot for this project

## Directory overview

### LineBot V1

A save of the first version of the bot.

### LineBot V2

This version has most of the essential tools to communicate with the data base and the skeleton of our dialog.


 
## Communication with Database

We deployed a tiny cloud database for our bot to store information. There are 5 types of tables in the DB.

### Table Type I

This is mainly our dictionary for comment analysis.


|ID|Type|Representative word|Synonym|
|-|-|-|-|
|int|varchar(50)|varchar(50)|varchar(255)|

### Table Type II

|ID|class_title|class_url|class_figure|stars|teacher_name|price|comment_date|comment_title|comment_text|
|-|-|-|-|-|-|-|-|-|-|
|int|varchar(50)|varchar(255)|varchar(255)|varchar(50)|varchar(50)|varchar(50)|varchar(50)|varchar(50)|varchar(255)|

### Table Type III

|ID|class_title|Keyword1|Keyword2|Keyword3|Keyword4|Keyword5|Keyword6|Keyword7|Keyword8|Keyword9|Keyword10|
|-|-|-|-|-|-|-|-|-|-|-|-|
|int|varchar(50))|varchar(50)|varchar(50)|varchar(50)|varchar(50)|varchar(50))|varchar(50)|varchar(50)|varchar(50)|varchar(50)|varchar(50)|


## 參考資料

### LINE Bot 基礎架構
1. [使用 Heroku 建立範例聊天機器人](https://developers.line.biz/zh-hant/docs/messaging-api/building-sample-bot-with-heroku/#%E9%83%A8%E7%BD%B2-echo-%E7%AF%84%E4%BE%8B%E8%81%8A%E5%A4%A9%E6%A9%9F%E5%99%A8%E4%BA%BA)
1. [How to deploy python selenium script on Heroku](https://www.youtube.com/watch?v=rfdNIOYGYVI)
1. [《Line Bot教學》用 Heroku、Python 建立自己的 Line Bot](https://cruelshare.com/line-bot-second/)
### 架設雲端資料庫
1. [MariaDB for Heroku](https://devcenter.heroku.com/articles/jawsdb-maria#using-jawsdb-maria-with-python-django)
1. [Tutorial: How to Create a MySQL Database with Heroku](https://www.youtube.com/watch?v=aEm0BN493sU)
1. [How to deploy Python Flask MySQL based application in Heroku Cloud](https://roytuts.com/how-to-deploy-python-flask-mysql-based-application-in-heroku-cloud/)
### 資料串接
1. [Panda dataframe and SQL](https://pythontic.com/pandas/serialization/mysql)
1. [Insert pandas to sql](https://www.dataquest.io/blog/sql-insert-tutorial/)
### LINE API
1. [LINE developers website](https://developers.line.biz/zh-hant/reference/messaging-api/)
2. [Github: line/line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
