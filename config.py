class Config(object):
    LOGGER = True

    # REQUIRED
    API_KEY = "6225350751:AAGbAYu_6nk7153YwMPcXQ4n6oQwzwmjyRU"
    OWNER_ID = 5202773486 # If you dont know, run the bot and do /id in your private chat with it
    OWNER_USERNAME = "COMP7940_bot"
    #ACCESS_TOKEN = "6090162920:AAFOV2pvgxUZILTb014kc4oRAK329fU5hnM"
    ACCESS_TOKEN = "6225350751:AAGbAYu_6nk7153YwMPcXQ4n6oQwzwmjyRU"


    #HOST = "redis-19529.c302.asia-northeast1-1.gce.cloud.redislabs.com"
    ##PASSWORD = "SkXQHWRRZlLEvJITiJ3f1X3N7ZiaULPS"
    #REDISPORT = "19529"

    MYSQL_HOST = "comp7940.ctai684j2oul.ap-east-1.rds.amazonaws.com"
    MYSQL_PORT = "3298"
    MYSQL_LOGIN = "administrator"
    MYSQL_PASSWORD = "administrator"

    # RECOMMENDED
    #SQLALCHEMY_DATABASE_URI = 'postgres://comp7940:administrator@database-1.cvdfjwwzctqq.ap-east-1.rds.amazonaws.com:5431/db_comp7940'  # needed for any database modules
    #MESSAGE_DUMP = None  # needed to make sure 'save from' messages persist
    #LOAD = []
    ##NO_LOAD = ['translation', 'rss']
    #WEBHOOK = False
    #URL = None

    # OPTIONAL
    #SUDO_USERS = []  # List of id's (not usernames) for users which have sudo access to the bot.
    #SUPPORT_USERS = []  # List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    ##WHITELIST_USERS = []  # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    #DONATION_LINK = None  # EG, paypal
    ##CERT_PATH = None
    #PORT = 5000
    #DEL_CMDS = False  # Whether or not you should delete "blue text must click" commands
    #STRICT_GBAN = False
    #STRICT_GMUTE = False
    #WORKERS = 8  # Number of subthreads to use. This is the recommended amount - see for yourself what works best!
    #BAN_STICKER = 'CAADAgADOwADPPEcAXkko5EB3YGYAg'  # banhammer marie sticker
    #ALLOW_EXCL = False  # Allow ! commands as well as /


#class Production(Config):
#    LOGGER = False


class Development(Config):
    LOGGER = True
