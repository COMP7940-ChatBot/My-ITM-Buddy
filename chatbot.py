from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext,CallbackQueryHandler, ConversationHandler
import configparser
import logging
#import redis
import pymysql
import os 
import sys
#global redis1
import decimal

from config import Development as Config
import mysql.connector
from mysql.connector import Error
#import telebot
#from telebot import types
  
studentID = None
coursecode = None
study_progression_reuslt, course_code,map_code = range(3)
db = pymysql.connect(host="comp7940.ctai684j2oul.ap-east-1.rds.amazonaws.com", user="administrator", password="administrator", port=3298, db="db_comp7940")
cursor = db.cursor()

#[telegram.ext.Updater]("https://python-telegrambot.readthedocs.io/en/latest/telegram.ext.updater.html#telegram.ext.updater.Updater")

#[telegram.ext.Dispatcher]("https://pythontelegrambot.readthedocs.io/en/latest/telegram.ext.dispatcher.html#telegram.ext.Dispatcher")

#[telegram.ext.Handler]("http://python-telegrambot.readthedocs.io/en/latest/telegram.ext.messagehandler.html")

# Load your token and create an Updater for your Bot

#bot = telebot.TeleBot(Config.API_KEY)

def main():
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

    gradreqconv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            "gradreq", gradreq)],
        states={
            study_progression_reuslt: [
                MessageHandler(Filters.text & (
                    ~Filters.command), studyprogressionresult)
            ],
        },
        fallbacks=[CommandHandler('end', cancel)],
    )

    
    course_handler = ConversationHandler(
        entry_points=[CommandHandler(
            "course", course)],
        states={
            course_code: [
                MessageHandler(Filters.text & (
                    ~Filters.command), course_command)
            ],
        },
        fallbacks=[CommandHandler('end', cancel)],
    )

    map_handler = ConversationHandler(
        entry_points=[CommandHandler(
            "map", map)],
        states={
            map_code: [
                MessageHandler(Filters.text & (
                    ~Filters.command), map_command)
            ],
        },
        fallbacks=[CommandHandler('end', cancel)],
    )

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dispatcher.add_handler(CommandHandler("start", start))
    #dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))
    dispatcher.add_handler(CommandHandler('info', info))
    #dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    #dispatcher.add_handler(CommandHandler('gradreq', result_info))
    dispatcher.add_handler(CommandHandler('core', core_course_list))
    dispatcher.add_handler(CommandHandler('elective', elective_course_list))

    #dispatcher.add_handler(CommandHandler('course', course_command))
    dispatcher.add_handler(course_handler)
    dispatcher.add_handler(gradreqconv_handler)
    dispatcher.add_handler(map_handler)

    updater.start_polling()
    updater.idle()

#def echo(update: Update, context: CallbackContext) -> None:
    #"""Respond to the user's message with the same message in uppercase."""
    #bot = context.bot
    #reply_message = update.message.text.upper()
    #logging.info("Update: " + str(update))
    #logging.info("context: " + str(context))
    #bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def echo(update: Update, context: CallbackContext) -> None:
    """Respond to the user's message with a greeting."""
    bot = context.bot
    user_name = update.message.from_user.first_name
    reply_message = f'Good day, {user_name}! This is My ITM Buddy. Please use the /start command to begin your journey with the chatbot.'
    bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="Welcome to ITM Buddy! Please find the following functions available:") #done
    bot.send_message(chat_id=chat_id, text="(1) Command /hello : say hello to us 🙈 ") #done
    bot.send_message(chat_id=chat_id, text="(2) Command /info : Here are some important links you may need 😇 ") #done
    bot.send_message(chat_id=chat_id, text="(3) Command /gradreq <studentID> : Check your study progression")   #needtoreview
    bot.send_message(chat_id=chat_id, text="(4) Command /course <course> :  Check information for a specific course in ITM") #needtoreview
    bot.send_message(chat_id=chat_id, text="(5) Command /core :  Check the list and schedule of the core courses for 2022-2023") #pending
    bot.send_message(chat_id=chat_id, text="(6) Command /elective :  Check the list and schedule of the elective courses available in 2022-2023") #pending
    bot.send_message(chat_id=chat_id, text="(7) Command /map <buildingshortname> :  Check the location of a building") #pending
    bot.send_message(chat_id=chat_id, text="(8) Command /print :  Check the location for the printer service")   #pending
    bot.send_message(chat_id=chat_id, text="(9) Command /eat :  Check the location for the canteen") #pending
    bot.send_message(chat_id=chat_id, text="(10) Command /study :  Check the location for the study place, such as library, learning common, computer room") #pending
    bot.send_message(chat_id=chat_id, text="(11) Command /help :  Check if you have further enquiry 🥰") #done

#def hello_command(update: Update, context: CallbackContext) -> None:
    #"""Send a message when the command /hello is issued with an argument."""
    #bot = context.bot
    #try:
        #msg = context.args[0] # /hello keyword <-- this should store the keyword
        #bot.send_message(chat_id=update.effective_chat.id, text='Good day, '+msg+'! This is Alvin_bot')
    #except (IndexError, ValueError):
        #bot.send_message(chat_id=update.effective_chat.id, text='Usage: /hello <keyword>')

def hello_command(update: Update, context: CallbackContext) -> None:
    """Respond to the /hello command with a greeting message."""
    bot = context.bot
    user_name = update.message.from_user.first_name
    reply_message = f'Good day, {user_name}! This is My ITM Buddy.'
    bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def info(update: Update, context: CallbackContext) -> None:
    """Send a message with ITM info as an inline keyboard markup."""
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(chat_id, 'ITM Info',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('ITM Website', url='https://www.comp.hkbu.edu.hk/msc/itm/en/')],
            [InlineKeyboardButton('Curriculum', url='https://www.comp.hkbu.edu.hk/msc/itm/en/curriculum.php')],
            [InlineKeyboardButton('Contact', url='https://www.comp.hkbu.edu.hk/msc/itm/tc/contact.php')],
            [InlineKeyboardButton('Prospectus', url='https://www.comp.hkbu.edu.hk/msc/msc_booklet.pdf?4')]
        ])
    )


# gradreq command
def gradreq(update, context):
    userid = update.message.from_user.id
    logging.info("User %s selected /gradreq", userid)
    user_name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text= f'Great! {user_name} ! Please input the name of studentID')
    return study_progression_reuslt

# Study Progression Result
def studyprogressionresult(update, context):
    global studentID
    studentID = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s share movie name %s", userid, studentID)

    try:
       
        cursor.execute(
            "SELECT * FROM tbl_student WHERE student_id<>%s order by RAND() LIMIT 1", (studentID))
        sqlresult = cursor.fetchall()
        db.commit()
        var =''
        for result in sqlresult:
            student_cgpa = "Student cGPA : " +  str(decimal.Decimal(result[1])) + "\n"
            student_student_result = "Student Result : " + result[10] + "\n"

        var += student_cgpa + student_student_result
                   
        reply_message = var   
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    return ConversationHandler.END

# cancel
def cancel(update, context) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logging.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! Have a nice day.'
    )
    return ConversationHandler.END

# course command
def course(update, context):
    userid = update.message.from_user.id
    logging.info("User %s selected /course", userid)
    user_name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text= f'Great! {user_name} ! Please input the name of course')
    return course_code


def course_command(update, context):
    global coursecode
    coursecode = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s name %s", userid, coursecode)

    try:
       
        cursor.execute(
            "SELECT * FROM tbl_course WHERE course_code<>%s order by RAND() LIMIT 1", (coursecode))
        sqlresult = cursor.fetchall()
        db.commit()

        print("Total number of rows in table: ", cursor.rowcount)
        var =''
        for result in sqlresult:
            course_code = "Course Code : " + result[0] + "\n"
            course_name = "Course Name : " + result[1] + "\n"
            course_category = "Course Category : " + result[2] + "\n"
            course_year = "Course Year : " + result[3] + "\n"
            course_sem = "Course Semester : " + str(result[4]) + "\n"
            course_stream = "Course Stream : " + str(result[5]) + "\n"
            course_credit = "Course Credit : " + str(result[6]) + "\n"
            course_link = "Course Link : " + str(result[7]) + "\n"
            course_daytime = "Course Day Time : " + result[10] + " " + result[11] + "\n\n"
            #var += course_code + " : " + course_name +"\n"
            var += course_code + course_name + course_year + course_sem + course_stream + course_credit + course_link + course_daytime
        
        reply_message = "student "+ var   
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    return ConversationHandler.END

# map command
def map(update, context):
    userid = update.message.from_user.id
    logging.info("User %s selected /map", userid)
    user_name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text= f'Great! {user_name} ! Please input the name of map code')
    return map_code

def map_command(update, context):
    global map_code
    map_code = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s name %s", userid, map_code)

    try:
       
        cursor.execute(
            "SELECT * FROM tbl_course WHERE course_code<>%s order by RAND() LIMIT 1", (map_code))
        sqlresult = cursor.fetchall()
        db.commit()

        print("Total number of rows in table: ", cursor.rowcount)
        var =''
        for result in sqlresult:
            course_code = "Course Code : " + result[0] + "\n"
            course_name = "Course Name : " + result[1] + "\n"
            course_category = "Course Category : " + result[2] + "\n"
            course_year = "Course Year : " + result[3] + "\n"
            course_sem = "Course Semester : " + str(result[4]) + "\n"
            course_stream = "Course Stream : " + str(result[5]) + "\n"
            course_credit = "Course Credit : " + str(result[6]) + "\n"
            course_link = "Course Link : " + str(result[7]) + "\n"
            course_daytime = "Course Day Time : " + result[10] + " " + result[11] + "\n\n"
            #var += course_code + " : " + course_name +"\n"
            var += course_code + course_name + course_year + course_sem + course_stream + course_credit + course_link + course_daytime
        
        reply_message = "student "+ var   
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    return ConversationHandler.END


def unknown(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def help_command(update: Update, context: CallbackContext) -> None: 
    """Send a message when the command /help is issued."""
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id, text='Helping you helping you.\nIf you have further inquiries, please contact us during office hours at Telephone: +852 3411 7079 or Email: itm@comp.hkbu.edu.hk.\n Or you can use /add <studentID> to share your studuentID and we will contact you asap')


#refer to helpmand
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


#Core Course List
def core_course_list(update: Update, context: CallbackContext):
    try:
        cursor.execute(
            "SELECT * FROM tbl_course Where course_category = 'Core'")
        sqlresult = cursor.fetchall()
        db.commit()

        print("Total number of rows in table: ", cursor.rowcount)
        var =''
        for result in sqlresult:
            course_code = "Course Code : " + result[0] + "\n"
            course_name = "Course Name : " + result[1] + "\n"
            course_category = "Course Category : " + result[2] + "\n"
            course_year = "Course Year : " + result[3] + "\n"
            course_sem = "Course Semester : " + str(result[4]) + "\n"
            course_stream = "Course Stream : " + str(result[5]) + "\n"
            course_credit = "Course Credit : " + str(result[6]) + "\n"
            course_link = "Course Link : " + str(result[7]) + "\n"
            course_daytime = "Course Day Time : " + result[10] + " " + result[11] + "\n\n"
            #var += course_code + " : " + course_name +"\n"
            var += course_code + course_name + course_year + course_sem + course_stream + course_credit + course_link + course_daytime
        
        reply_message = " "+ var   
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    return ConversationHandler.END

#Core Course List
def elective_course_list(update: Update, context: CallbackContext):
    try:
        cursor.execute(
            "SELECT * FROM tbl_course Where course_category = 'Elective' order by course_semester")
        sqlresult = cursor.fetchall()
        db.commit()

        print("Total number of rows in table: ", cursor.rowcount)
        var =''
        for result in sqlresult:
            course_code = "Course Code : " + result[0] + "\n"
            course_name = "Course Name : " + result[1] + "\n"
            course_category = "Course Category : " + result[2] + "\n"
            course_year = "Course Year : " + result[3] + "\n"
            course_sem = "Course Semester : " + str(result[4]) + "\n"
            course_stream = "Course Stream : " + str(result[5]) + "\n"
            course_credit = "Course Credit : " + str(result[6]) + "\n"
            #course_link = "Course Link : " + str(result[7]) + "\n"
            course_link = ""
            course_daytime = "Course Day Time : " + result[10] + " " + result[11] + "\n\n"
            #var += course_code + " : " + course_name +"\n"
            var += course_code + course_name + course_year + course_sem + course_stream + course_credit + course_link + course_daytime
        
        reply_message = " "+ var   
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    return ConversationHandler.END




if __name__ == '__main__':
    main()

