from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import configparser
import logging
#import redis
import pymysql
import os 
import sys
#global redis1
from config import Development as Config
  


#[telegram.ext.Updater]("https://python-telegrambot.readthedocs.io/en/latest/telegram.ext.updater.html#telegram.ext.updater.Updater")

#[telegram.ext.Dispatcher]("https://pythontelegrambot.readthedocs.io/en/latest/telegram.ext.dispatcher.html#telegram.ext.Dispatcher")

#[telegram.ext.Handler]("http://python-telegrambot.readthedocs.io/en/latest/telegram.ext.messagehandler.html")

 
def main():
# Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    #config.read('config.ini')
    #config.read('config.py')
    #updater = Updater(token=(Config.API_KEY), use_context=True)
    updater = Updater(Config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    #global redis1
    #redis1 = redis.Redis(host=(Config.HOST), password=(Config.PASSWORD), port=(Config.REDISPORT))
    print("abc")
    TOKEN = Config.API_KEY
    print(TOKEN) 
    OWNER_ID = int(Config.OWNER_ID)
    print(OWNER_ID)
    #host = Config.HOST
    ##password = Config.PASSWORD
    #port = Config.REDISPORT
    #print(host)
    #print(password)
    #print(port)

    db = pymysql.connect(host="database-2.ckqwwshghlpj.ap-east-1.rds.amazonaws.com", user="administrator", password="administrator", port=3298)
    #db = pymysql.connect('database-2.ckqwwshghlpj.ap-east-1.rds.amazonaws.com', 'administrator', 'administrator', '3298')
    cursor = db.cursor()
    cursor
    cursor.execute("select version()")

    data = cursor.fetchone()
    print(data)

    sql = '''use Test_Schema'''
    cursor.execute(sql)
    sql = '''SELECT * FROM Persons'''
    cursor.execute(sql)
    data = cursor.fetchall()


    print(data)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello",greeting_command))
   
    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)

def greeting_command(update: Update, context: CallbackContext) -> None:
    try:
        update.message.reply_text('Good Day, ' + context.args[0] + '!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /hello <keyword>')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Helping you helping you.')

def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        #global redis1
        logging.info(context.args[0])
        msg = context.args[0] # /add keyword <-- this should store the keyword
        #redis1.incr(msg)
        #update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        print(1)
        #global redis1
        print(2)
        logging.info(context.args[0])
        print(3)
        msg = context.args[0] # /add keyword <-- this should store the keyword
        print(4)

        #redis1.incr(msg)
        #update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')


if __name__ == '__main__':
    main()
