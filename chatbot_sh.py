from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import configparser
import logging
#import redis
import pymysql
import os 
import sys
#global redis1
from config import Development as Config
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
import telebot
from telebot import types
import mysql.connector
from mysql.connector import Error

  


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

    db = pymysql.connect(host=Config.MYSQL_HOST, user=Config.MYSQL_LOGIN, password=Config.MYSQL_PASSWORD, port=int(Config.MYSQL_PORT))
    #db = pymysql.connect('database-2.ckqwwshghlpj.ap-east-1.rds.amazonaws.com', 'administrator', 'administrator', '3298')
    cursor = db.cursor()
    cursor
    cursor.execute("select version()")

    data = cursor.fetchone()
    print(data)

    sql = '''use db_comp7940'''
    cursor.execute(sql)
    sql = '''SELECT * FROM tbl_campus'''
    cursor.execute(sql)
    data = cursor.fetchall()

    

    def course(course_code):
      print ()

    print(data)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("hello1",result_info))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello",greeting_command))
    dispatcher.add_handler(CommandHandler("start",start))
    
    dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    updater.start_polling()
    #updater.idle()

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

bot = telebot.TeleBot(Config.API_KEY)
@bot.message_handler(commands=['gradreq'])
def result_info(message):
    #update.message.reply_text('Enter your something')
    #bot = telebot.TeleBot(Config.API_KEY)
    #sent = bot.send_message(update.effective_chat.id, 'Please describe your problem.')
    sent = bot.send_message(message.chat.id, 'Please Enter Your Student ID.')
    bot.register_next_step_handler(sent, input_student_id)

def input_student_id(student_id):
  print ("abcde")
  #bot = telebot.TeleBot(Config.API_KEY)
  studentid = student_id.text
  #bot.send_message(student_id.chat.id, 'Enter Security ID')
  sent = bot.send_message(student_id.chat.id, 'Please Enter Security ID.')
  bot.register_next_step_handler(sent, input_security_code, student_id.text)

#@bot.message_handler(func=lambda msg: True)
def input_security_code(security_code, student_id):
  #bot.reply_to(security_code, student_id )
  execute_db_sp(security_code, "", student_id, security_code.text)

def execute_db_sp(obj, sp_name, param1="", param2=""):
    db = pymysql.connect(
        host=Config.MYSQL_HOST, 
        user=Config.MYSQL_LOGIN, 
        password=Config.MYSQL_PASSWORD, 
        port=int(Config.MYSQL_PORT),
        database="db_comp7940"
      )
    connection = mysql.connector.connect(host=Config.MYSQL_HOST,
                                         database="db_comp7940",
                                         user=Config.MYSQL_LOGIN, 
                                         password=Config.MYSQL_PASSWORD,
                                         port=int(Config.MYSQL_PORT))
    #db = pymysql.connect('database-2.ckqwwshghlpj.ap-east-1.rds.amazonaws.com', 'administrator', 'administrator', '3298')
    cursor = connection.cursor()
    #rtn_value = cursor.callproc("sp_student_result", [param1])
    #args = ['22461234', '', (0, 'CHAR')]
    #result_arg = cursor.callproc("sp_student_result", args)
    args = (param1, param2, 0) # 0 is to hold value of the OUT parameter sum
    result_arg = cursor.callproc('sp_student_result', args)
    #for result in cursor.stored_results():
    #        print(result.fetchall())
    bot.send_message(obj.chat.id, result_arg[2])

def start(update, context): 
    update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())

def main_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard())

def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Course Information', callback_data='m1')],
              [InlineKeyboardButton('Campus Information ', callback_data='m2')],
              [InlineKeyboardButton('Option 3', callback_data='m3')]]
  return InlineKeyboardMarkup(keyboard)
# ...

def first_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=first_menu_message(),
                        reply_markup=first_menu_keyboard())

def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Search Course Info by Course Code', callback_data='m1_1')],
              [InlineKeyboardButton('Search Course Info by ...', callback_data='m1_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def first_submenu(bot, update):
  pass

def second_submenu(bot, update):
  pass

#@udpater.callback_query_handler(func=lambda call: True)
#def iq_callback(query):


def main_menu_message():
  return 'Choose the option in main menu:'

def first_menu_message():
  return 'Choose the submenu in first menu:'

def second_menu_message():
  return 'Choose the submenu in second menu:'


#if __name__ == '__main__':
#    main()
bot.polling()