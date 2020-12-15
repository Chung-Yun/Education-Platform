import os
import sys
from decouple import config
from flask import Flask, request, abort
#from flask_sqlalchemy import SQLAlchemy
#import mariadb
import tiny_manual as man
import database as db
import hahao_crawler as hc # Webcrawling

from linebot import (
    LineBotApi, WebhookHandler #, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, SourceUser, SourceGroup
)

app = Flask(__name__)

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
    prefix = "買課幫手 " # there is a blank space
    if event.message.text.find(prefix)==0: 
        # reply to message start with 課金小天才
        my_message = event.message.text[6:]
        if len(my_message)<10:
            topic = my_message 
            myurl = 'https://hahow.in/courses?search=' + topic
            n_pages = hc.findTotalPage(myurl)
            reply = '想學嗎？（總共有' + str(n_pages) + '頁喔！）你可以去這邊：' + myurl  
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        else:
            reply = my_message + "⋯⋯太長了拉！"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
    elif event.message.text=='database overview':
        print(event)
        print(event.source.type)
        if event.source.type == 'group': # type = user / group
            target = event.source.group_id
        else:
            target = event.source.user_id
        connection = db.connectToDatabase()        
        db.addRow(connection,'Python 高級','https://example3.com','清晰')
        line_bot_api.push_message(target, TextSendMessage(text='database overview'))
    elif event.message.text=='HELP':
        if event.source.type == 'group': # type = user / group
            target = event.source.group_id
        else:
            target = event.source.user_id      
        line_bot_api.push_message(target, TextSendMessage(text=man.helpMe(prefix)))

if __name__ == "__main__":
    app.run()

