import os
import sys
from decouple import config
from flask import Flask, request, abort
import numpy as np
import pandas as pd

# Modules
import tiny_manual as man # Manual
import database as db # Database
import hahow_crawler as hc # Webcrawling

from linebot import (
    LineBotApi, WebhookHandler #, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
#    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
#    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
#    ImageMessage, VideoMessage, AudioMessage, FileMessage,
#    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
#    MemberJoinedEvent, MemberLeftEvent,
#    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
#    TextComponent, IconComponent, ButtonComponent,
#    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)

app = Flask(__name__)

# get KEYS from your environment variable
channel_secret = config('LINE_CHANNEL_SECRET')
channel_access_token = config('LINE_CHANNEL_ACCESS_TOKEN')
line_bot_api = LineBotApi(channel_access_token, timeout = 30)
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

def push_back_message(event, the_message):
    """ Pushes text messages back to either group or user. """
    if event.source.type == 'group': # type = user / group
        target = event.source.group_id
    else:
        target = event.source.user_id   
    return line_bot_api.push_message(target, TextSendMessage(text=the_message))

def push_back_template(event, template_message):
    """ Pushes template messages back to either group or user. 
    :param event <event>: the message
    """
    if event.source.type == 'group': # type = user / group
        target = event.source.group_id
    else:
        target = event.source.user_id   
    return line_bot_api.push_message(target, template_message)

def what_would_you_like_to_learn(event):
    """ Ask user what they would like to learn and redirect with postback messages. 
    :param event <event>: the message
    """
    learning_choices = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/xHzymxe.gif',
            title= '今天想學些什麼？',
            text= '抱歉，你能選的只有：',
            actions= [ 
                PostbackAction(
                    label= 'Python',
                    data= 'action=register_user&'+str(event.source.user_id)+'&Python'
                ),
                PostbackAction(
                    label= '想學其他東西點這邊',
                    data= 'demande=learn_sth_else'
                )
            ]
        )
    )
    return learning_choices

def feature_proposal(event, topic):
    """ Selects classes and recommand to users 
    :param event <event>: the message
    :param topic <string>: the topic that users want to learn
    """
    query_count = 'SELECT * FROM Python GROUP BY class_title;'
    n_class = len( db.executeQuery(query_count))

    recommandation = '找到'+str(n_class)+'堂課\n 輸入你有興趣的_'+topic+'_課程類型\n 最多可選擇三個類型\n 推薦類型:'

    # Select 10 features (from table 4)   
    feature_names = ["推薦","簡單","程式","好理解","用心","豐富","清晰","實用","樂於回答","應用"]

    features_lst = []
    max_features = 10
    for i in range(max_features):
        features_lst.append(            
            PostbackAction(
                    label=feature_names[i],
                    display_text= feature_names[i] + '已選取', # output as messages
                    data='action=select_feature&'+str(event.source.user_id)+'&'+feature_names[i]
                )
        )

    
    # Create carousel template  
    car_cols = []
    for i in range(4):
        action_lst = []
        for j in range(3):
            if 3*i+j < max_features:
                action_lst.append(features_lst[3*i+j])
            elif 3*i+j == max_features:
                action_lst.append(
                    URIAction(
                    label='回報問題',
                    uri='https://github.com/Chung-Yun/Education-Platform'
                    )
                )
            else:
                action_lst.append(
                    PostbackAction(
                    label= '.',
                    data='NAN'
                    )
                )
        car_cols.append(CarouselColumn(thumbnail_image_url='https://i.imgur.com/xHzymxe.gif',
                       title='課程推薦系統', 
                       text= recommandation + '（第'+str(i+1)+'頁）', 
                       actions= action_lst
                       ))

        
    carousel_template = CarouselTemplate(columns=car_cols)
    
    return TemplateSendMessage(alt_text='課程推薦系統', template=carousel_template)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Parameters
    prefix = "買課幫手" # there is a blank space
    system_setup_prefix = '-set- ' # there is a blank space

    # Ask for HELP
    if event.message.text=='HELP':
        line_bot_api.reply_message(event.reply_token, man.helpWithCarousel())

    # Section I: Interaction with users

    elif event.message.text.find(prefix)==0: 
        # reply to message start with prefix
        my_message = event.message.text[len(prefix)+1:]
        if my_message.find("我想學 ")==0:
            table_name = my_message[len("我想學 "):]
            if table_name == 'Python':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=table_name+ ' 已創建，請輸入「買課幫手」'))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="開始創建 "+table_name))
                push_back_message(event,"正在幫您爬找資料，請稍等") # There is technical issue here, might need to change
                #df =  hc.crawlAllComments(table_name)
                #db.addTableFromDF(table_name, df)
                
                topic = my_message 
                n_pages = hc.findTotalPage(topic)
                
                push_back_message(event,"結束創建"+table_name) # this is placed here to create delay

                reply = '想學嗎？（總共有' + str(n_pages) + '頁喔！）你可以去這邊：' + myurl  
                push_back_message(event,reply)

        # THIS IS THE BEGINNING OF THE LONG DIALOG
        elif len(my_message)==0:
            line_bot_api.reply_message(event.reply_token, what_would_you_like_to_learn(event))



    # Section II: Backend setup for devs

    elif event.message.text.find(system_setup_prefix)==0:
        setup_order = event.message.text[len(system_setup_prefix):]
        if setup_order.find('create')==0:
            table_name = setup_order[len('create')+1:]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=table_name+' created'))
            if table_name=='replies':
                log_message = db.createTableReplies()
                push_back_message(event,str(log_message))
            else:
                push_back_message(event,'ERR: nothing created')
        elif setup_order.find('reset')==0:
            table_name = setup_order[len('reset')+1:]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='start resetting '+table_name))
            if table_name=='replies':
                db.resetTableReplies()
            else: 
                db.resetTableComments(table_name)
            push_back_message(event,table_name+' has been reset')
        elif setup_order.find('add')==0:
            table_name = setup_order[len('add')+1:]
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='added a row to '+table_name))
            if table_name=='replies':
                addition_replies_df = pd.DataFrame({\
                        "user_id"       : ['example_user_id'], \
                        "reply"         : ['passion'], \
                        "choices"       : ['features'], \
                        "time_stamp"    : ['date'], \
                        "status"        : [0]}) 
                db.addTableFromDF(table_name, addition_replies_df)
                push_back_message(event,"done adding example")
            else :
                push_back_message(event,"done nothing")

            



@handler.add(PostbackEvent)
def handle_postback(event):
    print(event.postback.data)
    if event.postback.data == 'demande=learn_sth_else':
        line_bot_api.reply_message(event.reply_token,  TextSendMessage('請下指令： 買課幫手 我想學 [想學的東西]\n Example: 買課幫手 我想學 英文'))

    elif event.postback.data.find('action')==0 :
        # action=select_feature&'+str(event.source.user_id)+'&'+featurename
        data = event.postback.data[len('action')+1:]
        print(data)

        # Step 1: Registeration
        if data.find('register_user')==0 :

            # Interprete user_id and selected features
            user_and_label = data[len('register_user')+1:]
            first_and = user_and_label.find('&')
            user_id = user_and_label[:first_and]
            label = user_and_label[first_and+1:]
            
            
            # Save to DB (status set to 0)
            register_df = pd.DataFrame({\
                        "user_id"       : [user_id], \
                        "reply"         : [label], \
                        "choices"       : [''], \
                        "time_stamp"    : ['date'], \
                        "status"        : [0]}) 
            db.addTableFromDF('replies', register_df)
            print('user registered to replies')
            
            line_bot_api.reply_message(event.reply_token, feature_proposal(event, label))
        
        # Step 2: Choose features
        elif data.find('select_feature')==0:

            # Interprete user_id and selected features
            user_and_feature = data[len('select_feature')+1:]
            first_and = user_and_feature.find('&')
            user_id = user_and_feature[:first_and]
            feature = user_and_feature[first_and+1:]
            
            # Get user's latest reply 
            query = "SELECT * FROM replies WHERE user_id = '"+user_id+"' ORDER BY replies_id DESC LIMIT 1"
            last_reply = db.executeQuery(query)[0] # type = dictionary
            print(last_reply)
            reply = last_reply['reply']
            features = last_reply['choices']
            status = int(last_reply['status']) ### remove this later
            
            if status == 0 :
                # add feature 1 and change status
                addition_replies_df = pd.DataFrame({\
                        "user_id"       : [user_id], \
                        "reply"         : [reply], \
                        "choices"       : [features+'&'+feature], \
                        "time_stamp"    : ['date'], \
                        "status"        : [1]}) 
                db.addTableFromDF('replies', addition_replies_df)
                print('user : '+user_id+' | status = 0')
            elif status == 1 :
                addition_replies_df = pd.DataFrame({\
                        "user_id"       : [user_id], \
                        "reply"         : [reply], \
                        "choices"       : [features+'&'+feature], \
                        "time_stamp"    : ['date'], \
                        "status"        : [2]}) 
                db.addTableFromDF('replies', addition_replies_df)
                print('user : '+user_id+' | status = 1')
            elif status == 2 : 
                # All three features are here now, do the research
                first_and = features[1:].find('&') # features = &feature1&feature2
                feature1 = features[1:first_and]
                feature2 = features[first_and+1:]
                feature3 = feature
                push_back_message(event,feature1+'、'+feature2+'、'+feature3+'⋯⋯稍等我一下')

                #### RECOMMENDATION PART #### # TODO
                #query = "SELECT * FROM tableThree;hon WHERE class_title = '"+courses[i]+"' LIMIT 1"
                #class_info = db.executeQuery(query)[0] # type = dictionary
                tableThree = db.fetchTable2Dataframe('tableThree')
                #print(tableThree)
                scores = []  
                for i in range(len(tableThree.index)):
                    score = 0
                    for j in range(len(tableThree.columns)-1):
                        if tableThree.loc[i][j+1]==feature1:
                            score +=1
                        elif tableThree.loc[i][j+1]==feature2:
                            score +=1
                        elif tableThree.loc[i][j+1]==feature3:
                            score +=1 
                    scores.append(score)
                
                # sorting
                arr_data = np.array(scores)
                idx = (-arr_data).argsort()[:10]
                courses = []
                for i in range(3):
                    courses.append(tableThree.loc[idx[i]][0])
                    
                # Presentation
                car_cols = []
                for i in range(3):
                    # Dig data from Table 2 (Python)
                    print(courses[i])
                    query = "SELECT * FROM Python WHERE class_title = '"+courses[i]+"' LIMIT 1"
                    class_info = db.executeQuery(query)[0] # type = dictionary
                    
                    class_url = class_info["class_url"]
                    class_figure = class_info["class_figure"]
                    stars = class_info["stars"]
                    teacher_name = class_info["teacher_name"]
                    price = class_info["price"]
                    car_cols.append(CarouselColumn(thumbnail_image_url=class_figure ,
                                   title='推薦課程'+str(i+1)+'-'+courses[i],
                                   text= '老師：'+teacher_name+'/ 星數：'+stars+'/ 價格：'+price , 
                                   actions=[
                                       URIAction(
                                            label='課程連結',
                                            uri=class_url                                            )
                                   ]
                                   ))
                    
                carousel_template = CarouselTemplate(columns=car_cols)
                course_proposal = TemplateSendMessage(alt_text='課程推薦', template=carousel_template)
 


                # Propose and ask for confirm
                push_back_template(event,course_proposal)

                confirm_template_message = TemplateSendMessage(
                    alt_text='Confirm template',
                    template=ConfirmTemplate(
                    text='結果滿意嗎?',
                    actions=[
                        PostbackAction(
                            label='滿意',
                            data='confirm_suggestion'
                            ),
                        PostbackAction(
                            label='不滿意',
                            data='decline_suggestion'
                            ) 
                        ]
                    )
                )
                push_back_template(event, confirm_template_message)
            elif status > 2 : 
                push_back_message(event,'超過三個了！')
            else:
                push_back_message(event,'There is an error, pls contact our staff. Tks!')


    elif event.postback.data == 'confirm_suggestion':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='結束'))
    elif event.postback.data == 'decline_suggestion':
        label = 'Python'
        user_id = target = event.source.user_id
        # status set to 0 again
        register_df = pd.DataFrame({\
                        "user_id"       : [user_id], \
                        "reply"         : [label], \
                        "choices"       : [''], \
                        "time_stamp"    : ['date'], \
                        "status"        : [0]}) 
        db.addTableFromDF('replies', register_df)
        
        line_bot_api.reply_message(event.reply_token, feature_proposal(event, label)) # back to this

                



if __name__ == "__main__":
    app.run()

