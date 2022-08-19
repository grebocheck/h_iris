import os

TOKEN = os.getenv("TOKEN")  # telegram bot api TOKEN @BotFather
DATABASE = "postgresql" + os.getenv('DATABASE_URL')[8:]  # sqlite:///bot.db
ADMIN_GROUP = -1001673592113  # ID ADMIN GROUP

AUTO_DELETE = True  # Auto delete bot messages
AUTO_DELETE_COMMAND = True  # Auto delete user commands
DEL_TIME = 20  # delete time for AUTO_DELETE
APP_LANGUAGE = 'en'  # user's language
MAX_WARNS = 3  # max warns, get ban user if his had max warns
GROUP_URL = "https://t.me/shard_test"  # group url
BOT_LOG = True  # save messages from ban/mute/warn
BOT_LOG_GROUP = -1001795166159  # group for BOT_LOG
WARN_LIVE = 1  # days living warn
WARN_LIVE_ALL = False  # all warns minus if time reduce compleate

# rank 0 - rank debug
# rank 1 - rank moderator
# rank 2 - rank admin
# rank 3 - rank head admin

# ACCESS LEVELS
SUPER_ADMINS = [430952068]  # Head admins rank 3
LVL_WARN = 1                # access to /warn
LVL_UNWARN = 2              # access to /unwarn
LVL_MUTE = 1                # access to /mute
LVL_UNMUTE = 2              # access to /unmute
LVL_BAN = 2                 # access to /ban
LVL_UNBAN = 2               # access to /unban
LVL_SET_MODER = 3           # access to create admin rank 1
LVL_DEL_MODER = 3           # access to delere admin rank 1
LVL_SET_ADMIN = 3           # access to create admin rank 2
LVL_DEL_ADMIN = 3           # access to delete admin rank 2
LVL_HAMER_LIST = 2          # access to /hammer (list all active ban/warn/mute)