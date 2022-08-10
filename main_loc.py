from aiogram import executor
from bot.bote import *

if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp, skip_updates=True)
        except Exception as ex:
            print(ex)
