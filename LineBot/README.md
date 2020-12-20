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



