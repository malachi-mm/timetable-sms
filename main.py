# author: Malachi Mahpod (:
# his super cool brother: Nerya (who didn't do anything)
import time
import datetime
import csv
import math


# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC***************'  # put your account sid
auth_token = '******************'  # put your secret token
client = Client(account_sid, auth_token)


days = {"א:": 1, "ב:": 2, "ג:": 3, "ד:": 4, "ה:": 5, "ו:": 6}

with open('luz.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    headings = next(reader)

    t = []
    for row in reader:
        b = row[5].split(',')
        a = b[0].split()
        day = days[a[1]]
        hour = a[2].split('-')
        hour[0] = hour[0].split(":")
        hour[0] = int(hour[0][0]) + int(hour[0][1])/60
        hour[1] = hour[1].split(":")
        hour[1] = int(hour[1][0]) + int(hour[1][1])/60
        t.append([day, hour[0], hour[1], row[1], b[1]])


def whatNow(day, hour):
    lesson = []
    for unit in t:
        if unit[0] == day:
            if unit[1] <= hour < unit[2]:
                lesson += [unit[3], unit[4], unit[1], unit[2]]

    return lesson


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    m1 = 0
    while True:
        day = int(datetime.datetime.today().strftime('%w')) + 1
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        hour_ = hour + (minute + 30)/60
        lesson = whatNow(day, hour_)

        if not lesson:
            message = "חופש (בינתיים)"
        else:
            message = "השיעור הבא שלך:"
            message += "\n" + lesson[0] + "   |   " + lesson[1]
            h, m = math.modf(lesson[2])
            start = str(int(m)) + ":" + str(int(h*60))
            h, m = math.modf(lesson[3])
            end = str(int(m)) + ":" + str(int(h*60))
            message += "\n בשעות:" + start + "-" + end

        if m1 != message:
            m1 = message

            message_ = client.messages.create(
                body=message,
                from_="+****",  # put the phone number that you got
                to='+*****'     # put the phone number that you want to send a message to it (if trial twilio the
                                # number have to be verified)
            )

        time.sleep(60*15)
