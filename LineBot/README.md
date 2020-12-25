# LINE Bot

We created a LINE bot from zero for this project. Check out tutorial.md for the setups.

## Directory overview

### LineBot V1

A save of the first version of the bot.

### LineBot V2

This version has most of the essential tools to communicate with the data base and the skeleton of our dialog.

### LineBot V3

Final version for the ccClub course.

 
## Communication with Database

We deployed a tiny cloud database for our bot to store information. There are 5 types of tables in the DB.

### Table Type I

This is mainly our dictionary for comment analysis.

|ID|Type|Representative word|Synonym|
|-|-|-|-|
|int|varchar(50)|varchar(50)|varchar(255)|

### Table Type II

Web crawling results.

|ID|class_title|class_url|class_figure|stars|teacher_name|price|comment_date|comment_title|comment_text|
|-|-|-|-|-|-|-|-|-|-|
|int|varchar(50)|varchar(255)|varchar(255)|varchar(50)|varchar(50)|varchar(50)|varchar(50)|varchar(50)|varchar(255)|

### Table Type III

From Table I and Table II, find the 10 keywords that occurs the most in each course(class_name).
Keyword
: represented by *Representative word*, is the group of words defined in Table I.

|ID|class_title|Keyword1|Keyword2|Keyword3|Keyword4|Keyword5|Keyword6|Keyword7|Keyword8|Keyword9|Keyword10|
|-|-|-|-|-|-|-|-|-|-|-|-|
|int|varchar(50))|varchar(50)|varchar(50)|varchar(50)|varchar(50)|varchar(50))|varchar(50)|varchar(50)|varchar(50)|varchar(50)|varchar(50)|


### Table Type IV

|ID|Representative word|n_count|
|-|-|-|
|int||varchar(50)|int|

n_count
: The number of time the class of representative word is presented in all comments in Table II.


### Table Type V
Given three *Representative words*, show how many keywords are matched (0-3) for each course in Table III.


|ID|class_name|n_match|
|-|-|-|
|int||varchar(50)|int|


