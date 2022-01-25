import telebot
from telebot import types
import time
import datetime

from config import TOKEN
from messages import messages
import keyboards as keyboards
from production_calendar import get_days, record_time, work_time
import google_calendar

bot = telebot.TeleBot(token=TOKEN)
states = {}
dates = {}

@bot.message_handler(commands=['start'])
def process_to_start_command(message: types.Message):
    bot.send_message(message.from_user.id, messages['start'])

@bot.message_handler(commands=['help'])
def process_to_help_command(message: types.Message):
    bot.send_message(message.from_user.id, messages['help'])

@bot.message_handler(commands=['time'])
def process_to_help_command(message: types.Message):
    time_server = datetime.datetime.today()
    time_moscow = time_server + datetime.timedelta(hours=7)
    report = 'Сервер: ' + str(time_server) + ', Москва: ' + str(time_moscow)
    bot.send_message(message.from_user.id, report)

@bot.message_handler(content_types=['text'])
def start(message):
    question = message.from_user.first_name + ', чем я могу помочь?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboards.keyboard_main)

# Новая запись
@bot.callback_query_handler(func=lambda call: call.data == 'record')
def new_record_on_day(message):
    have_record = google_calendar.get_my_time(str(message.from_user.id))
    if have_record != False:
        report = 'Вы уже записаны на ' + have_record
        bot.send_message(message.from_user.id, text=report)
    else:
        global states
        states[message.from_user.id] = 'record'
        question = 'На какую дату вы хотели бы записаться?'
        time_server = datetime.datetime.today()
        time_moscow = time_server + datetime.timedelta(hours=7)
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboards.keyboard_days_select(time_moscow))

# Узнаем расписание на неделю
@bot.callback_query_handler(func=lambda call: call.data == 'schedule')
def learn_schedule_on_week(message):
    global states
    states[message.from_user.id] = 'schedule'
    question = 'На какую дату вы хотели бы бы хотели узнать свободное время?'
    time_server = datetime.datetime.today()
    time_moscow = time_server + datetime.timedelta(hours=7)
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboards.keyboard_days_select(time_moscow))

# обрабатываем сообщение с датой
@bot.callback_query_handler(func=lambda call: call.data in get_days(datetime.datetime.today()+ datetime.timedelta(hours=7)).values())
def new_record_on_time(message):
    global states, dates
    if message.from_user.id in states:
        freedom_time = google_calendar.get_freedom_time(message.data)
        if states[message.from_user.id] == 'record' and len(freedom_time) > 0:
            question = 'На какое время вы хотели бы записаться?'
            keyboard_with_freedom_time = keyboards.keyboard_with_freedom_time(freedom_time)
            bot.send_message(message.from_user.id, text=question, reply_markup=keyboard_with_freedom_time)
            dates[message.from_user.id] = message.data
        elif states[message.from_user.id] == 'record' and len(freedom_time) == 0:
            report = 'На дату ' + message.data + ' записать не могу, там нет свободного времени :('
            bot.send_message(message.from_user.id, text=report)
            states.pop(message.from_user.id)
        elif states[message.from_user.id] == 'schedule':
            if len(freedom_time) > 0:
                report = 'На дату ' + message.data + ' свободно следующее время: '
                for time in freedom_time.keys():
                        report = report + time + ', '
                report = report[0:-2] + '.'
            else:
                report = 'На дату ' + message.data + ' нет свободного времени :('
            bot.send_message(message.from_user.id, text=report)
            states.pop(message.from_user.id)

# обрабатываем сообщение со временем
@bot.callback_query_handler(func=lambda call: call.data in record_time.keys())
def new_record_on_time(message):
    global dates, states
    if (message.from_user.id in states) and (message.from_user.id in dates):
        if states[message.from_user.id] == 'record':
            date = dates[message.from_user.id]
            date_format = date[6:] + '-' + date[3:5] + '-' + date[0:2]
            time_start = message.data
            datetime_start = date_format + 'T' + time_start + ':00+03:00'
            time_start_minute = record_time[time_start]
            time_end_minute = str(int(time_start_minute) + 30)
            for key, value in work_time.items():
                if value == time_end_minute:
                    time_end = key
            datetime_end = date_format + 'T' + time_end + ':00+03:00'
            person = message.from_user.first_name + ' ' + message.from_user.last_name + ' id' + str(message.from_user.id)
            # Еще одна проверка свободного времени
            freedom_time = google_calendar.get_freedom_time(date)
            if time_start in freedom_time:
                answer = google_calendar.note_on_time(datetime_start, datetime_end, person)
                if answer == True:
                    report = 'Вы записались на ' + date + ' в ' + time_start
                else:
                    report = 'Не получилось подключиться к календарю для создания записи :('
            else:
                report = 'Это время только что заняли вперед вас :('
            bot.send_message(message.from_user.id, text=report)
        states.pop(message.from_user.id)
        dates.pop(message.from_user.id)

# Узнать время записи
@bot.callback_query_handler(func=lambda call: call.data == 'learn_my_time')
def new_record_on_day(message):
    have_record = google_calendar.get_my_time(str(message.from_user.id))
    if have_record == False:
        report = 'На ближайшую неделю я Вас не записывал'
    else:
        report = 'Вы записаны на ' + have_record
    bot.send_message(message.from_user.id, text=report)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True, interval=1)
        except Exception as e:
            print(e)
            time.sleep(15)