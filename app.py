import time
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.chataction import ChatAction

from telegram import InlineKeyboardButton 
from telegram import InlineKeyboardMarkup

import confiq

import os
PORT = int(os.environ.get('PORT', 5000))


updater = Updater(confiq.id)
counter = 1

def start(bot, update):
    # import pdb;pdb.set_trace()
    chat_id = update.message.chat_id
    global counter
    counter = 1

    bot.send_chat_action(chat_id,ChatAction.TYPING)
    bot.sendMessage(chat_id,confiq.continuetext)

    name = update.message.chat.first_name
    familyname = update.message.chat.last_name 

    save(name,familyname)

    
def continues(bot,update):
    time.sleep(1)
    q1(bot,update)

def q1(bot, update):    
    chat_id = update.message.chat_id    
    keyboard = [
                 [
                     InlineKeyboardButton('سلامتی',callback_data='1'),
                     InlineKeyboardButton('خطر',callback_data='2'),
                     InlineKeyboardButton('کودک',callback_data='3'),
                     InlineKeyboardButton('قول',callback_data='4'),   
                 ]
               ]    
    
    sendimg1(bot,update)

    global counter
    counter +=1
    
    bot.sendMessage(chat_id,'باشنیدن کلمه مراقبت یاد چی میفتی ؟',reply_markup = InlineKeyboardMarkup(keyboard) )    

def q1_handler_btn(bot, update):
    # import pdb;pdb.set_trace()
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id  =query.message.message_id
    des =''

    name = update.callback_query.message.chat.first_name
    familyname = update.callback_query.message.chat.last_name    

    global counter
    flag = False
    # counter += 1

    if counter == 2:
        q2(bot,query)
        des = 'پیام شما ثبت شد با تشکر. \n'
        save1(name, familyname, data)
    elif counter == 3:
        q3(bot,query)
        des = 'پیام شما ثبت شد با تشکر. \n'      
        save2(name, familyname, data)
    elif counter == 4:       
        des = confiq.podcastText
        save3(name, familyname, data)
        counter = 1
        flag = True

    bot.editMessageText(text = des,chat_id = chat_id, message_id = message_id)
    
    if flag :
        flag = False
        time.sleep(3)        
        sendpodcast(bot,chat_id)
        time.sleep(160) 
        sendlinksite(bot,chat_id)
        savelink(name,familyname)
    

def q2(bot, query):      
    chat_id = query.message.chat_id    
    keyboard = [
                 [
                    InlineKeyboardButton('بله',callback_data='1'),
                    InlineKeyboardButton('خیر',callback_data='2'),
                     
                 ]
               ]    

    sendimg2(bot,query)

    global counter
    counter +=1

    bot.sendMessage(chat_id,'تابه حال ازچیزی مراقبت ویژه ای کردید؟',reply_markup = InlineKeyboardMarkup(keyboard) )

def q2_handler_btn(bot, update):
    query = update.callback_query
    # data = query.data
    chat_id = query.message.chat_id
    message_id  =query.message.message_id    
    des ='/Q3'

    bot.editMessageText(text = des,chat_id = chat_id, message_id = message_id)

def q3(bot, query):    
    chat_id = query.message.chat_id    
    keyboard = [
                 [
                    
                    InlineKeyboardButton('امنیت',callback_data='1'),
                    InlineKeyboardButton('قول وقرار',callback_data='2'),
                    InlineKeyboardButton('سلامت',callback_data='3'),
                    InlineKeyboardButton('دارایی',callback_data='4'),
                     
                     
                 ]
               ]    

    sendimg3(bot,query)

    global counter
    counter +=1

    bot.sendMessage(chat_id,'به نظرت کدوم مورد به مراقبت ویژه ای نیاز داره؟',reply_markup = InlineKeyboardMarkup(keyboard) )

def q3_handler_btn(bot, update):
    query = update.callback_query
    # data = query.data
    chat_id = query.message.chat_id
    message_id  =query.message.message_id
    des ='/pod'

    bot.editMessageText(text = des,chat_id = chat_id, message_id = message_id) 

def sendpodcast(bot, chat_id):
    # chat_id = update.message.chat_id
    chat_id = chat_id
    bot.send_chat_action(chat_id,ChatAction.UPLOAD_AUDIO)
    audio=open('mp3/مراقبت ویژه.mp3', 'rb')
    bot.send_audio(chat_id, audio)     
    audio.close()

    time.sleep(5)
    sendlinksite(bot,chat_id)

def sendimg1(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id,ChatAction.UPLOAD_PHOTO)
    img = open('img/1.jpg', 'rb')
    bot.sendPhoto(chat_id, img)
    img.close()

def sendimg2(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id,ChatAction.UPLOAD_PHOTO)
    img = open('img/2.jpg', 'rb')
    bot.sendPhoto(chat_id, img)
    img.close()

def sendimg3(bot, update):
    chat_id = update.message.chat_id
    bot.send_chat_action(chat_id,ChatAction.UPLOAD_PHOTO)
    img = open('img/3.jpg', 'rb')
    bot.sendPhoto(chat_id, img)
    img.close()

def sendlinksite(bot,chat_id):
    chat_id = chat_id       
    bot.send_chat_action(chat_id,ChatAction.TYPING)
    keyboard = [
                 [
                    
                    InlineKeyboardButton('لینک','https://moraghebatevizhe-pelak12.fandogh.cloud/'),                                        
                     
                 ]
               ]    
    bot.sendMessage(chat_id,'کلیک کنید',reply_markup = InlineKeyboardMarkup(keyboard) )
def save(name, familyname):   
    op = open('doc/Login.txt','a+')    
    start = time.time()
    start = time.localtime(start)    
    op.writelines('{} {} {}:{}:{}\n'.format(name, familyname,start.tm_hour,start.tm_min,start.tm_sec))
    op.close()


def save1(name, familyname, data):
    op = open('doc/Info_1.txt','a+')
    op.writelines('{} {} : {}\n'.format(name, familyname, data))
    op.close()

def save2(name, familyname, data):
    op = open('doc/Info_2.txt','a+')
    op.writelines('{} {} : {}\n'.format(name, familyname, data))
    op.close()

def save3(name, familyname, data):
    op = open('doc/Info_3.txt','a+')
    op.writelines('{} {} : {}\n'.format(name, familyname, data))
    op.close()

def savelink(name, familyname):
    op = open('doc/info_link.txt','a+')    
    start = time.time()
    start = time.localtime(start)    
    op.writelines('{} {} {}:{}:{}\n'.format(name, familyname,start.tm_hour,start.tm_min,start.tm_sec))
    op.close()

def sendlog(bot, update, args):
    chat_id = update.message.chat_id   
    if not args:
        bot.sendMessage(chat_id,"لطفا پسورد خود را وارد کنید")
    elif args[0] == confiq.password:           
        bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
        doc = open('./doc/Login.txt', 'rb')
        bot.sendDocument(chat_id, doc)
    else:
        bot.sendMessage(chat_id,'پسورد وارد شده صحیح نمی باشد')  
    doc.close()

def sendq1(bot, update, args):
    chat_id = update.message.chat_id   
    if not args:
        bot.sendMessage(chat_id,"لطفا پسورد خود را وارد کنید")
    elif args[0] == confiq.password:           
        bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
        doc = open('./doc/Info_1.txt', 'rb')
        bot.sendDocument(chat_id, doc)
    else:
        bot.sendMessage(chat_id,'پسورد وارد شده صحیح نمی باشد')  
    doc.close()

def sendq2(bot, update, args):
    chat_id = update.message.chat_id
    if not args:
        bot.sendMessage(chat_id,"لطفا پسورد خود را وارد کنید")
    elif args[0] == confiq.password:
        chat_id = update.message.chat_id
        bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
        doc = open('./doc/Info_2.txt', 'rb')
        bot.sendDocument(chat_id, doc)
        doc.close()
    else:
       bot.sendMessage(chat_id,"پسورد وارد شده صحیح نمی باشد")

def sendq3(bot, update, args):
    chat_id = update.message.chat_id
    if not args:
        bot.sendMessage(chat_id,"لطفا پسورد خود را وارد کنید")        
    elif args[0] == confiq.password:
        chat_id = update.message.chat_id
        bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
        doc = open('./doc/Info_3.txt', 'rb')
        bot.sendDocument(chat_id, doc)
        doc.close()
    else:
       bot.sendMessage(chat_id,"پسورد وارد شده صحیح نمی باشد")

def sendlinkinfo(bot, update, args):
    chat_id = update.message.chat_id
    if not args:
        bot.sendMessage(chat_id,"لطفا پسورد خود را وارد کنید")
    elif args[0] == confiq.password:        
        bot.send_chat_action(chat_id,ChatAction.UPLOAD_DOCUMENT)
        doc = open('./doc/info_link.txt', 'rb')
        bot.sendDocument(chat_id, doc)
        doc.close()
    else:
      bot.sendMessage(chat_id,"پسورد وارد شده صحیح نمی باشد")

# --------------Command--------------- #
start_command = CommandHandler('start',start)
sendpodcast_command = CommandHandler('pod',sendpodcast)
continues_command = CommandHandler('continue',continues)
link_command = CommandHandler('link',sendlinksite)

sendlog_command = CommandHandler('log',sendlog, pass_args= True)
sendq1_command = CommandHandler('info1',sendq1, pass_args= True)
sendq2_command = CommandHandler('info2',sendq2, pass_args= True)
sendq3_command = CommandHandler('info3',sendq3, pass_args= True)
sendlink_command = CommandHandler('linkinfo',sendlinkinfo, pass_args= True)

# Q1
q1_command = CommandHandler('Q1',q1)
q1_handler = CallbackQueryHandler(q1_handler_btn)
img1_command = CommandHandler('img1',sendimg1)

# Q2
q2_command = CommandHandler('Q2',q2)
q2_handler = CallbackQueryHandler(q2_handler_btn)
img2_command = CommandHandler('img2',sendimg2)

# Q3
q3_command = CommandHandler('Q3',q3)
q3_handler = CallbackQueryHandler(q3_handler_btn)
img3_command = CommandHandler('img3',sendimg3)

# -----------------------Dispatcher-----------------------#

updater.dispatcher.add_handler(start_command)
updater.dispatcher.add_handler(sendpodcast_command)
updater.dispatcher.add_handler(continues_command)
updater.dispatcher.add_handler(link_command)

updater.dispatcher.add_handler(sendlog_command)
updater.dispatcher.add_handler(sendq1_command)
updater.dispatcher.add_handler(sendq2_command)
updater.dispatcher.add_handler(sendq3_command)
updater.dispatcher.add_handler(sendlink_command)

# Q1
updater.dispatcher.add_handler(q1_command)
updater.dispatcher.add_handler(q1_handler)
updater.dispatcher.add_handler(img1_command)

# Q2
updater.dispatcher.add_handler(q2_command)
updater.dispatcher.add_handler(q2_handler)
updater.dispatcher.add_handler(img2_command)

# Q3
updater.dispatcher.add_handler(q3_command)
updater.dispatcher.add_handler(q3_handler)
updater.dispatcher.add_handler(img3_command)


# updater.start_polling()

updater.start_webhook(listen="0.0.0.0",
                        port=int(PORT),
                        url_path=updater)
updater.bot.setWebhook('https://yourherokuappname.herokuapp.com/' + updater)

updater.idle()