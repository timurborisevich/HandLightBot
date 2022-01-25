from __future__ import print_function
import httplib2
import datetime
import config
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from production_calendar import record_time

# Подключаемся к календарю
credentials = ServiceAccountCredentials.from_json_keyfile_name(config.client_secret_calendar, 'https://www.googleapis.com/auth/calendar')
http = credentials.authorize(httplib2.Http())
service = discovery.build('calendar', 'v3', http=http)

def get_freedom_time(date_text):
    day_events = []
    date = datetime.datetime.strptime(date_text, '%d-%m-%Y').date().isoformat()
    start_day = date + 'T00:00:00+03:00'
    end_day = date + 'T23:59:59+03:00'
    eventsResult = service.events().list(
        calendarId=config.google_calendarId, timeMin=start_day, timeMax=end_day,
        maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    for event in events:
        event_in_day_events = {
            'summary': event['summary'],
            'start': event['start']['dateTime'][11:16],
            'start_minute': int(event['start']['dateTime'][11:13])*60 + int(event['start']['dateTime'][14:16]),
            'end': event['end']['dateTime'][11:16],
            'end_minute': int(event['end']['dateTime'][11:13])*60 + int(event['end']['dateTime'][14:16])
        }
        day_events.append(event_in_day_events)
    change_record_time = record_time.copy()
    for key, value in record_time.items():
        for event in day_events:
            if int(value) >= event['start_minute'] and int(value) < event['end_minute']:
                change_record_time.pop(key)
    return change_record_time

def note_on_time(start_time, end_time, person):
    EVENT = {
        'summary': person,
        'start': {'dateTime': start_time},
        'end': {'dateTime': end_time}
    }
    answer = service.events().insert(calendarId=config.google_calendarId, body=EVENT).execute()
    if answer['status'] == 'confirmed':
        return True
    else:
        return False

def get_my_time(user_id):
    date_start = datetime.date.today().isoformat()
    start_day = date_start + 'T00:00:00+03:00'
    date_end = (datetime.date.today() + datetime.timedelta(days=7)).isoformat()
    end_day = date_end + 'T23:59:59+03:00'
    eventsResult = service.events().list(
        calendarId=config.google_calendarId, timeMin=start_day, timeMax=end_day,
        maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    for event in events:
        summary_sp = event['summary'].split('id')
        if summary_sp[-1] == user_id:
            return event['start']['dateTime'][8:10] + '-' + event['start']['dateTime'][5:7] + '-' \
                   + event['start']['dateTime'][0:4] + ' ' + event['start']['dateTime'][11:16]
    return False