import datetime
import io


def log(a):
    today = datetime.datetime.today()
    t = "[" + today.strftime("%H:%M:%S - %d.%m.%y") + "] " + a
    loger = io.open('log.txt', "a", encoding="utf-8")
    loger.write(t + '\n')
    loger.close()