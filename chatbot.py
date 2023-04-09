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
  
  
studentID = None
Studyprogression = range(2)
db = pymysql.connect(host="comp7940.ctai684j2oul.ap-east-1.rds.amazonaws.com", user="administrator", password="administrator", port=3298, db="db_comp7940")
cursor = db.cursor()

#[telegram.ext.Updater]("https://python-telegrambot.readthedocs.io/en/latest/telegram.ext.updater.html#telegram.ext.updater.Updater")

#[telegram.ext.Dispatcher]("https://pythontelegrambot.readthedocs.io/en/latest/telegram.ext.dispatcher.html#telegram.ext.Dispatcher")

#[telegram.ext.Handler]("http://python-telegrambot.readthedocs.io/en/latest/telegram.ext.messagehandler.html")

# Load your token and create an Updater for your Bot
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
            "sharegradreq", sharegradreq)],
        states={
            Studyprogression: [
                MessageHandler(Filters.text & (
                    ~Filters.command), sharestudyprogression)
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

    dispatcher.add_handler(CommandHandler('course', course_command))
    dispatcher.add_handler(gradreqconv_handler)

    updater.start_polling()
    updater.idle()

# gradreq command
def sharegradreq(update, context):
    userid = update.message.from_user.id
    logging.info("User %s selected /gradreq", userid)
    user_name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text= f'Great! {user_name} ! Please input the name of studentID')
    return Studyprogression

# sharestudyprogression
def sharestudyprogression(update, context):
    global studentID
    studentID = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s share movie name %s", userid, studentID)

    try:
       
        cursor.execute(
            "SELECT * FROM tbl_student WHERE student_id<>%s order by RAND() LIMIT 1", (studentID))
        sqlresult = cursor.fetchall()
        db.commit()
        for result in sqlresult:
            student_cgpa = result[1]
            student_total_unit = result[1]

        #dec = decimal.Decimal(student_cgpa)
                   
        reply_message = "student cGPA:"+ str(decimal.Decimal(student_cgpa))   
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

# sharecourse
def course_command(update, context):
    global studentID
    studentID = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s share movie name %s", userid, studentID)

    try:
       
        cursor.execute(
            "SELECT * FROM tbl_course")
        sqlresult = cursor.fetchall()
        db.commit()

        print("Total number of rows in table: ", cursor.rowcount)
        var =''
        for result in sqlresult:
            course_code = result[0]
            course_name = result[1]
            var += course_code + " : " + course_name +"\n"
        
        reply_message = "student "+ var   
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    return ConversationHandler.END







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


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="Welcome to ITM Buddy! Please find the following functions available:")
    bot.send_message(chat_id=chat_id, text="(1) Command /hello : say hello to us 🙈 ")
    bot.send_message(chat_id=chat_id, text="(2) Command /info : Here are some important links you may need 😇 ")
    bot.send_message(chat_id=chat_id, text="(3) Command /gradreq <studentID> : Check your study progression")   
    bot.send_message(chat_id=chat_id, text="(4) Command /course <course> :  Check information for a specific course in ITM")
    bot.send_message(chat_id=chat_id, text="(5) Command /core :  Check the list and schedule of the core courses for 2022-2023")
    bot.send_message(chat_id=chat_id, text="(6) Command /elective :  Check the list and schedule of the elective courses available in 2022-2023")
    bot.send_message(chat_id=chat_id, text="(7) Command /map <buildingshortname> :  Check the location of a building")
    bot.send_message(chat_id=chat_id, text="(8) Command /print :  Check the location for the printer service")   
    bot.send_message(chat_id=chat_id, text="(9) Command /eat :  Check the location for the canteen") 
    bot.sendMessage(chat_id=chat_id, text="(10) Command /study :  Check the location for the study place, such as library, learning common, computer room")
    bot.sendMessage(chat_id=chat_id, text="(11) Command /help :  Check if you have further enquiry 🥰")

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

def unknown(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

def help_command(update: Update, context: CallbackContext) -> None: 
    """Send a message when the command /help is issued."""
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id, text='Helping you helping you.\nIf you have further inquiries, please contact us during office hours at Telephone: +852 3411 7079 or Email: itm@comp.hkbu.edu.hk..')


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