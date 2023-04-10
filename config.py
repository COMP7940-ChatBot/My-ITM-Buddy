class Config(object):
    LOGGER = True

    # REQUIRED
    API_KEY = "6225350751:AAGbAYu_6nk7153YwMPcXQ4n6oQwzwmjyRU"
    OWNER_ID = 5202773486 # If you dont know, run the bot and do /id in your private chat with it
    OWNER_USERNAME = "COMP7940_bot"
    ACCESS_TOKEN = "6225350751:AAGbAYu_6nk7153YwMPcXQ4n6oQwzwmjyRU"

    MYSQL_HOST = "comp7940.ctai684j2oul.ap-east-1.rds.amazonaws.com"
    MYSQL_PORT = "3298"
    MYSQL_LOGIN = "administrator"
    MYSQL_PASSWORD = "administrator"

class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
