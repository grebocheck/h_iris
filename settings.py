import os

TOKEN = os.getenv("TOKEN")  # telegram bot api TOKEN @BotFather
DATABASE = "postgresql" + os.getenv('DATABASE_URL')[8:]  # sqlite:///bot.db
ADMIN_GROUP = -1001673592113  # ID ADMIN GROUP

AUTO_DELETE = True  # Auto delete bot messages
AUTO_DELETE_COMMAND = True  # Auto delete user commands
DEL_TIME = 20  # delete time for AUTO_DELETE
SUPER_ADMINS = [430952068]  # Highest admin(`s)
APP_LANGUAGE = 'en'  # user's language
MAX_WARNS = 3  # max warns, get ban user if his had max warns
GROUP_URL = "https://t.me/shard_test"  # group url
BOT_LOG = True  # save messages from ban/mute/warn
BOT_LOG_GROUP = -1001673592113  # group for BOT_LOG
WARN_LIVE = 1  # days living warn
WARN_LIVE_ALL = False  # all warns minus if time reduce compleate
