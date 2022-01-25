import datetime

time_server = datetime.datetime.today()
time_moscow = time_server + datetime.timedelta(hours=7)
today = time_moscow
def get_days(today):
    days = {
        'one_day': str(today.strftime("%d-%m-%Y")),
        'two_day': str((today + datetime.timedelta(days=1)).strftime("%d-%m-%Y")),
        'three_day': str((today + datetime.timedelta(days=2)).strftime("%d-%m-%Y")),
        'four_day': str((today + datetime.timedelta(days=3)).strftime("%d-%m-%Y")),
        'five_day': str((today + datetime.timedelta(days=4)).strftime("%d-%m-%Y")),
        'six_day': str((today + datetime.timedelta(days=5)).strftime("%d-%m-%Y")),
        'seven_day': str((today + datetime.timedelta(days=6)).strftime("%d-%m-%Y"))
    }
    return days

record_time = {
     '10:00' : '600',
     '10:30' : '630',
     '11:00' : '660',
     '11:30' : '690',
     '12:00' : '720',
     '12:30' : '750',
     '14:00' : '840',
     '14:30' : '870',
     '15:00' : '900',
     '15:30' : '930',
     '16:00' : '960',
     '16:30' : '990',
     '17:00' : '1020',
     '17:30' : '1050',
     '18:00' : '1080',
     '18:30' : '1110',
     '19:00' : '1140',
     '19:30' : '1170',
}
work_time = record_time.copy()
work_time['20:00'] = '1200'