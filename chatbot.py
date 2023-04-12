from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext,CallbackQueryHandler, ConversationHandler
import configparser
import logging
import pymysql
import os 
import sys
import decimal

from config import Development as Config
  
studentID = None
securityID = None
coursecode = None
course_code,map_code = range(2)
study_progression_reuslt, security_check = range(2)
db = pymysql.connect(host="comp7940.ctai684j2oul.ap-east-1.rds.amazonaws.com", user="administrator", password="administrator", port=3298, db="db_comp7940")
cursor = db.cursor()


def main():
    config = configparser.ConfigParser()
    updater = Updater(Config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher


    gradreqconv_handler = ConversationHandler(
        entry_points=[CommandHandler(
            "gradreq", gradreq)],
        states={
            security_check: [
                MessageHandler(Filters.text & (
                    ~Filters.command), securityreq)
            ],
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
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))
    dispatcher.add_handler(CommandHandler('info', info))
    dispatcher.add_handler(CommandHandler('core', core_course_list))
    dispatcher.add_handler(CommandHandler('elective', elective_course_list))
    dispatcher.add_handler(CommandHandler("study", study))
    dispatcher.add_handler(CommandHandler("eat", eat))
    dispatcher.add_handler(CommandHandler("printer", printer))

    dispatcher.add_handler(course_handler)
    dispatcher.add_handler(gradreqconv_handler)
    dispatcher.add_handler(map_handler)
    dispatcher.add_handler(CommandHandler("cancel", cancel))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()
    updater.idle()

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="Welcome to ITM Buddy! Please find the following functions available:") 
    bot.send_message(chat_id=chat_id, text="(1) Command /hello : say hello to us 🙈 ") 
    bot.send_message(chat_id=chat_id, text="(2) Command /info : Here are some important links you may need 😇 ") 
    bot.send_message(chat_id=chat_id, text="(3) Command /gradreq <student id> : Check your study progression")   
    bot.send_message(chat_id=chat_id, text="(4) Command /course <course code> :  Check information for a specific course in ITM") 
    bot.send_message(chat_id=chat_id, text="(5) Command /core :  Check the list and schedule of the core courses for 2022-2023") 
    bot.send_message(chat_id=chat_id, text="(6) Command /elective :  Check the list and schedule of the elective courses available in 2022-2023") 
    bot.send_message(chat_id=chat_id, text="(7) Command /map <building code> :  Check the location of a building") 
    bot.send_message(chat_id=chat_id, text="(8) Command /printer :  Check the location for the printer service")   
    bot.send_message(chat_id=chat_id, text="(9) Command /eat :  Check the location for the canteen") 
    bot.send_message(chat_id=chat_id, text="(10) Command /study :  Check the location for the study place, such as library, learning common, computer room") 
    bot.send_message(chat_id=chat_id, text="(11) Command /help :  Check if you have further enquiry 🥰") 
    bot.send_message(chat_id=chat_id, text="(12) Command /cancel :  You could end the conversation if needed") 


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
    logging.info("User %s selected /gradreq studentID", userid)
    user_name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text= f'Great! {user_name} ! Please input the name of studentID')
    return security_check

def securityreq(update, context):
    global studentID
    studentID = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s selected /gradreq studentID", userid)
    logging.info("studentID %s selected /gradreq ", studentID)

    user_name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text= f'Great! {user_name} ! Please input your securityID')
    return study_progression_reuslt

# Study Progression Result
def studyprogressionresult(update, context):
    global studentID, securityID
    securityID = update.message.text

    userid = update.message.from_user.id
    logging.info("User %s gradreq studyprogressionresult studentID %s", userid, studentID)
    logging.info("User %s gradreq studyprogressionresult securityID %s", userid, securityID)
    try:
       
        cursor.execute(
            "SELECT * FROM tbl_student WHERE student_id=%s and student_security_code=%s order by RAND() LIMIT 1", (studentID, securityID))
        sqlresult = cursor.fetchall()
        db.commit()
        print("Total number of rows in table: ", cursor.rowcount)
        var =''
        if  cursor.rowcount > 0:
            for result in sqlresult:
                student_cgpa = "Student cGPA : " +  str(decimal.Decimal(result[1])) + "\n"
                student_student_result = "Student Result : " + result[10] + "\n"

            var += student_cgpa + student_student_result
        else:
            var = "Your student ID or security code may be invalid. Please try again by /gradreq."

        logging.info("User %s gradreq studyprogressionresult", var)
              
        reply_message = var   
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    return ConversationHandler.END


# course command
def course(update, context):
    userid = update.message.from_user.id
    logging.info("User %s selected /course", userid)
    user_name = update.message.from_user.first_name
    context.bot.send_message(
        chat_id=update.effective_chat.id, text= f'Great! {user_name} ! Please input the course code')
    return course_code


def course_command(update, context):
    global coursecode
    coursecode = update.message.text
    userid = update.message.from_user.id
    logging.info("User %s name %s", userid, coursecode)

    try:
       
        cursor.execute(
            "SELECT * FROM tbl_course WHERE course_code = %s", (coursecode,))
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
            "SELECT * FROM tbl_campus WHERE campus_b_code<>%s order by RAND() LIMIT 1", (map_code))
        sqlresult = cursor.fetchall()
        db.commit()

        print("Total number of rows in table: ", cursor.rowcount)
        var_campus_latitude  =''
        var_campus_longitude  =''

        for result in sqlresult:
            var_campus_latitude = result[4]
            var_campus_longitude = result[5]

        reply_message = "This is " + map_code + " location of a building" 
        print("Total var_campus_latitude: ", var_campus_latitude)
        print("Total var_campus_longitude: ", var_campus_longitude)
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
        context.bot.sendLocation(chat_id=update.effective_chat.id, latitude=var_campus_latitude, longitude=var_campus_longitude)

    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    return ConversationHandler.END


def printer(update: Update, context: CallbackContext) -> None: 
    """Send a message when the command /printer is issued."""
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id, text='You could find the printer service in the Kowloon Tong Campaus by "https://ito.hkbu.edu.hk/services/printing-services/fup.html", feel free to use the /map command to find the location 😉')

def eat(update: Update, context: CallbackContext) -> None: 
    """Send a message when the command /eat is issued."""
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id, text='There are several restaurants on campus available for students. You can find a list of them on "http://sass.hkbu.edu.hk/sass/ntt/guests/eng/Catering_Outlets.php", feel free to use the /map command to find the location 😉')

def study(update: Update, context: CallbackContext) -> None: 
    """Send a message when the command /study is issued."""
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id, text='For studying, we recommend the library (AML, SCM) and the Learning Commons (AAB, FSC), where are quiet and provide the resources for academic success, feel free to use the /map command to find the location 😉')

def help_command(update: Update, context: CallbackContext) -> None: 
    """Send a message when the command /help is issued."""
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id, text='Helping you helping you.\nIf you have further inquiries, please contact us during office hours at Telephone: +852 3411 7079 or Email: itm@comp.hkbu.edu.hk.\n Or you can use /add <studentID> to share your studuentID and we will contact you asap🤓')


#refer to helpmand
def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        print("INSERT INTO tbl_enquiry VALUES('" +  str(context.args[0]) + "')")
        cursor.execute(
            "INSERT INTO tbl_enquiry VALUES('" +  str(context.args[0]) + "', now())")
        sqlresult = cursor.fetchall()
        db.commit()

        print("Total number of rows in table: ", cursor.rowcount)

        reply_message = "Student ID added. we will contact you asap"   
        
        if len(str(context.args[0])) < 8:
            reply_message = "Invalid Student ID. Please Input again"   

        context.bot.send_message(
            chat_id=update.effective_chat.id, text=reply_message)
    except pymysql.Error as e:
        print("could not close connection error pymysql %d: %s" %
              (e.args[0], e.args[1]))
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <student id>')
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

def unknown(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")



if __name__ == '__main__':
    main()

