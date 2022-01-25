from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
from production_calendar import get_days, work_time

# Главная клавиатура
keyboard_main = InlineKeyboardMarkup()
keyboard_main_record = InlineKeyboardButton(text='Хочу записаться на определенное время', callback_data='record')
keyboard_main.add(keyboard_main_record)
keyboard_main_schedule = InlineKeyboardButton(text='Хочу узнать сободное время на ближайшую неделю', callback_data='schedule')
keyboard_main.add(keyboard_main_schedule)
keyboard_main_my_time = InlineKeyboardButton(text='Хочу узнать на какое время я записан', callback_data='learn_my_time')
keyboard_main.add(keyboard_main_my_time)

# Клавиатура с днями
def keyboard_days_select (today):
    keyboard_days_select = InlineKeyboardMarkup()
    days = get_days(today)
    keyboard_days_select_one_day = InlineKeyboardButton(text='Сегодня', callback_data=days['one_day'])
    keyboard_days_select.add(keyboard_days_select_one_day)
    keyboard_days_select_two_day = InlineKeyboardButton(text='Завтра', callback_data=days['two_day'])
    keyboard_days_select_three_day = InlineKeyboardButton(text='Послезавтра', callback_data=days['three_day'])
    keyboard_days_select.row(keyboard_days_select_two_day, keyboard_days_select_three_day)
    keyboard_days_select_four_day = InlineKeyboardButton(text=days['four_day'], callback_data=days['four_day'])
    keyboard_days_select_five_day = InlineKeyboardButton(text=days['five_day'], callback_data=days['five_day'])
    keyboard_days_select_six_day = InlineKeyboardButton(text=days['six_day'], callback_data=days['six_day'])
    keyboard_days_select_seven_day = InlineKeyboardButton(text=days['seven_day'], callback_data=days['seven_day'])
    keyboard_days_select.row(keyboard_days_select_four_day, keyboard_days_select_five_day, keyboard_days_select_six_day, keyboard_days_select_seven_day)
    return keyboard_days_select

# Клавиатура со всем возможным временем
keyboard_times_select = InlineKeyboardMarkup()
keyboard_times_select.add(*[InlineKeyboardButton(text=time, callback_data=time) for time in work_time.keys()])

# Клавиатура со свободным временем
def keyboard_with_freedom_time (par_work_time):
    keyboard_times_select = InlineKeyboardMarkup()
    keyboard_times_select.add(*[InlineKeyboardButton(text=time, callback_data=time) for time in par_work_time.keys()])
    return keyboard_times_select