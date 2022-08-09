import os

TOKEN = os.getenv('TOKEN')  # telegram bot api TOKEN @BotFather
DATABASE = "postgresql" + os.getenv('DATABASE_URL')[8:]  # sqlite:///bot.db

AUTO_DELETE = True